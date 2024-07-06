import os.path

from src.parsing import parse
from src.parsing.classes import *
from src.scratch3.classes import *
from src.scratch3.validate import *
from src.utils import block_id
from src.asset import serialize_asset
from src.logging import *


def parse_hat_code(code: list) -> None:
    pass


def process_hats(hats: list[Hat], project_cwd: str) -> list:
    transpiled = []
    for hat in hats:
        col = BlockColumn()

        if isinstance(hat, SpriteStatement):
            serialize_asset(hat, project_cwd)

        if isinstance(hat, InitializationHat):
            for block in hat.code:
                if isinstance(block, Function):
                    log_error("Cannot run function in initialization hat")
                    exit(1)

        if isinstance(hat, OnHat):
            # Create hats for on events
            if hat.on_keyword == "green_flag_clicked":
                col.list.append(ScratchBlock(opcode="event_whenflagclicked"))

            elif hat.on_keyword == "key_pressed":
                if is_valid_key(hat.arguments[0]):
                    col.list.append(ScratchBlock(opcode="event_whenkeypressed",
                                                 fields={"KEY_OPTION": [hat.arguments[0], None]}))
                else:
                    log_error(f"{hat.arguments[0]} is not a valid key.")
                    exit(1)

            elif hat.on_keyword == "sprite_clicked":
                col.list.append(ScratchBlock(opcode="event_whenthisspriteclicked"))

            elif hat.on_keyword == "backdrop_switch_to":
                col.list.append(ScratchBlock(opcode="event_whenbackdropswitchesto",
                                             fields={"BACKDROP": [hat.arguments[0], None]}))

            elif hat.on_keyword == "timer_greater_than":
                if hat.arguments[0] >= 0:
                    col.list.append(ScratchBlock(opcode="event_whengreaterthan",
                                                 inputs={"VALUE": [1, [1, hat.arguments[0]]]},
                                                 fields={"WHENGREATERTHANMENU": ["TIMER", None]}))
                else:
                    log_error(f"{hat.arguments[0]} is not a valid timer value (must be 0 or above).")
                    exit(1)

            elif hat.on_keyword == "loudness_greater_than":
                if hat.arguments[0] >= 0:
                    col.list.append(ScratchBlock(opcode="event_whengreaterthan",
                                                 inputs={"VALUE": [1, [1, hat.arguments[0]]]},
                                                 fields={"WHENGREATERTHANMENU": ["LOUDNESS", None]}))
                else:
                    log_error(f"{hat.arguments[0]} is not a valid loudness value (must be 0 or above).")
                    exit(1)

            elif hat.on_keyword == "receive_broadcast":
                # TODO: Look up broadcast ID for "recieve_broadcast" event
                col.list.append(ScratchBlock(opcode="event_whenbroadcastreceived",
                                             fields={"BROADCAST_OPTION": [hat.arguments[0], "TODO"]}))

            elif hat.on_keyword == "clone_created":
                col.list.append(ScratchBlock(opcode="control_start_as_clone"))

            for block in hat.code:
                translate_block(block)
            transpiled.append(col.parse())

    return transpiled


def translate_block(block) -> dict | list:
    if isinstance(block, IfHat):
        pass

    elif isinstance(block, SpriteStatement):
        pass

    elif isinstance(block, FunctionDefinitionHat):
        definition_block_id = block_id
        prototype_block_id = block_id
        return [
            ScratchBlock(
                definition_block_id, 
                "procedures_definition",
                inputs={"custom_block": [1, prototype_block_id]}
                ),
            ScratchMutatedBlock(
                prototype_block_id,
                "procedures_prototype",
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
            except FileNotFoundError:
                log_error(f"Could not access {file_path}")
                exit(1)
        else:
            log_error(f"Unknown directive: {type(directive)}")
            exit(1)

    return parsed_directives


def generate_project(prog: Program, project_cwd: str) -> ScratchProject:
    project = ScratchProject()

    for component in prog.components:
        if isinstance(component, LibraryComponent):
            pass

        elif isinstance(component, StageComponent):
            target = Stage()
            target.blocks = process_hats(component.hats, project_cwd)
            project.targets.append(target)

        elif isinstance(component, SpriteComponent):
            target = Sprite(name=component.sprite)
            target.blocks = process_hats(component.hats, project_cwd)
            project.targets.append(target)

        else:
            log_error(f"Unrecognized component: {type(component)}")
            exit(1)

    return project
