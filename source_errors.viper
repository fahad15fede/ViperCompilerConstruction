HOLD

# =========================================================
# VIPER LEXICAL ERROR TEST PROGRAM
# =========================================================

fang age = 20;

# =========================================================
# ERROR 1: ILLEGAL CHARACTER
# @ is not a valid VIPER character
# =========================================================

fang salary = 50000 @ 2;

# =========================================================
# ERROR 2: INVALID IDENTIFIER
# Identifier cannot start with a number
# =========================================================

fang 123student = 20;

# =========================================================
# ERROR 3: NUMBER TOO LONG
# =========================================================

fang hugeNumber = 1234567890123456789012345678901234567890;

# =========================================================
# ERROR 4: UNTERMINATED STRING
# Closing quotation mark is missing
# =========================================================

coil name = "Muhammad Fahad;

# =========================================================
# ERROR 5: UNTERMINATED MULTILINE COMMENT
# Opens with ## but never closes with ##
# =========================================================

##

This is an unterminated multiline comment.

fang hiddenValue = 100;

strike(hiddenValue > 50) {

    hissout("This code is inside the unfinished comment");

}

RELEASE