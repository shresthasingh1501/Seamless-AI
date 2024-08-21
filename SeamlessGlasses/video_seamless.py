import replicate
import streamlit as st
from PIL import Image
import cv2
from audio_recorder_streamlit import audio_recorder
import torchaudio
from speechbrain.inference.classifiers import EncoderClassifier
from bhashini_pipelines import bhashini_asr, record_audio, save_wav ,bhashini_translate , bhashini_tts
import pyaudio
import base64
import os
import io
import requests
import json
import numpy as np
import tempfile
from io import BytesIO



def send_to_vlm_api(frame, transcription, frame_number):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/fireworks/models/firellava-13b",
        "max_tokens": 2048,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": transcription + "give detailed response"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{frame}"
                        }
                    }
                ]
            }
        ]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer 3J2VhOCg9nJF30zpLUJvlALsMAM0zG6b9KjJf1PhX7mx7GIn"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    output = response.json()
    return output["choices"][0]["message"]["content"]


def generate_answer(user_message,context):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    prompt = f"You are an Advanced Video Intelligence AI, capable of analyzing and providing key details on user questions regarding a video file. Here is the context retrieved by our VLM on the video for  equally spaced frames. You have to use the original user question and context to answer user's query.\n\nUser Question: {user_message}\nContext: {context}\n\nYour Response: "
    payload = {
        "model": "accounts/fireworks/models/mixtral-8x7b-instruct",
        "max_tokens": 4096,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer 3J2VhOCg9nJF30zpLUJvlALsMAM0zG6b9KjJf1PhX7mx7GIn"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    llm_response = response.json()['choices'][0]['message']['content'].replace('\\n', '')
    return llm_response


st.title("Seamless Glasses For Video (FireLLaVA)")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Create a temporary file to store the uploaded video
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_filename = tmp.name
    st.video(uploaded_file.read())

    # Read the video file
    video = cv2.VideoCapture(tmp_filename)

    # Get the total number of frames
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the step size to get 6 equally spaced frames
    step_size = total_frames // 6

    # Initialize a list to store the frames
    frame_codes = []

    # Loop through the video and extract frames at the specified intervals
    for i in range(6):
        video.set(cv2.CAP_PROP_POS_FRAMES, i * step_size)
        ret, frame = video.read()
        if ret:
            # Convert the frame to PIL Image format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame)

            # Convert the PIL Image to base64
            buffered = BytesIO()
            pil_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Append the base64 code to the list
            frame_codes.append(img_str)

    # Release the video capture object
    video.release()

    # Audio recording
    audio_bytes = audio_recorder(
        "Record Audio For Atleast 5 Seconds for accurate Language Detection",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        icon_name="microphone-lines",
        icon_size="6x"
    )

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

        # Save the recorded audio to a WAV file
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)

        # Load the language identification model
        language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa")

        # Load the recorded audio file
        signal = language_id.load_audio("temp_audio.wav")

        # Classify the language of the audio
        prediction = language_id.classify_batch(signal)

        # Extract the ISO code from the prediction
        iso_code = prediction[3][0]
        iso = iso_code.split(":")[0]
        if iso == "la" or iso == "nn":
            iso = "en"
        elif iso == "ur":
            iso == "hi"
        st.write("Detected language ISO code:", iso)

        # Call the Bhashini ASR API
        with open("temp_audio.wav", "rb") as f:
            audio_bytes = f.read()
        base64_input = base64.b64encode(audio_bytes).decode("utf-8")
        transcription = bhashini_asr(base64_input, iso)
        st.write("Transcription:", transcription)
        if iso!="en":
           translated_text=bhashini_translate(transcription,iso,"en")
           context = ""
           st.write(translated_text)
           # Use the transcription and frames with the Fireworks AI API
           for i, frame in enumerate(frame_codes):
               output = send_to_vlm_api(frame, translated_text, i)
               frame_context = f"Frame {i+1}:" + output
               context = context + frame_context
           response=generate_answer(translated_text,context)
           translated_answer=bhashini_translate(response,"en",iso)
           audio_base64 = bhashini_tts(translated_answer, iso)
           audio_bytes = base64.b64decode(audio_base64)
           audio_file = io.BytesIO(audio_bytes)
           # Play the audio
           st.audio(audio_file, format="audio/wav")
        else:
        # Use the transcription and frames with the Fireworks AI API
            context = ""
            for i, frame in enumerate(frame_codes):
                output = send_to_vlm_api(frame, transcription, i)
                frame_context = f"Frame {i+1}:" + output
                context = context + frame_context
            response=generate_answer(transcription,context)
            st.write(response)
            # Generate base64-encoded audio from the output
            audio_base64 = bhashini_tts(response, "en")
            audio_bytes = base64.b64decode(audio_base64)
            audio_file = io.BytesIO(audio_bytes)

            # Play the audio
            st.audio(audio_file, format="audio/wav")

        # Remove the temporary audio file
        os.remove("temp_audio.wav")



else:
    st.warning("Please upload a video file.")

