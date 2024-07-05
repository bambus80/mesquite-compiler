from src.parsing.classes import CostumeStatement, SoundStatement

native_image_formats = [
    "png",
    "bmp",
    "jpg",
    "jpeg",
    "gif",
    "svg"
]
convertible_image_formats = [  # TODO: Convert image formats to native ones
    "eps",
    "heic",
    "psd"
]
native_sound_formats = [
    "mp3",
    "wav"
]
convertible_sound_formats = [  # TODO: Convert sound formats to native ones
    "flac",
    "aac",
    "ogg"
]


def handle_asset(asset: CostumeStatement | SoundStatement):
    pass
