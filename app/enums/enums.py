from enum import Enum


class LogicalOperatorEnum(str, Enum):
    AND = "and"
    OR = "or"


class QueryBuilderTypeEnum(str, Enum):
    NUM = "num"
    STR = "str"
    BOOL = "bool"
    DATE = "date"
    DATETIME = "datetime"
    NULL = "null"


class FilterOperatorEnum(str, Enum):
    EQ = "eq"
    NOT_EQ = "not_eq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    BTW = "btw"
    LIKE = "like"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"


class OrderOperatorEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"


class GameType(Enum):
    DND = "dnd"


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
    AVERAGE = "avg"
    MAX = "max"
    MIN = "min"
    THRESH = "thresh"
    REROLL_ONES = "reroll_ones"


class DiceRegexes(Enum):
    MULTIPLIER = r"\d+x"
    DICE = r"\d+d\d+"
    MODIFIER = r"[\+\-]\d+"
    THRESHOLD = r"t\d+"


class DndAbilities(Enum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"


class DndRollTypes(Enum):
    ATTACK = "attack"
    DAMAGE = "damage"
    CHECK = "check"


class DndSkills(Enum):
    ACROBATICS = "acrobatics"  # dex
    ANIMAL_HANDLING = "animal_handling"  # wis
    ARCANA = "arcana"  # int
    ATHLETICS = "athletics"  # str
    DECEPTION = "deception"  # cha
    HISTORY = "history"  # int
    INSIGHT = "insight"  # wis
    INTIMIDATION = "intimidation"  # cha
    INVESTIGATION = "investigation"  # int
    MEDICINE = "medicine"  # wis
    NATURE = "nature"  # wis
    PERCEPTION = "perception"  # wis
    PERFORMANCE = "performance"  # cha
    PERSUASION = "persuasion"  # cha
    RELIGION = "religion"  # int
    SLEIGHT_OF_HAND = "sleight_of_hand"  # dex
    STEALTH = "stealth"  # dex
    SURVIVAL = "survival"  # wis


class DndWeapons(Enum):
    SIMPLE = "simple"
    MARTIAL = "martial"
    OTHER = "other"


class DndWeaponWeight(Enum):
    HEAVY = "heavy"
    MEDIUM = "medium"
    LIGHT = "light"


class DndTools(Enum):
    ALCHEMIST = "alchemist"
    BREWER = "brewer"
    CALLIGRAPHER = "calligrapher"
    CARPENTER = "carpenter"
    CARTOGRAPHER = "cartographer"
    COBBLER = "cobbler"
    COOK = "cook"
    GLASSBLOWER = "glassblower"
    JEWELER = "jeweler"
    LEATHER = "leatherworker"
    MASON = "mason"
    PAINTER = "painter"
    POTTER = "potter"
    SMITH = "smith"
    TINKER = "tinker"
    WEAVER = "weaver"
    WOODCARVER = "woodcarver"
    DISGUISE = "disguise"
    FORGERY = "forgery"
    DICE = "dice"
    DRAGONCHESS = "dragonchess"
    PLAYING_CARD = "playing_cards"
    THREE_DRAGON = "three-dragon_ante"
    HERBALISM = "herbalism"
    BAGPIPE = "bagpipes"
    DRUM = "drum"
    DULCIMER = "dulcimer"
    FLUTE = "flute"
    LUTE = "lute"
    LYRE = "lyre"
    HORN = "horn"
    PAN_FLUTE = "pan_flute"
    SHAWM = "shawm"
    VIOL = "viol"
    NAVIGATOR = "navigator"
    POISONER = "poisoner"
    THIEF = "thief"
    LAND = "land_vehicles"
    WATER = "water_vehicles"
