import os
import sys

# Allow importing lexer / syntax packages when running this file directly
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from lexer.lexer import Lexer
from syntax.parser import Parser
from syntax.errors import SyntaxAnalysisError


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ---------------------------------------------------------
# FILE READER
# ---------------------------------------------------------

def read_source(filename):

    filepath = os.path.join(
        PROJECT_ROOT,
        filename
    )

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ---------------------------------------------------------
# LEX + PARSE
# Returns None if valid, otherwise the error
# ---------------------------------------------------------

def analyze(source):

    tokens, lexical_errors = Lexer(source).tokenize()

    assert len(lexical_errors) == 0, (
        f"Unexpected lexical errors: {lexical_errors}"
    )

    try:

        Parser(tokens).parse()

        return None

    except SyntaxAnalysisError as error:

        return error


# ---------------------------------------------------------
# TEST VALID SOURCE
# ---------------------------------------------------------

def test_valid_source():

    print("\n")
    print("#" * 80)
    print("TEST 1: SYNTACTICALLY VALID VIPER SOURCE")
    print("#" * 80)

    error = analyze(
        read_source("syntax_valid.viper")
    )

    assert error is None, (
        f"Valid VIPER source was rejected: {error}"
    )

    print("syntax_valid.viper -> accepted")

    print("\nVALID SOURCE TEST PASSED")


# ---------------------------------------------------------
# TEST ERROR SOURCES
# Every file in syntax_error_cases/ must be rejected
# ---------------------------------------------------------

def test_error_sources():

    print("\n")
    print("#" * 80)
    print("TEST 2: VIPER SOURCES WITH SYNTAX ERRORS")
    print("#" * 80)

    folder = os.path.join(
        PROJECT_ROOT,
        "syntax_error_cases"
    )

    files = sorted(
        name for name in os.listdir(folder)
        if name.endswith(".viper")
    )

    assert len(files) > 0, (
        "No syntax error test files found."
    )

    for name in files:

        error = analyze(
            read_source(
                os.path.join("syntax_error_cases", name)
            )
        )

        assert error is not None, (
            f"{name} should have a syntax error but was accepted."
        )

        print(f"{name:<40} -> {error}")

    print(
        f"\nTOTAL SYNTAX ERROR FILES DETECTED: "
        f"{len(files)}"
    )

    print("\nERROR SOURCE TEST PASSED")


# ---------------------------------------------------------
# RUN TESTS
# ---------------------------------------------------------

if __name__ == "__main__":

    sys.setrecursionlimit(10000)

    test_valid_source()
    test_error_sources()

    print("\n")
    print("=" * 80)
    print("ALL PARSER TESTS COMPLETED SUCCESSFULLY")
    print("=" * 80)
