import replicate
import streamlit as st
from PIL import Image
import cv2
from audio_recorder_streamlit import audio_recorder
import torchaudio
from speechbrain.inference.classifiers import EncoderClassifier
from bhashini_pipelines import bhashini_asr, record_audio, save_wav, bhashini_translate ,bhashini_tts
import pyaudio
import base64
import os
import io
import requests
import json
import numpy as np
import tempfile
from io import BytesIO


def send_to_vlm_api(image_file, text_input):
    # Initialize the Replicate client
    replicate_client = replicate.Client("r8_4zP7jhBoAKiMIk7SMDLJ161WHUTVYdZ2jQ7u0")
    
    # Open the image file
    with Image.open(image_file) as image:
        # Create a BytesIO object from the image
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        question=text_input
        # Define the input data for the CogVLM model
        input = {
            "image": image_bytes,
            "query": "Give a straight answer , guess if you have to but never say i cannot say exactly" + question
        }

        # Run the CogVLM model with the provided input
        output = replicate_client.run(
            "cjwbw/cogvlm:a5092d718ea77a073e6d8f6969d5c0fb87d0ac7e4cdb7175427331e1798a34ed",
            input=input
        )

        # Return the output from the CogVLM model
        return output

def main():
    st.title("Seamless Glasses For Images (CogVLM)")
    file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if file is not None:
        # Check if file is image
        if file.type.startswith("image/"):
            # Display the uploaded image
            image = Image.open(file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

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
                    iso = "hi"
                st.write("Detected language ISO code:", iso)

                # Call the Bhashini ASR API
                with open("temp_audio.wav", "rb") as f:
                    audio_bytes = f.read()
                base64_input = base64.b64encode(audio_bytes).decode("utf-8")
                transcription = bhashini_asr(base64_input, iso)
                st.write("Transcription:", transcription)
                st.write("Please Wait for 1-2 minute for First answer since a new instance is being cold started on replicate (no dedicated API for this VLM)")	

                # Use the transcription with the CogVLM API
                image_bytes = io.BytesIO()
                image.save(image_bytes, format="JPEG")
                base64_image = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

                if iso != "en":
                    translated_text = bhashini_translate(transcription, iso, "en")
                    output = send_to_vlm_api(file, translated_text)
                    translated_answer = bhashini_translate(output, "en", iso)
                    st.write(translated_answer)

                    # Generate base64-encoded audio from the translated answer
                    audio_base64 = bhashini_tts(translated_answer, iso)
                    audio_bytes = base64.b64decode(audio_base64)
                    audio_file = io.BytesIO(audio_bytes)

                    # Play the audio
                    st.audio(audio_file, format="audio/wav")
                else:
                    output = send_to_vlm_api(file, transcription)
                    st.write(output)

                    # Generate base64-encoded audio from the output
                    audio_base64 = bhashini_tts(output, "en")
                    audio_bytes = base64.b64decode(audio_base64)
                    audio_file = io.BytesIO(audio_bytes)

                    # Play the audio
                    st.audio(audio_file, format="audio/wav")

                # Remove the temporary audio file
                os.remove("temp_audio.wav")
        else:
            st.write("Unsupported file format.")

if __name__ == "__main__":
    main()
