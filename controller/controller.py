import sys
from compiler import compiler


def repl():
    while True:
        user_input: str = input("dice-roller > ")

        if user_input.startswith("."):
            if user_input == ".exit":
                sys.exit(0)
        elif not user_input.startswith("."):
            commands = compiler.compile_raw_user_input(user_input)
            print(commands)
        else:
            print("incorrect command")