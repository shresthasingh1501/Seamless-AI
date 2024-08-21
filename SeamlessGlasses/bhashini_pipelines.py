import json
import requests
import base64
import pyaudio
import wave
import os
from pydub import AudioSegment
from pydub.playback import play
# first try all with giving in the base64 input, we'll work out on taking input from user later

def record_audio(stream, rate = 44100, frame_length = 1024, record_seconds = 5):
    print("Recording...")
    frames = []
    for _ in range(0, int(rate / frame_length * record_seconds)):
        try:
            data = stream.read(frame_length, exception_on_overflow=False) 
            frames.append(data)
        except IOError as e:
            if e.errno == pyaudio.paInputOverflowed:
                # Handling overflow
                continue  # Proceed to the next frame
    print("Recording stopped.")
    return b''.join(frames)

def save_wav(audio_data, directory='./temp', channels=2, sample_width=2, frame_rate=44100):
    # Create the directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Creating the path for the filename
    file_path = os.path.join(directory, 'input.wav')
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(frame_rate)
        wf.writeframes(audio_data)



########### ENTER BHASHINI INFERENCE API KEY ###########
bhashini_api_key = '-ZMTsWoHLAsGSKpgnvuwPF3LJUK71XPdYxnMPW6dC55JfDa_Sgy4vYi6JHi7ZnE0'

def bhashini_asr(base64_input, input_language):
    url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
    asr_serviceid_dict = {'bn': 'ai4bharat/conformer-multilingual-indo_aryan-gpu--t4', 'en': 'ai4bharat/whisper-medium-en--gpu--t4', 'gu': 'ai4bharat/conformer-multilingual-indo_aryan-gpu--t4', 'hi': 'ai4bharat/conformer-hi-gpu--t4', 'kn': 'ai4bharat/conformer-multilingual-dravidian-gpu--t4', 'ml': 'ai4bharat/conformer-multilingual-dravidian-gpu--t4', 'mr': 'ai4bharat/conformer-multilingual-indo_aryan-gpu--t4', 'or': 'ai4bharat/conformer-multilingual-indo_aryan-gpu--t4', 'pa': 'ai4bharat/conformer-multilingual-indo_aryan-gpu--t4', 'sa': 'ai4bharat/conformer-multilingual-indo_aryan-gpu--t4', 'ta': 'ai4bharat/conformer-multilingual-dravidian-gpu--t4', 'te': 'ai4bharat/conformer-multilingual-dravidian-gpu--t4', 'ur': 'ai4bharat/conformer-multilingual-indo_aryan-gpu--t4'}

    asr_serviceid_val = asr_serviceid_dict[input_language]

    payload = json.dumps({
    "pipelineTasks": [
        {
        "taskType": "asr",
        "config": {
            "language": {
            "sourceLanguage": input_language
            },
            "serviceId": asr_serviceid_val,
            "audioFormat": "wav",
            "samplingRate": 16000
        }
        }
    ],
    "inputData": {
        "audio": [
        {
            "audioContent": base64_input
        }
        ]
    }
    })
    headers = {
    'Accept': '*/*',
    'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
    'Authorization': bhashini_api_key,
    'Content-Type': 'application/json',
    "Connection": "keep-alive"
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    output = json_data["pipelineResponse"][0]["output"][0]["source"]
    return(output)


def bhashini_translate(my_input, input_language, output_language='en'):
    url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
    nmt_serviceid_dict = {'bn,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'bn,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'en,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'gu,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'hi,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'kn,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ml,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'mr,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'or,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'pa,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'sa,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ta,te': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'te,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,en': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,as': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,bn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,brx': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,gu': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,hi': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,kn': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,ml': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,mni': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,mr': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,or': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,pa': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,ta': 'ai4bharat/indictrans-v2-all-gpu--t4', 'ur,te': 'ai4bharat/indictrans-v2-all-gpu--t4'}
    comb = str(input_language) + "," + str(output_language)
    nmt_serviceid_val = nmt_serviceid_dict[comb]

    payload = json.dumps({
      "pipelineTasks": [
        {
          "taskType": "translation",
          "config": {
            "language": {
              "sourceLanguage": input_language,
              "targetLanguage": output_language
            },
            "serviceId": nmt_serviceid_val
          }
        }
      ],
      "inputData": {
        "input": [
          {
            "source": my_input
          }
        ]
      }
    })
    headers = {
      'Accept': '*/*',
      'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
      'Authorization': bhashini_api_key,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    output = json_data["pipelineResponse"][0]["output"][0]["target"]
    return output


def bhashini_tts(my_input, input_language):
    url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
    tts_serviceid_dict = {'en': 'ai4bharat/indic-tts-coqui-misc-gpu--t4', 'as': 'ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4', 'brx': 'ai4bharat/indic-tts-coqui-misc-gpu--t4', 'gu': 'ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4', 'hi': 'ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4', 'kn': 'ai4bharat/indic-tts-coqui-dravidian-gpu--t4', 'ml': 'ai4bharat/indic-tts-coqui-dravidian-gpu--t4', 'mni': 'ai4bharat/indic-tts-coqui-misc-gpu--t4', 'mr': 'ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4', 'or': 'ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4', 'pa': 'ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4', 'ta': 'ai4bharat/indic-tts-coqui-dravidian-gpu--t4', 'te': 'ai4bharat/indic-tts-coqui-dravidian-gpu--t4', 'bn': 'ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4'}
    tts_serviceid_val = tts_serviceid_dict[input_language]

    payload = json.dumps({
    "pipelineTasks": [
        {
        "taskType": "tts",
        "config": {
            "language": {
            "sourceLanguage": input_language
            },
            "serviceId": tts_serviceid_val,
            "gender": "female"
        }
        }
    ],
    "inputData": {
        "input": [
        {
            "source": my_input
        }
        ]
    }
    })
    headers = {
    'Accept': '*/*',
    'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
    'Authorization': bhashini_api_key,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    output = json_data["pipelineResponse"][0]["audio"][0]["audioContent"]
    # # Play the audio segment
    return output
