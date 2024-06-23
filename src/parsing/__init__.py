import inspect
from pprint import pprint
from types import FunctionType

from lark import Transformer, Lark

from dataclasses import dataclass
from typing import Literal, Any, Callable


@dataclass
class VariableDefinition:
    name: str
    var_typing: str
    var_type: Literal["const", "var", "list"]
    var_locality: Literal["sprite", "global", "cloud"]
    value: Any


class Reformatter(Transformer):
    def keyword(self, s):
        (s,) = s
        if s in ["true", "True"]:
            return True
        if s in ["false", "False"]:
            return False
        return s.value

    def var_locality(self, s):
        (s,) = s
        return s.value

    @staticmethod
    def return_object(name: Any) -> Callable[[Any, Any], Any]:
        def internal(_, __):
            return name

        return internal

    type_number = return_object("type_number")
    type_string = return_object("type_string")
    type_bool = return_object("type_bool")
    type_value = return_object("type_value")

    #def variable_define(self, argtuple):
    #     ...


with open("parser.lark", "r") as larkfile:
    parser = Lark(larkfile, parser='lalr')

if __name__ == '__main__':
    with open("test.msq") as f:
        tree = parser.parse(f.read())
        print(Reformatter().transform(tree))
