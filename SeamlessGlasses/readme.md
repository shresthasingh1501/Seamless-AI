# Seamless Glasses

Seamless Glasses is a project that combines audio, video, and image processing capabilities with natural language processing and computer vision models to provide intelligent assistants for multimedia content. The project includes two main applications: `video_seamless.py` and `image_seamless.py`.

## video_seamless.py

This application allows users to upload a video file and record an audio query related to the video content. The recorded audio is processed to detect the language, and the transcription is obtained using automatic speech recognition (ASR). If the detected language is not English, the transcription is translated to English.

Six equally spaced frames from the video are then sent to the FireLLaVA (FireWorks LLaVA) multimodal AI model, along with the transcription or its English translation. FireLLaVA generates context descriptions for each frame based on the transcription and video frames.

The context descriptions from FireLLaVA are then used by another large language model, Mixtral, to generate a comprehensive answer to the user's query. If the original language was not English, the answer is translated back to the original language.

Finally, the application displays the answer and provides an option to play the answer as synthesized speech using a text-to-speech (TTS) model.

## image_seamless.py

This application is similar to `video_seamless.py`, but it focuses on image content instead of videos. Users can upload an image file and record an audio query related to the image. The recorded audio is processed for language detection, transcription, and translation (if necessary).

The transcription (or its English translation) and the uploaded image are then sent to the CogVLM (Cognitive Visual Language Model) multimodal AI model. CogVLM generates a textual answer based on the image and the transcription.

The application displays the answer from CogVLM and provides an option to play the answer as synthesized speech using a TTS model.

## Dependencies

The project relies on the following Python libraries and services:

- Replicate (for CogVLM)
- Streamlit (for the web application)
- Pillow (for image processing)
- OpenCV (for video processing)
- PyAudio (for audio recording)
- NumPy (for numerical operations)
- Requests (for making API calls)
- SpeechBrain (for language identification)
- Bhashini Pipelines (for ASR, machine translation, and TTS)

The required packages are listed in the `requirements.txt` file.

## Usage

1. Install the required packages by running `pip install -r requirements.txt`.
2. Run `streamlit run video_seamless.py` or `streamlit run image_seamless.py` to start the respective application.
3. Follow the instructions in the web application to upload a video/image file and record an audio query.
4. Wait for the application to process the input and generate the answer.
5. The answer will be displayed in the web application, and you can optionally play the synthesized speech.

Note: The applications use the FireLLaVA and CogVLM models hosted on the Replicate platform, which may require some time for initial model loading and inference.
