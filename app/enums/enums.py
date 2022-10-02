from enum import Enum


class CompileValidationResults(Enum):
    COMPILE_POSSIBLE = "compile_possible"
    COMPILE_IMPOSSIBLE = "compile_impossible"


class MetaCommands(Enum):
    EXIT = ".exit"
    HELP = ".help"
    DICE = ".dice"
    PREFIX = ".prefix"


class MetaCommandOutputs(Enum):
    EXIT = """
        Exiting script
        """
    HELP = """
        '.help' for how to
        '.dice' for dice roll syntax
        '.prefix' for possible prefixes
        '.exit' to exit
        """
    DICE = """
        example 1: 3x2d6+5
        roll 2d6 dices with a +5 modifier 3 times

        example 2: 1d20-2
        roll a d20 dice with a -2 modifier 1 times
        """
    PREFIX = """
        can be both upper and lowercase
        get = get an existing character
        upsert = create a new character or update a character
        del = delete a character
        adv = advantage
        dadv = disadvantage
        dropmax = drops max from a number of rolls
        dropmin = drops min from a number of rolls
        getmax = gets maximum possible value
        getmin = gets minimum possible value
        average = rolls using average values
        max = gets maximum of the rolls
        min = get minimum of the rolls
        """


class Commands(Enum):
    GET = "get"
    UPSERT = "upsert"
    DELETE = "del"
    ADVANTAGE = "adv"
    DISADVANTAGE = "dadv"
    DROPMIN = "dropmin"
    DROPMAX = "dropmax"
    GETMIN = "getmin"
    GETMAX = "getmax"
    AVERAGE = "avg"
    MAX = "max"
    MIN = "min"
    THRESH = "thresh"


class AverageRolls(Enum):
    HUNDREAD = 50.5
    TWENTY = 10.5
    TWELVE = 6.5
    EIGHT = 4.5
    SIX = 3.5
    FOUR = 2.5


class DiceRegexes(Enum):
    MULTIPLIER = r"\d+x"
    DICE = r"\d+d\d+"
    MODIFIER = r"[\+\-]\d+"
