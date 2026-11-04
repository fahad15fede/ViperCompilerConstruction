# ============================================================
# ============================================================
# VIPER LANGUAGE DEFINITIONS
# ============================================================
# ============================================================


# ============================================================
# 1. PROGRAM BOUNDARIES
# ============================================================

PROGRAM_BOUNDARIES = {
    "HOLD": "Hold",
    "RELEASE": "Release"
}


# ============================================================
# 2. DATA TYPE KEYWORDS
# ============================================================

DATA_TYPES = {
    "fang": "DT",
    "venom": "DT",
    "scale": "DT",
    "coil": "DT",
    "hiss": "DT",
    "shed": "DT"
}


# ============================================================
# 3. CONTROL / FUNCTION / I/O KEYWORDS
# ============================================================

KEYWORDS = {
    "HOLD": "HOLD",
    "RELEASE": "RELEASE",

    "strike": "Strike",
    "shift": "Shift",
    "slither": "Slither",

    "coilrun": "Coilrun",
    "stalk": "Stalk",
    "lurk": "Lurk",

    "escape": "Escape",
    "slide": "Slide",

    "nest": "Nest",
    "fangback": "Fangback",

    "sense": "Sense",
    "hissout": "Hissout"
}


# ============================================================
# 4. BOOLEAN LITERALS
# ============================================================

BOOLEAN_LITERALS = {
    "true": "True",
    "false": "False"
}


# ============================================================
# 5. ASSIGNMENT OPERATORS
# ============================================================

ASSIGNMENT_OPERATORS = {
    "=": "=",
    "+=": "+=",
    "-=": "-=",
    "*=": "*=",
    "/=": "/="
}


# ============================================================
# 6. ARITHMETIC OPERATORS
# ============================================================

ARITHMETIC_OPERATORS = {
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
    "%": "%"
}


# ============================================================
# 7. RELATIONAL OPERATORS
# ============================================================

RELATIONAL_OPERATORS = {
    "==": "==",
    "!=": "!=",
    "<": "<",
    ">": ">",
    "<=": "<=",
    ">=": ">="
}


# ============================================================
# 8. LOGICAL OPERATORS
# ============================================================

LOGICAL_OPERATORS = {
    "&&": "&&",
    "||": "||",
    "!": "!"
}


# ============================================================
# 9. SPECIAL SYMBOLS
# ============================================================

SPECIAL_SYMBOLS = {
    "(": "(",
    ")": ")",

    "{": "{",
    "}": "}",

    "[": "[",
    "]": "]",

    ";": ";",
    ",": ",",
    ":": ":"
}


# ============================================================
# 10. COMBINED OPERATOR TABLE
# ============================================================

OPERATORS = {
    **ASSIGNMENT_OPERATORS,
    **ARITHMETIC_OPERATORS,
    **RELATIONAL_OPERATORS,
    **LOGICAL_OPERATORS
}

OPERATOR_START_CHARS = set()

for operator in OPERATORS:
    OPERATOR_START_CHARS.add(operator[0])


# ============================================================
# 11. ALL RESERVED WORDS
# ============================================================

RESERVED_WORDS = {}

RESERVED_WORDS.update(PROGRAM_BOUNDARIES)
RESERVED_WORDS.update(DATA_TYPES)
RESERVED_WORDS.update(KEYWORDS)
RESERVED_WORDS.update(BOOLEAN_LITERALS)


# ============================================================
# 12. ALL SPECIAL CHARACTERS
# ============================================================

SPECIAL_CHARACTERS = set(SPECIAL_SYMBOLS.keys())


# ============================================================
# 13. COMMENT DEFINITIONS
# ============================================================

SINGLE_LINE_COMMENT_START = "#"

MULTILINE_COMMENT_START = "##"
MULTILINE_COMMENT_END = "##"


# ============================================================
# 14. LEXICAL LIMITS
# ============================================================

MAX_IDENTIFIER_LENGTH = 16
MAX_NUMBER_LENGTH = 16


# ============================================================
# 15. VALID IDENTIFIER CHARACTERS
# ============================================================

IDENTIFIER_START_CHARS = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "_"
)

IDENTIFIER_CHARS = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "_"
)

# ============================================================
# 16. NUMBER CHARACTERS
# ============================================================

DIGITS = "0123456789"


# ============================================================
# 17. LITERAL DELIMITERS
# ============================================================

STRING_QUOTE = '"'

CHARACTER_QUOTE = "'"