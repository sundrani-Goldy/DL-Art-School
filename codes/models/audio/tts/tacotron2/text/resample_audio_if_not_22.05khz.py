import librosa
import soundfile as sf
from glob import glob

def resample_wav_file(input_file, target_sampling_rate=22050):
    # Load audio file
    audio, sampling_rate = librosa.load(input_file, sr=None)

    # Check if the sampling rate matches the target
    if sampling_rate != target_sampling_rate:

        # Resample audio to the target sampling rate
        audio_resampled = librosa.resample(audio, orig_sr=sampling_rate, target_sr=target_sampling_rate)

        # Overwrite the input file with the resampled audio
        sf.write(input_file, audio_resampled, target_sampling_rate)

dataset_path = "/home/ubuntu/Testing/DL-Art-School/datasets/wavs/"
# Resample all audio samples to 22.05kHz
dataset_path = "/home/ubuntu/Testing/DL-Art-School/datasets/wavs"
for wav_file in glob(dataset_path + "*.wav"):
    resample_wav_file(wav_file)