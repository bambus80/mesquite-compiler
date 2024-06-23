from src.parsing import parse
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
        print(tokenized_output)
        # TODO: Zip and save to .SPRITE3 and print info about the compiled sprite (eg. sprite size)