from src.parsing import parse
from src.transpiling import generate_project
import os
import argparse

from src.utils import pretty_print_program

VERSION = "0.0.1a2"

if __name__ == "__main__":
    print(f"\x1b[40;36m ━━━━━━ Mesquite Compiler version {VERSION} ━━━━━━")
    parser = argparse.ArgumentParser(prog='mesquite')
    parser.add_argument('-i', '--input', type=str, required=True, default="main.msq")
    parser.add_argument('-o', '--output', type=str, required=False, default="main.sb3")
    args = parser.parse_args()

    input_dir = os.path.join(os.getcwd(), args.input)

    with open(input_dir, 'r') as f:
        print(f"\x1b[40;36m {input_dir} \x1b[0;36m🭞🭜🭘\x1b[0m Tokenizing...")
        tree = parse(f.read())
        pretty_print_program(tree)
        # print("Transpiling...")
        # project = generate_project(tree)
        # pretty_print_program(project)
        # TODO: Zip and save to .SPRITE3 and print info about the compiled sprite (eg. sprite size)