## Usage

### SpeechLID.py

1. Replace the line `signal = language_id.load_audio("load wav file here")` with the path to your input audio file.
2. Run the script using `python SpeechLID.py`.
3. The script will output the ISO 639-3 language code of the detected language.

### IndicLID_Inference.ipynb

1. Open the Jupyter Notebook `IndicLID_Inference.ipynb`.
2. Follow the instructions in the notebook to download the required model files.
3. Provide the input text samples for language and script identification.
4. Run the cells in the notebook to obtain the predicted language, script, and confidence scores.

## Contributing

Contributions to this repository are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [SpeechBrain](https://github.com/speechbrain/speechbrain) for the language identification model and library.
- [AI4Bharat](https://github.com/AI4Bharat/IndicLID) for the IndicLID model and code.
