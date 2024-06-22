# Mesquite Compiler
A Python compiler for the Mesquite programming language, designed to compile typed code to Scratch 3 sprites.

### Important
This compiler is not yet functional. There's also no documentation for it as in this stage of development, it would be kinda useless to type one in and the grammar of the language is still in development.

### Usage
`main.py -f /path/to/file.msq`

### Libraries
Stantard libraries are stored in the `/lib` folder. All libraries are in a JSON format and contain two fields, `hats` and `blocks`. Hats are used for events, while blocks are used for regular blocks of code.