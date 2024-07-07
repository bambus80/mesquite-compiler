import os.path
from src.parsing import parse
from src.parsing.classes import *
from src.scratch3.classes import *
from src.scratch3.validate import *
from src.utils import block_id, pretty_print_program
from src.asset import serialize_asset
from src.logging import *

project = ScratchProject()

_builtin_funcs = [
    # Category: Motion
    "move",  # move(steps: number) -> null
    "turn_right",  # turn_right(degrees: number) -> null
    "turn_left",  # turn_left(degrees: number) -> null
    # "goto_target,  # goto(t: target) -> null
    "goto",  # goto(x: number, y: number) -> null
    # "glide_to_target",  # glide_to_target(secs: number, t: target) -> null
    "glide_to",  # glide_to(x: number, y: number, secs: number)
    "point",  # point(degrees: number) -> null
    # "point_towards",  # point_towards(t: target) -> null
    "if_on_edge_bounce",
    "rotation_style_left_right",
    "rotation_style_no_rotation",
    "rotation_style_all_around",

    # Category: Looks
    "say",  # say(in: text) -> null
]

builtin_funcs = {
    "move": ScratchBlock(opcode="motion_movesteps")
}


def parse_hat_code(code: list) -> None:
    # TODO: Parse code inside hats
    out: list[ScratchBlock] = []

    for i in code:
        if isinstance(i, VariableDefinition):
            pass
        elif isinstance(i, Function):
            if i.name in builtin_funcs:
                out.append(builtin_funcs[i.name])
            else:
                pass

    pass


def process_hats(hats: list[Hat], project_cwd: str, include_dango: bool = True) -> tuple[list, list]:
    transpiled_blocks: list = []
    transpiled_assets: list = []
    is_costume_added: bool = False

    for hat in hats:
        col = BlockColumn()

        if isinstance(hat, SpriteStatement):  # costume "costume_file" as costume_name
            if isinstance(hat, CostumeStatement):
                is_costume_added = True
            transpiled_assets.append(serialize_asset(hat, project_cwd))

        if isinstance(hat, InitializationHat):  # init {}
            for block in hat.code:
                # TODO: Handle non-code procedures in initialization hat (eg. variable declarations)
                if isinstance(block, Function):
                    log_error("Cannot run function in initialization hat")
                    exit(1)

        if isinstance(hat, OnHat):
            if hat.on_keyword == "green_flag_clicked":  # on green_flag_clicked {}
                col.list.append(ScratchBlock(opcode="event_whenflagclicked"))

            elif hat.on_keyword == "key_pressed":  # on key_pressed("key_name") {}
                if is_valid_key(hat.arguments[0]):
                    col.list.append(ScratchBlock(opcode="event_whenkeypressed",
                                                 fields={"KEY_OPTION": [hat.arguments[0], None]}))
                else:
                    log_error(f"{hat.arguments[0]} is not a valid key.")
                    exit(1)
            elif hat.on_keyword == "sprite_clicked":  # on sprite_clicked {}
                col.list.append(ScratchBlock(opcode="event_whenthisspriteclicked"))
            elif hat.on_keyword == "backdrop_switch_to":  # on backdrop_switch_to {}
                col.list.append(ScratchBlock(opcode="event_whenbackdropswitchesto",
                                             fields={"BACKDROP": [hat.arguments[0], None]}))
            elif hat.on_keyword == "timer_greater_than":  # on timer_greater_than(5) {}
                if hat.arguments[0] >= 0:
                    col.list.append(ScratchBlock(opcode="event_whengreaterthan",
                                                 inputs={"VALUE": [1, [1, hat.arguments[0]]]},
                                                 fields={"WHENGREATERTHANMENU": ["TIMER", None]}))
                else:
                    log_error(f"{hat.arguments[0]} is not a valid timer value (must be 0 or above).")
                    exit(1)
            elif hat.on_keyword == "loudness_greater_than":  # on timer_greater_than(20) {}
                if hat.arguments[0] >= 0:
                    col.list.append(ScratchBlock(opcode="event_whengreaterthan",
                                                 inputs={"VALUE": [1, [1, hat.arguments[0]]]},
                                                 fields={"WHENGREATERTHANMENU": ["LOUDNESS", None]}))
                else:
                    log_error(f"{hat.arguments[0]} is not a valid loudness value (must be 0 or above).")
                    exit(1)
            elif hat.on_keyword == "receive_broadcast":  # on receive_broadcast("brodadcast_name") {}
                # TODO: Look up broadcast ID for "recieve_broadcast" event
                col.list.append(ScratchBlock(opcode="event_whenbroadcastreceived",
                                             fields={"BROADCAST_OPTION": [hat.arguments[0], "TODO"]}))
            elif hat.on_keyword == "clone_created":  # on clone_created {}
                col.list.append(ScratchBlock(opcode="control_start_as_clone"))

            for block in hat.code:
                translate_block(block)
            transpiled_blocks.append(col.parse())

    if not is_costume_added and include_dango:
        transpiled_assets.append(serialize_asset(CostumeStatement(import_from="./resources/dango.svg",
                                                                  import_to="Dango",
                                                                  origin="int")))

    return transpiled_blocks, transpiled_assets


def translate_block(block) -> dict | list:
    # TODO: Include stantard Scratch blocks as Mesquite functions
    if isinstance(block, IfHat):
        pass

    elif isinstance(block, SpriteStatement):
        pass

    elif isinstance(block, FunctionDefinitionHat):
        definition_block_id = block_id()
        prototype_block_id = block_id()
        return [
            ScratchBlock(
                id=definition_block_id,
                opcode="procedures_definition",
                inputs={"custom_block": [1, prototype_block_id]}
                ),
            ScratchMutatedBlock(
                id=prototype_block_id,
                opcode="procedures_prototype",
                mutation={
                    "tagName": "mutation",
                    "children": [],
                    "proccode": block.name,
                    "argumentids": "[]",
                    "argumentnames": "[]",
                    "argumentdefaults": "[]",
                    "warp": "false"
                }
            )
        ]


def parse_directives(prog: Program, project_cwd: str) -> list[Program] | None:
    # For standalone files w/o directives
    if not prog.directives:
        return None

    parsed_directives = []
    for directive in prog.directives:
        if isinstance(directive, UseStatement):
            file_path = os.path.normpath(os.path.join(project_cwd, directive.import_from))
            try:
                with open(file_path, "r") as directive_file:
                    parsed_directives.append(parse(directive_file.read()))
            except OSError:
                log_error(f"Could not access {file_path}")
                exit(1)
        else:
            log_error(f"Unknown directive: {type(directive)}")
            exit(1)

    return parsed_directives


def generate_project(prog: Program, project_cwd: str) -> ScratchProject:
    # TODO: Include code imported via 'use' to the project

    for component in prog.components:
        if isinstance(component, LibraryComponent):
            pass

        elif isinstance(component, (StageComponent, SpriteComponent)):
            if isinstance(component, StageComponent):
                target = Stage()
            else:
                target = Sprite(name=component.sprite)
            transpiled = process_hats(component.hats,
                                      project_cwd,
                                      include_dango=isinstance(component, SpriteComponent))
            target.blocks = transpiled[0]
            for asset in transpiled[1]:
                if isinstance(asset, Costume):
                    target.costumes.append(asset)
                elif isinstance(asset, Sound):
                    target.sounds.append(asset)
            project.targets.append(target)
            pretty_print_program(target)

        else:
            log_error(f"Unrecognized component: {type(component)}")
            exit(1)

    return project
