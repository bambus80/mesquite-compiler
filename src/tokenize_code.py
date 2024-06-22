import random
import string


class DefineToken:
    """
    A token containing definitions of blocks or variables.
    The opcode signifies which type is the definition and the name signifies its external name defined by the user.
    """
    def __init__(self, opcode, name, pointer):
        self.opcode = opcode
        self.name = name
        self.pointer = pointer

    def to_dict(self):
        return {
            "opcode": self.opcode,
            "name": self.name,
            "pointer": self.pointer
        }


class Token:
    """
    A token containing a block of code.
    """
    def __init__(self, opcode, input_dict, output):
        self.opcode = opcode
        self.input = input_dict
        self.output = output

    def to_dict(self):
        return {
            "opcode": self.opcode,
            "input": self.input,
            "output": self.output
        }


class MesquiteCompilationError(Exception):
    # TODO: Make the tokenizer throw more accurate compilation errors.
    pass


def generate_random_string(length=18):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def find_segment(line, start_idx):
    brackets = 0
    buf = ""
    i = start_idx
    while i < len(line):
        if line[i] == "{":
            brackets += 1
        elif line[i] == "}":
            brackets -= 1
        buf += line[i]
        i += 1
    return buf, i


def tokenize_code(line):
    global define_tokens
    print(line.split(" "))
    tokens = []
    i = 0
    while i < len(line):
        # TODO: Load libraries with 'use' keyword
        if line[i] == "on":
            """
            On event trigger
            Connects code to Scratch's "Event" hat blocks.
            Syntax: 'on <event_name> {}', where '{}' is the block of code to be attached.
            
            Supported events:
            "green_flag_click", "key_pressed(<key>)", "sprite_clicked", "backdrop_switch(<backdrop name>)",
            "loudness_exceeds(<value>)", "timer_exceeds(<value>)", "receive_broadcast(<broadcast name>)",
            "create_clone"
            """
            with open("../lib/std.json") as f:
                event_opcodes = f.read()["hats"]

            try:
                event_opcode = event_opcodes[line[i + 1]]
            except ValueError:
                raise MesquiteCompilationError("Could not parse event type")
            token_opcode = f"event_{event_opcode}"
            i += 2
            code_block = ""
            while not line[i] == "}":
                code_block += line[i]
                i += 1
            tokens.append(Token(opcode=token_opcode, input_dict={}, output=code_block))
        elif line[i] == "define":
            """
            A definition, may be used for:
            - Variable definition 'define <var|global_var> <name> = <type> <value>'
            - Non-rep. block definition 'define block (<input>) => <name> => {}'
            - Returning block definition 'define block (<input>) => <name> => <output> {}'
            Each definition has a name assigned by the user and a randomly generated pointer.
            """
            define_type = line[i + 1]
            if define_type == "var":
                # TODO: Handle 'define var'
                """
                Define local variable (not accessible outside the sprite)
                Syntax: 'define var <name> = <type> <value>'
                """
                define_tokens.append(DefineToken(opcode="var", name="", pointer=generate_random_string()))
            elif define_type == "global_var":
                # TODO: Handle 'define global_var'
                """
                Define global variable (accessible outside the sprite)
                Syntax: 'define global_var <name> = <type> <value>'
                """
                pass
            elif define_type == "block":
                # TODO: Handle 'define block' 
                pass
        i += 1
    return tokens


if __name__ == "__main__":
    define_tokens = []
    # Example usage
    example_code = [
        "use events;",
        'use "./lib/std.msl";',
        "define block (name) => say_name => text { return join('Hello, ', name, '!'); };",
        'define block (null) => main { define var username = text "Iga"; say(text_message); };',
        "on green_flag_click { main; };"
    ]

    tokenized_output = tokenize_code('on key_pressed("space") { main; }')
    for i in tokenized_output:
        print(i.to_dict())
elif __name__ == "src.tokenize":
    pass
