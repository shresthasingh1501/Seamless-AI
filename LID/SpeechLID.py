import torchaudio
from speechbrain.inference.classifiers import EncoderClassifier
language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa")
signal = language_id.load_audio("load wav file here")
prediction = language_id.classify_batch(signal)
# Extract the ISO code from the prediction
iso_code = prediction[3][0]
iso = iso_code.split(":")[0]
print(iso)


