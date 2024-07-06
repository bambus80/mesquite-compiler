import wave
from src.logging import *
from pydub import AudioSegment


def get_wav_sample_data(file_dir: str) -> tuple[int, int]:  # 1st element is sample rate, 2nd is sample count
    try:
        with wave.open(file_dir, "rb") as wave_file:
            sample_rate = wave_file.getframerate()
            frames = wave_file.getnframes()
            channels = wave_file.getnchannels()
    except OSError:
        log_error(f"Could not access {file_dir}")
        exit(1)

    return sample_rate, (sample_rate * channels) * frames


def get_mp3_sample_data(file_dir: str) -> tuple[int, int]:  # 1st element is sample rate, 2nd is sample count
    try:
        audio = AudioSegment.from_mp3(file_dir)
        audio.duration_seconds
    except OSError:
        log_error(f"Could not access {file_dir}")
        exit(1)

    return audio.frame_rate, (audio.frame_rate * audio.channels) * audio.frame_count()
