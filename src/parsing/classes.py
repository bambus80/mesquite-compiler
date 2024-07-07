from dataclasses import dataclass
from typing import Literal, Any, Optional, List, Union
from enum import StrEnum


class VariableSetOp(StrEnum):
    ASSIGN = "="
    ADD_ASSIGN = "+="
    SUBTRACT_ASSIGN = "-="
    MULTIPLY_ASSIGN = "*="
    DIVIDE_ASSIGN = "/="


class MathExprOp(StrEnum):
    ADD = "+"
    SUBTRACT = "-"
    DIVIDE = "/"
    MULTIPLY = "*"
    MODULO = "%"
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    NOT_EQUAL = "!="
    EQUAL = "=="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="


@dataclass
class MathExpr:
    expression_left: Any
    operation: MathExprOp
    expression_right: Any


@dataclass
class VariableSet:
    variable: str
    operation: VariableSetOp
    expression: Any

@dataclass
class ListType:
    subtype: str


@dataclass
class CodeStatement:
    ...


@dataclass
class Function(CodeStatement):
    name: str
    arguments: Optional[List[Any]]

@dataclass
class VariableDefinition(CodeStatement):
    name: str
    var_typing: str
    var_type: Literal["const", "var", "list"]
    var_locality: Literal["sprite", "global", "cloud"]
    value: Optional[Any]


@dataclass
class Hat:
    code: Optional[List[CodeStatement]]

@dataclass
class CodeStatementHat(Hat, CodeStatement):
    ...

@dataclass
class IfInner(CodeStatementHat):
    condition: MathExpr

@dataclass
class ElifInner(CodeStatementHat):
    condition: MathExpr

@dataclass
class ElseInner(CodeStatementHat):
    ...

@dataclass
class IfHat(CodeStatementHat):
    ifinner: Optional[IfInner]
    elifs: Optional[List[ElifInner]]
    ifhat_else: Optional[ElseInner]


@dataclass
class LoopHat(CodeStatementHat):
    arguments: Optional[List[Any]]

@dataclass
class ComponentHat(Hat):
    ...


@dataclass
class InitializationHat(ComponentHat):
    ...


@dataclass
class FunctionVariableDefinition:
    name: str
    type: Union[str, ListType]
    optional: bool

@dataclass
class FunctionDefinitionHat(ComponentHat):
    vars: Optional[List[FunctionVariableDefinition]]
    name: str

@dataclass
class OnHat(ComponentHat):
    arguments: Optional[List[Any]]
    on_keyword: str


@dataclass
class ProgramComponent:
    hats: Optional[List[Hat]]


@dataclass
class LibraryComponent(ProgramComponent):
    ...


@dataclass
class StageComponent(ProgramComponent):
    ...


@dataclass
class SpriteComponent(ProgramComponent):
    sprite: str


@dataclass
class Statement:
    import_from: str
    import_to: str
    origin: str = "ext"


@dataclass
class Directive:
    ...


@dataclass
class UseStatement(Statement, Directive):
    ...


@dataclass
class SpriteStatement(Statement):
    ...


@dataclass
class SoundStatement(SpriteStatement):
    ...


@dataclass
class CostumeStatement(SpriteStatement):
    ...


@dataclass
class Program:
    directives: Optional[List[Directive]]
    components: Optional[List[ProgramComponent]]


@dataclass
class NotExpr:
    ...


@dataclass
class NotExprWithBool:
    boolean: Any