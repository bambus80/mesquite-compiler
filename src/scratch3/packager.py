from queue import Full
from src.parsing.classes import *
from src.scratch3.classes import *
from src.utils import block_id, md5ext


def parse_hat_code(code: list) -> None:
    pass


def add_asset_to_sprite(asset: ScratchAsset) -> None:
    pass


def process_hats(hats: list[Hat]) -> list:
    transpiled = []
    for hat in hats:
        col = BlockColumn()
        if isinstance(hat, OnHat):
            if hat.on_keyword == "green_flag_clicked":
                col.list.append(ScratchBlock(opcode="event_whenflagclicked"))
        for block in hat.code:
            translate_block(block)
        transpiled.append(col.parse())
    return transpiled


def translate_block(block) -> dict:
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


def generate_project(prog: Program) -> ScratchProject:
    project = ScratchProject()

    for component in prog.components:
        if isinstance(component, LibraryComponent):
            pass
        elif isinstance(component, StageComponent):
            target = Stage()
            process_hats(component.hats)
            project.targets.append(target)
        elif isinstance(component, SpriteComponent):
            target = Sprite()
            project.targets.append(target)
        else:
            Exception(f"Unrecognized component: {type(component)}")

    return project