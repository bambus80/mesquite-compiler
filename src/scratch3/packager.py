from dataclasses import asdict
from queue import Full
from src.parsing.classes import *
from src.scratch3.classes import *
from src.utils import block_id, md5ext


def process_hats(hats: list[Hat]):
    transpiled = []
    for hat in hats:
        if isinstance(hat, OnHat):
            if hat.on_keyword == "green_flag_clicked":
                transpiled.append(ScratchBlock(block_id, "event_whenflagclicked"))


def translate_block(block) -> dict:
    if type(block) == IfHat:
        pass
    if type(block) == FunctionDefinitionHat:
        definition_block_id = block_id
        prototype_block_id = block_id
        return {
            definition_block_id: ScratchBlock(
                "procedures_definition",
                inputs={"custom_block": [1, prototype_block_id]}
                ),
            prototype_block_id: ScratchPrototypeBlock(
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
                ),
            }


def generate_project(prog: Program) -> ScratchProject:
    project = ScratchProject()

    for component in prog.components:
        if isinstance(component, LibraryComponent):
            pass
        elif isinstance(component, StageComponent):
            target = ScratchTarget(True, "Stage")
            process_hats(component.hats)
            project.targets.append(target)
        elif isinstance(component, SpriteComponent):
            target = ScratchTarget(False, component.sprite)
            project.targets.append(target)
        else:
            Exception(f"Unrecognized component: {type(component)}")

    return project