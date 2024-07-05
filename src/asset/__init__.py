import os
import mimetypes
from src.parsing.classes import CostumeStatement, SoundStatement
from src.scratch3.classes import ScratchAsset, Costume, Sound
from src.logging import *
from src.utils import md5ext


native_image_formats = {
    "image/png": "png",
    "image/bmp": "bmp",
    "image/jpeg": "jpg",
    "image/gif": "gif",
    "image/svg+xml": "svg"
}
convertible_image_formats = {  # TODO: Convert image formats to native ones
    "application/postscript": "eps",
    "image/heic": "heic",
    "image/vnd.adobe.photoshop": "psd"
}
native_sound_formats = {
    "audio/mpeg": "mp3",
    "audio/wav": "wav"
}
convertible_sound_formats = {  # TODO: Convert sound formats to native ones
    "audio/flac": "flac",
    "audio/aac": "aac",
    "audio/ogg": "ogg"
}


def serialize_asset(asset: CostumeStatement | SoundStatement, project_cwd: str) -> ScratchAsset:
    file_path = os.path.join(project_cwd, asset.import_from)
    file_format, _ = mimetypes.guess_type(file_path)

    new_asset = None
    if isinstance(asset, CostumeStatement):
        new_asset = Costume()
    elif isinstance(asset, SoundStatement):
        new_asset = Sound()

    # Check if file format is valid and convert it to a supported one if necessary
    if not file_format:
        log_error(f"Could not recognize file format of {file_path}")
        exit(1)
    elif file_format in native_image_formats:
        new_asset.dataFormat = native_image_formats[file_format]
    elif file_format in native_sound_formats:
        new_asset.dataFormat = native_sound_formats[file_format]
    elif file_format in convertible_image_formats or file_format in convertible_sound_formats:
        log_error(f"The file type of {file_path} is not yet supported: {file_format}")
        exit(1)
    else:
        log_error(f"The file type of {file_path} is not valid: {file_format}")
        exit(1)

    if asset.import_to:
        new_asset.name = asset.import_to
    else:
        new_asset.name = os.path.splitext(asset.import_from)[0]  # Filename without extension

    # Get MD5 hash of file
    try:
        with open(file_path, "rb") as file:
            asset_md5 = md5ext(file.read())
    except OSError:
        log_error(f"Could not access {file_path}")
        exit(1)

    new_asset.assetId = asset_md5
    new_asset.md5ext = f"{asset_md5}.{new_asset.dataFormat}"

    if isinstance(new_asset, Costume):
        if new_asset.dataFormat == "svg":
            # TODO: Set proper rotation centers for SVG costumes
            new_asset.rotationCenterX = 0
            new_asset.rotationCenterY = 0
        elif new_asset.dataFormat in ["png", "bmp", "jpg", "jpeg", "gif"]:
            pass
    elif isinstance(new_asset, Sound):
        if new_asset.dataFormat == "wav":
            # TODO: Set proper metadata for WAV sounds
            new_asset.rate = 48000
            new_asset.sampleCount = 0

    return new_asset
