from pathlib import Path
from typing import Any, Callable

import lark.exceptions
from lark import Transformer, Lark, Token

from src.parsing.classes import *
from src.logging import *
from src.utils import pretty_print_program


class Reformatter(Transformer):
    def true(self, s):
        return True

    def false(self, s):
        return False

    @staticmethod
    def return_object(name: Any) -> Callable[[Any, Any], Any]:
        def internal(_, __):
            return name

        return internal

    def return_value(self, val):
        return val[0].value

    def return_first(self, val):
        return val[0]

    def keyword(self, s):
        (s,) = s
        return s.value

    def expression(self, s):
        if isinstance(s[0], (str, int, float, bool, type(None), list, Token)):
            (s,) = s
        return s

    type_number = return_object("!type_number")
    type_string = return_object("!type_string")
    type_bool = return_object("!type_bool")
    type_value = return_object("!type_value")
    var_locality = return_value
    number = return_value
    var_type = return_value
    code_stmts = return_first
    parenthesis_expression = return_first

    def type_custom(self, s):
        return f"!type_!custom_{s[0]}"

    def find_variable_type(self, name):
        definition = self.find_variable_definition(name)
        return definition.var_typing

    def variable_define(self, argtuple):
        if argtuple[2].startswith("!type_"):
            return VariableDefinition(argtuple[3], argtuple[2][6:], argtuple[1], argtuple[0], argtuple[4] or None)
        return VariableDefinition(argtuple[2], "value", argtuple[1], argtuple[0], argtuple[3] or None)

    def variable_call(self, s):
        name = s[0]
        var_type = self.find_variable_type(name)
        referenced_definition = self.find_variable_definition(name)
        return VariableCall(name, var_type, referenced_definition)

    def hat_init(self, s):
        return InitializationHat(s)

    def library(self, s):
        return LibraryComponent(s)

    def stage(self, s):
        return StageComponent(s)

    def sprite(self, s):
        return SpriteComponent(s[1:], s[0])

    def string(self, s):
        (s,) = s
        return s[1:-1]

    def use_stmt(self, s):
        if s[1] is None:
            return UseStatement(s[0], s[0])
        return UseStatement(s[0], s[1])

    def sound_stmt(self, s):
        if s[1] is None:
            return SoundStatement(s[0], s[0])
        return SoundStatement(s[0], s[1])

    def costume_stmt(self, s):
        if s[1] is None:
            return CostumeStatement(s[0], s[0])
        return CostumeStatement(s[0], s[1])

    def start(self, s):
        program = Program([], [])
        for component in s:
            if isinstance(component, Directive): program.directives.append(component)
            if isinstance(component, ProgramComponent): program.components.append(component)
        return program

    def list(self, s):
        list = []
        for element in s:
            list.append(element)
        return list

    def hat_loop(self, s):
        if not isinstance(s[0], list):
            return LoopHat(s, None)
        return LoopHat(s[1:],s[0])

    array = return_first
    arguments = return_first

    arguments_custom_block = return_first

    def list_custom_block(self, s):
        list = []
        for element in s:
            list.append(element)
        return list

    def keyword_custom_block(self, s):
        if len(s) == 1:
            return FunctionVariableDefinition(s[0], "value", False)
        if len(s) == 2:
            return FunctionVariableDefinition(s[0], s[1], False)
        if len(s) == 3:
            return FunctionVariableDefinition(s[0], s[2], True)

    def variable_set_ops(self, s):
        return VariableSetOp(s[0].value)
    def variable_set(self, s):
        return VariableSet(s[0], s[1], s[2])

    def math_expr_ops(self, s):
        return MathExprOp(s[0].value)

    def not_expr(self, s):
        return NotExpr()

    def math_expr(self, s):
        if len(s) == 1:
            return s[0]
        if len(s) == 2:
            if isinstance(s[1], Token):
                s[1] = s[1].value
            if isinstance(s[0], NotExpr) and isinstance(s[1], bool):
                return not s[1]
            elif isinstance(s[0], NotExpr):
                return NotExprWithBool(s[1])
        if len(s) == 3:
            return MathExpr(s[0], s[1], s[2])
        return s

    def function(self, s):
        if len(s) == 1:
            return Function(s[0], None)
        return Function(s[0], s[1])

    def hat_custom_block(self, s):
        return FunctionDefinitionHat(s[2:], s[1], s[0])

    def hat(self, s):
        if isinstance(s[1], list): return OnHat(s[2:], s[1], s[0])
        return OnHat(s[1:], None, s[0])

    def if_loop_if(self, s):
        return IfInner(s[1:], s[0])

    def if_loop_elif(self, s):
        return ElifInner(s[1:], s[0])

    def if_loop_else(self, s):
        return ElseInner(s)

    def if_loop(self, s):
        ifloop = IfHat([], None, [], None)
        for section in s:
            if isinstance(section, IfInner): ifloop.ifinner = section
            elif isinstance(section, ElifInner): ifloop.elifs.append(section)
            elif isinstance(section, ElseInner): ifloop.ifhat_else = section
            else: ifloop.code.append(section)
        return ifloop


with open(Path("resources/parser.lark"), "r") as larkfile:
    parser = Lark(larkfile, parser='lalr')


def parse(string: str) -> Program:
    try:
        tree = parser.parse(string)
    except lark.exceptions.UnexpectedToken as e:
        log_error(str(e))
        exit(1)
    reformatted = Reformatter().transform(tree)
    if not isinstance(reformatted, Program):
        program = Program([], [])
        if isinstance(reformatted, Directive): program.directives.append(reformatted)
        if isinstance(reformatted, ProgramComponent): program.components.append(reformatted)
    else:
        program = reformatted
    return program
