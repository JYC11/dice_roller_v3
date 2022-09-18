import sys

from enums.enums import MetaCommands, MetaCommandOutputs


def do_meta_command_output(command: str) -> str:
    command = command.lower()
    if command == MetaCommands.EXIT.value:
        print(MetaCommandOutputs.EXIT.value)
        sys.exit(0)
    elif command == MetaCommands.HELP.value:
        print(MetaCommandOutputs.HELP.value)
        return MetaCommandOutputs.HELP.value
    elif command == MetaCommands.DICE.value:
        print(MetaCommandOutputs.DICE.value)
        return MetaCommandOutputs.DICE.value
    elif command == MetaCommands.PREFIX.value:
        print(MetaCommandOutputs.PREFIX.value)
        return MetaCommandOutputs.PREFIX.value
