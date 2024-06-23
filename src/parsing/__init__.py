from lark_parser import Lark_StandAlone, Transformer
from dataclasses import dataclass
from typing import Literal

@dataclass
class Variable:
    name: str
    var_typing: str
    var_type: Literal["const", "var", "list"]
    var_locality: Literal["sprite","global","cloud"]

class Reformatter(Transformer):
    def
