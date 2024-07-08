from src.scratch3.classes import ScratchBlock, ScratchMutatedBlock, BlockColumn
from src.parsing.classes import Function, FunctionDefinitionHat, FunctionVariableDefinition
from src.logging import log_error


builtin_funcs = {
    # Category: Motions
    # move(steps: number) -> null
    "move": ScratchBlock(opcode="motion_movesteps"),
    # turn_right(degrees: number) -> null
    "turn_right": ScratchBlock(opcode="motion_turnright",
                               inputs={"STEPS": [3, [4, ""]] }),
    # turn_left(degrees: number) -> null
    "turn_left": ScratchBlock(opcode="motion_turnleft",
                              inputs={"STEPS": [3, [4, ""]] }),
    # goto(x: number, y: number) -> null
    "goto": ScratchBlock(opcode="motion_gotoxy",
                         inputs={"X": [3, [4, ""]],
                                 "Y": [3, [4, ""]]
                                 }),
    # glide_to(x: number, y: number, secs: number) -> null
    "glide_to": ScratchBlock(opcode="motion_glidesecstoxy",
                             inputs={"SECS": [3, [4, ""]],
                                     "X": [3, [4, ""]],
                                     "Y": [3, [4, ""]]
                                     }),
    # point(degrees: number) -> null
    "point": ScratchBlock(opcode="motion_pointindirection",
                          inputs={"TOWARDS": [3, [4, ""]] }),


    # Category: Looks
    # say(message: text) -> null
    "say": ScratchBlock(opcode="looks_say",
                        inputs={"MESSAGE": [1, [10, ""]] }),
    # say_for(message: text, secs: number) -> null
    "say_for": ScratchBlock(opcode="looks_sayforsecs",
                            inputs={"MESSAGE": [1, [10, ""]],
                                    "SECS": [1, [4, ""]]
                                    }),
    # think(message: text) -> null
    "think": ScratchBlock(opcode="looks_think",
                          inputs={"MESSAGE": [1, [10, ""]] }),
    # think_for(message: text, secs: number) -> null
    "think_for": ScratchBlock(opcode="looks_thinkforsecs",
                              inputs={"MESSAGE": [1, [10, ""]],
                                      "SECS": [1, [4, ""]]
                                      }),
    # show() -> null
    "show": ScratchBlock(opcode="looks_show"),
    # hide() -> null
    "hide": ScratchBlock(opcode="looks_hide"),
    # layer_front() -> null
    "layer_front": ScratchBlock(opcode="looks_gotofrontback",
                                inputs={"FRONT_BACK": ["front", None]}),
    # layer_back() -> null
    "layer_back": ScratchBlock(opcode="looks_gotofrontback",
                               inputs={"FRONT_BACK": ["back", None]}),
    # layer_move(num: number) -> null
    "layer_move": ScratchBlock(opcode="looks_goforwardbackwardlayers",
                               inputs={"FRONT_BACK": ["", None],
                                       "NUM": [1, [7, ""]]
                                       }),

    # Category: Control
    # wait(secs: number) -> null
    "wait": ScratchBlock(opcode="control_wait",
                         inputs={"DURATION": [1, [5, ""]] }),
    # stop() -> null
    "stop": ScratchMutatedBlock(opcode="control_stop",
                                fields={"STOP_OPTION": ["this script", None]},
                                mutation={"tagName": "mutation",
                                          "children": [],
                                          "hasnext": "false"}),
    # stop_other() -> null
    "stop_other": ScratchMutatedBlock(opcode="control_stop",
                                      fields={"STOP_OPTION": ["other scripts in sprite", None]},
                                      mutation={"tagName": "mutation",
                                                "children": [],
                                                "hasnext": "false"}),
    # stop_all() -> null
    "stop_all": ScratchMutatedBlock(opcode="ocontrol_stop",
                                    fields={"STOP_OPTION": ["all", None]},
                                    mutation={"tagName": "mutation",
                                              "children": [],
                                              "hasnext": "false"}),


    # Category: Sensing
    # ask(question: text) -> null
    "ask": ScratchBlock(opcode="sensing_askandwait",
                        inputs={"QUESTION": [1, [10, ""]] }),
    # set_drag(mode: text["draggable", "not draggable"]) -> null
    "set_drag": ScratchBlock(opcode="sensing_setdragmode",
                             inputs={"DRAG_MODE": [1, [10, ""]]})
}


class FunctionConstructor:
    def __init__(self):
        self.declared_funcs = {}

    def construct(self, func: Function) -> ScratchBlock:
        """
        Returns a block of a declared function.
        :param func: Function
        :return: ScratchBlock
        """
        if func.name in builtin_funcs:
            return builtin_funcs.get(func.name)
        elif func.name in self.declared_funcs:
            pass
        else:
            log_error(f"Function {func.name} is not defined.")
            exit(1)

    def define(self, func: FunctionDefinitionHat) -> tuple[BlockColumn, BlockColumn]:
        # TODO: Define custom functions
        """
        Defines a Mesquite function
        :param func: FunctionDefinitionHat
        :return: tuple[BlockColumn (definition hats), BlockColumn (function code)]
        """
        pass
