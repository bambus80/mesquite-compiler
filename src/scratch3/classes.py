from dataclasses import dataclass, field, asdict
from typing import Literal
from src.utils import block_id


@dataclass
class ScratchBlock:
    id: str = block_id
    opcode: str = ""
    next = None
    parent = None
    inputs: dict = field(default_factory=dict)
    fields: dict = field(default_factory=dict)
    shadow: bool = False
    topLevel: bool = True if not parent else False


@dataclass
class ScratchMutatedBlock(ScratchBlock):
    mutation: dict = field(default_factory=dict)


class BlockColumn:
    def __init__(self) -> None:
        self.list: list[ScratchBlock] = []

    def parse(self) -> list:
        parsed: list[dict] = []
        for i in range(0, len(self.list) - 1):
            parent = self.list[i - 1] if i > 0 else None
            current = self.list[i]
            next = self.list[i + 1] if i <= len(self.list) - 1 else None

            current.parent = parent.id
            current.next = next.id
            parsed.append(asdict(current))
        return parsed


@dataclass
class ScratchTarget:
    isStage: bool = False
    name: str = ""
    variables: dict = field(default_factory=dict)
    lists: dict = field(default_factory=dict)
    broadcasts: dict = field(default_factory=dict)
    blocks: dict = field(default_factory=dict)
    comments: dict = field(default_factory=dict)
    currentCostume: int = 0
    costumes: list = field(default_factory=list)
    sounds: list = field(default_factory=list)
    layerOrder: int = 0
    volume: float = 100


@dataclass
class Stage(ScratchTarget):
    isStage: bool = True
    name: str = "Stage"
    tempo: int = 60
    videoState: Literal["on", "off", "on-flipped"] = "off"
    videoTransparency: int = 50
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
class ScratchMonitor:
    # TODO: Support monitors
    ...


@dataclass
class ScratchExtension:
    # TODO: Support Scratch extensions
    ...


@dataclass
class ScratchProject:
    targets: list[ScratchTarget] = field(default_factory=list)
    monitors: list[ScratchMonitor] = field(default_factory=list)
    extensions: list[ScratchExtension] = field(default_factory=list)
    meta = {
        "semver": "3.0.0",
        "vm": "0.0.0",
        "agent": "",
    }
