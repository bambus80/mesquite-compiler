from src.parsing import parse
from src.logging import *
from src.scratch3.packager import generate_project
from json import JSONEncoder
import os
import argparse

from src.utils import pretty_print_program

VERSION = "0.0.2"

# TODO: Include tests !!!
if __name__ == "__main__":
    print(f"\x1b[40;36m ━━━━━━ Mesquite Compiler version {VERSION} ━━━━━━")
    parser = argparse.ArgumentParser(prog='mesquite')
    # TODO: Add support for compiling standalone Scratch sprites
    parser.add_argument('-i', '--input', type=str, required=False, default="./main.msq")
    parser.add_argument('-o', '--output', type=str, required=False, default="./main.sb3")
    parser.add_argument('-w', '--warnings', type=str, required=False, default="medium")
    args = parser.parse_args()

    input_dir = os.path.normpath(os.path.join(os.getcwd(), args.input))

    project_cwd, _ = os.path.split(os.path.abspath(input_dir))

    with open(input_dir, 'r') as f:
        print(f"\x1b[40;36m {input_dir} \x1b[0;36m🭞🭜🭘\x1b[0m\nTokenizing...")
        log_info("Parsing entry file")
        tree = parse(f.read())
        # pretty_print_program(tree)

    log_info("Transpiling entry file")
    project = generate_project(tree, project_cwd)

    with open("./build/project.json", "w") as project_json:
        project_json.write(JSONEncoder().encode(project.serialize()))
        # TODO: Zip and save to .SPRITE3 and print info about the compiled sprite (eg. sprite size)
