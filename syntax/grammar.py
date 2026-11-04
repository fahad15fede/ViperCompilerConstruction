# ============================================================
# ============================================================
# VIPER GRAMMAR SETS (used by the recursive descent parser)
# ============================================================
# ============================================================
#
# Terminals are the token TYPES produced by lexer/lexer.py:
#
#   DT            fang | venom | scale | coil | hiss | shed
#   ID            identifier
#   DIGIT         integer literal
#   FLOAT_CONST   float literal
#   CHAR_CONST    character literal
#   STRING_CONST  string literal
#   BOOL_CONST    true | false
#   keywords      HOLD RELEASE strike shift slither coilrun stalk
#                 lurk escape slide nest fangback sense hissout
#   operators     the operator itself, e.g. "+=", "&&", "!"
#   symbols       the symbol itself, e.g. "(", ";", "{"
#   $             end of input (added by the parser)


# ============================================================
# 1. FIRST(<data_type>)
# ============================================================

FIRST_DATA_TYPE = {"DT"}


# ============================================================
# 2. FIRST(<value>)
# ============================================================

FIRST_VALUE = {
    "DIGIT",
    "FLOAT_CONST",
    "CHAR_CONST",
    "STRING_CONST",
    "BOOL_CONST"
}


# ============================================================
# 3. FIRST(<expression>)
# ============================================================

FIRST_EXPRESSION = {"ID", "!", "("} | FIRST_VALUE


# ============================================================
# 4. FIRST(<statement>)
# ============================================================

FIRST_STATEMENT = (
    FIRST_DATA_TYPE
    | FIRST_EXPRESSION
    | {
        "strike",
        "coilrun", "stalk", "lurk",
        "nest",
        "sense", "hissout",
        "fangback",
        "escape",
        "slide"
    }
)


# ============================================================
# 5. FOLLOW SETS (used to choose ε productions)
# ============================================================

FOLLOW_STATEMENTS = {"RELEASE", "}"}

FOLLOW_ASSIGNMENT_TAIL = {")", ",", ";"}

FOLLOW_PARAMETERS = {")"}

FOLLOW_PARAMETER_TAIL = {")"}

FOLLOW_OUTPUT_LIST_TAIL = {")"}


# ============================================================
# 6. OPERATOR GROUPS
# ============================================================

ASSIGN_OPS = {"=", "+=", "-=", "*=", "/="}

EQUALITY_OPS = {"==", "!="}

ORDERING_OPS = {"<", ">", "<=", ">="}

ADD_OPS = {"+", "-"}

MUL_OPS = {"*", "/", "%"}


# ============================================================
# 7. LOOP KEYWORDS
# ============================================================

LOOP_KEYWORDS = {"coilrun", "stalk", "lurk"}

IO_KEYWORDS = {"sense", "hissout"}
