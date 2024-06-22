from src.minify import minify
from tokenize_code import tokenize_code
import os
import argparse

if __name__ == "__main__":
    print("Mesquite Compiler 1.0")
    parser = argparse.ArgumentParser(prog='Mesquite Compiler')
    parser.add_argument('-F', '--file', type=str, required=True, default="main.msq")
    args = parser.parse_args()

    file_dir = os.path.join(os.getcwd(), args.file)

    with open(file_dir, 'r') as f:
        print(f"Compiling '{file_dir}'...")
        code = minify(f.read().split('\n'))

        tokenized_output = []
        for line in code:
            tokenized_output = tokenize_code(line, tokens=tokenized_output)["tokens"]
        print(tokenized_output)
        # TODO: Zip and save to .SPRITE3 and print info about the compiled sprite (eg. sprite size)