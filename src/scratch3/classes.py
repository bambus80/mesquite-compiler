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
    topLevel: bool = False


@dataclass
class ScratchMutatedBlock(ScratchBlock):
    mutation: dict = field(default_factory=dict)


class BlockColumn:
    def __init__(self, col=None) -> None:
        if col is None:
            col = []
        self.col: list[ScratchBlock] = col

    def parse(self) -> list:
        parsed: list[dict] = []
        for i in range(0, len(self.col) - 1):
            parent_block = self.col[i - 1] if i > 0 else None
            current_block = self.col[i]
            next_block = self.col[i + 1] if i <= len(self.col) - 1 else None

            current_block.parent = parent_block.id
            current_block.next = next_block.id
            current_block.topLevel = isinstance(current_block.parent, str)
            parsed.append(asdict(current_block))
        return parsed


class ScratchTarget:
    def __init__(self):
        self.isStage: bool = False
        self.name: str = ""
        self.variables: dict = {}
        self.lists: dict = {}
        self.broadcasts: dict = {}
        self.blocks: BlockColumn = BlockColumn
        self.comments: dict = {}
        self.currentCostume: int = 0
        self.costumes: list = []
        self.sounds: list = []
        self.layerOrder: int = 0
        self.volume: float = 100

    def serialize(self):
        self.costumes = [asdict(c) for c in self.costumes]
        self.sounds = [asdict(s) for s in self.sounds]
        return {"isStage": self.isStage,
                "name": self.name,
                "variables": self.variables,
                "lists": self.lists,
                "broadcasts": self.broadcasts,
                "blocks": self.blocks.parse(),
                "comments": self.comments,
                "currentCostume": self.currentCostume,
                "costumes": self.costumes,
                "sounds": self.sounds,
                "layerOrder": self.layerOrder,
                "volume": self.volume
                }


class Stage(ScratchTarget):
    tempo: int = 60
    videoState: Literal["on", "off", "on-flipped"] = "off"
    videoTransparency: int = 50
    textToSpeechLanguage: str = "English"

    def __init__(self, tempo: int = 60, videoState: Literal["on", "off", "on-flipped"] = "off",
                 videoTransparency: int = 50, textToSpeechLanguage: str = "English"):
        super().__init__()
        self.isStage = True
        self.name = "Stage"
        self.tempo = tempo
        self.videoState = videoState
        self.videoTransparency = videoTransparency
        self.textToSpeechLanguage = textToSpeechLanguage

    def serialize(self):
        self.costumes = [asdict(c) for c in self.costumes]
        self.sounds = [asdict(s) for s in self.sounds]
        return {"isStage": self.isStage,
                "name": self.name,
                "variables": self.variables,
                "lists": self.lists,
                "broadcasts": self.broadcasts,
                "blocks": self.blocks.parse(),
                "comments": self.comments,
                "currentCostume": self.currentCostume,
                "costumes": self.costumes,
                "sounds": self.sounds,
                "layerOrder": self.layerOrder,
                "volume": self.volume,
                "tempo": self.tempo,
                "videoState": self.videoState,
                "videoTransparency": self.videoTransparency,
                "textToSpeechLanguage": self.textToSpeechLanguage
                }


class Sprite(ScratchTarget):
    visible: bool = True
    x: float = 0
    y: float = 0
    size: float = 100
    direction: float = 90
    draggable: bool = False
    rotationStyle: Literal["all around", "left-right", "don't rotate"] = "all around"

    def __init__(self, name: str = "", visible: bool = True, x: float = 0, y: float = 0, size: float = 100,
                 direction: float = 90, draggable: bool = False,
                 rotationStyle: Literal["all around", "left-right", "don't rotate"] = "all around"):
        super().__init__()
        self.name = name
        self.visible = visible
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction
        self.draggable = draggable
        self.rotationStyle = rotationStyle

    def serialize(self):
        self.costumes = [asdict(c) for c in self.costumes]
        self.sounds = [asdict(s) for s in self.sounds]
        return {"isStage": self.isStage,
                "name": self.name,
                "variables": self.variables,
                "lists": self.lists,
                "broadcasts": self.broadcasts,
                "blocks": self.blocks.parse(),
                "comments": self.comments,
                "currentCostume": self.currentCostume,
                "costumes": self.costumes,
                "sounds": self.sounds,
                "layerOrder": self.layerOrder,
                "volume": self.volume,
                "visible": self.visible,
                "x": self.x,
                "y": self.y,
                "size": self.size,
                "direction": self.direction,
                "draggable": self.draggable,
                "rotationStyle": self.rotationStyle
                }


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


class ScratchProject:
    def __init__(self):
        self.targets: list[ScratchTarget] = []
        self.monitors: list[ScratchMonitor] = []
        self.extensions: list[ScratchExtension] = []
        self.meta = {
            "semver": "3.0.0",
            "vm": "0.0.0",
            "agent": "",
        }

    def serialize(self) -> dict:
        self.targets = [t.serialize() for t in self.targets]
        self.extensions = [asdict(e) for e in self.extensions]
        return {"targets": self.targets,
                "monitors":[],
                "extensions": self.extensions,
                "meta": self.meta}
