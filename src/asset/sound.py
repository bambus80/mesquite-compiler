import wave


def get_wav_sample_data(file_dir: str) -> tuple[int, int]:  # 1st element is sample rate, 2nd is sample count
    with wave.open(file_dir, "rb") as wave_file:
        sample_rate = wave_file.getframerate()
        sample_width = wave_file.getsampwidth()
        frames = wave_file.getnframes()
        channels = wave_file.getnchannels()

    return sample_rate, (sample_rate * sample_width * channels) * frames


def get_mp3_sample_data(file_dir: str) -> tuple[int, int]:  # 1st element is sample rate, 2nd is sample count
    # TODO: Get sample rate and count of MP3 file
    pass
