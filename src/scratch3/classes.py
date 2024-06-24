from dataclasses import dataclass, field
from typing import Literal
from src.utils import block_id


@dataclass
class ScratchBlock:
    id = ""
    opcode = ""
    next = None
    parent = None
    inputs = {}
    fields = {}
    shadow = False
    topLevel = False if not parent else True


@dataclass
class ScratchPrototypeBlock(ScratchBlock):
    mutation = {}


@dataclass
class ScratchTarget:
    isStage: bool = False
    name: str = ""
    variables: dict = field(default_factory=dict)
    lists: dict = field(default_factory=dict)
    broadcasts: dict = field(default_factory=dict)
    blocks: dict = field(default_factory=dict)
    comments: dict = {
        block_id: {
            "blockId": None,
            "x": 200,
            "y": 100,
            "width": 400,
            "height": 200,
            "minimized": False,
            "text":"Compiled from Mesquite code.\n\nThis code is the output of the Mesquite compiler and is not supposed to be human readable."
        }
    }
    currentCostume: int = 0
    costumes: list = field(default_factory=list)
    sounds: list = field(default_factory=list)
    layerOrder: int = 0
    volume: float = 100


@dataclass
class Stage(ScratchTarget):
    tempo: int = 60
    videoState: Literal["on", "off", "on-flipped"] = "off"
    textToSpeechLanguage: str = "English"


@dataclass
class Sprite(ScratchTarget):
    visible: bool = True
    x: float = 0
    y: float = 0
    size: float = 100
    direction: float = 90
    draggable: bool = False
    rotationStyle: Literal["all around", "left-right", "don't rotate"] = "all around"


@dataclass
class ScratchAsset:
    assetId: str = ""
    name: str = ""
    dataFormat: str = ""
    md5ext: str = f"{assetId}.{dataFormat}"


@dataclass
class Costume(ScratchAsset):
    bitmapResolution: float = 1
    rotationCenterX: float = 0
    rotationCenterY: float = 0


@dataclass
class Sound(ScratchAsset):
    rate: int = 0
    sampleCount: int = 0


@dataclass
class ScratchProject:
    targets: list = field(default_factory=list)
    monitors: list = field(default_factory=list)
    extensions: list = field(default_factory=list)
    meta = {
        "semver": "3.0.0",
        "vm": "0.0.0",
        "agent": "",
        "platform": { 
            "name": "Mesquite Compiler",
            "url": "https://github.com/bambus80/mesquite-compiler"
        }
    }