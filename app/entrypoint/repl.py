import sys
from app.enums import Commands, CompileValidationResults
from app.compiler import compiler


def repl():
    while True:
        user_input: str = input("dice-roller > ")

        if user_input.startswith("."):
            if user_input == ".exit":
                sys.exit(0)
        elif not user_input.startswith("."):
            split_user_input = {*user_input.lower().split(" ")}
            crud_commands = {
                Commands.UPSERT.value,
                Commands.GET.value,
                Commands.DELETE.value,
            }
            dice_validator = compiler.validator(user_input)
            if len(split_user_input.intersection(crud_commands)) > 0:
                print("not implemented yet lol")
            if dice_validator == CompileValidationResults.COMPILE_POSSIBLE.value:
                commands = compiler.compile_raw_user_input(user_input)
                print(commands)
            else:
                print("unrecognized command")
