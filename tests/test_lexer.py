import os
import sys

# Allow importing lexer package when running this file directly
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from lexer.lexer import Lexer


# ---------------------------------------------------------
# FILE READER
# ---------------------------------------------------------

def read_source(filename):

    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    filepath = os.path.join(
        project_root,
        filename
    )

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ---------------------------------------------------------
# PRINT TOKENS
# ---------------------------------------------------------

def print_tokens(tokens):

    print("\nTOKENS")
    print("=" * 80)

    print(
        f"{'TYPE':<20}"
        f"{'LEXEME':<25}"
        f"{'LINE':<8}"
        f"{'COLUMN':<8}"
    )

    print("-" * 80)

    for token in tokens:

        print(
            f"{token.type:<20}"
            f"{token.lexeme:<25}"
            f"{token.line:<8}"
            f"{token.column:<8}"
        )


# ---------------------------------------------------------
# PRINT ERRORS
# ---------------------------------------------------------

def print_errors(errors):

    print("\nERRORS")
    print("=" * 80)

    if not errors:

        print("No lexical errors found.")

        return

    for error in errors:

        print(error)


# ---------------------------------------------------------
# TEST VALID SOURCE
# ---------------------------------------------------------

def test_valid_source():

    print("\n")
    print("#" * 80)
    print("TEST 1: VALID VIPER SOURCE CODE")
    print("#" * 80)

    source = read_source(
        "source_valid.viper"
    )

    lexer = Lexer(source)

    tokens, errors = lexer.tokenize()

    print_tokens(tokens)
    print_errors(errors)

    assert len(errors) == 0, (
        "Valid VIPER source contains lexical errors."
    )

    assert len(tokens) > 0, (
        "No tokens were generated."
    )

    print("\nVALID SOURCE TEST PASSED")


# ---------------------------------------------------------
# TEST ERROR SOURCE
# ---------------------------------------------------------

def test_error_source():

    print("\n")
    print("#" * 80)
    print("TEST 2: VIPER SOURCE WITH LEXICAL ERRORS")
    print("#" * 80)

    source = read_source(
        "source_errors.viper"
    )

    lexer = Lexer(source)

    tokens, errors = lexer.tokenize()

    print_tokens(tokens)
    print_errors(errors)

    assert len(errors) >= 5, (
        "Expected at least 5 lexical errors."
    )

    print(
        f"\nTOTAL LEXICAL ERRORS DETECTED: "
        f"{len(errors)}"
    )

    print("\nERROR SOURCE TEST PASSED")


# ---------------------------------------------------------
# RUN TESTS
# ---------------------------------------------------------

if __name__ == "__main__":

    test_valid_source()
    test_error_source()

    print("\n")
    print("=" * 80)
    print("ALL LEXER TESTS COMPLETED SUCCESSFULLY")
    print("=" * 80)