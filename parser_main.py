import sys
import os

from lexer.lexer import Lexer
from syntax.parser import Parser
from syntax.errors import SyntaxAnalysisError


# ---------------------------------------------------------
# READ SOURCE FILE
# ---------------------------------------------------------

def read_source(filename):

    project_root = os.path.dirname(
        os.path.abspath(__file__)
    )

    filepath = os.path.join(
        project_root,
        filename
    )

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except FileNotFoundError:

        print(f"Error: File '{filename}' not found.")
        sys.exit(1)


# ---------------------------------------------------------
# PRINT TOKENS
# ---------------------------------------------------------

def print_tokens(tokens):

    print("\n" + "=" * 80)
    print("TOKENS")
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
# PHASE 1: LEXICAL ANALYSIS
# ---------------------------------------------------------

def run_lexer(source, show_tokens):

    print("\n" + "=" * 80)
    print("PHASE 1: LEXICAL ANALYSIS")
    print("=" * 80)

    lexer = Lexer(source)

    tokens, errors = lexer.tokenize()

    if show_tokens:
        print_tokens(tokens)

    if errors:

        for error in errors:
            print(error)

        print(
            f"\nLEXICAL ANALYSIS FAILED WITH "
            f"{len(errors)} ERROR(S)."
        )

        return tokens, False

    print(
        f"No lexical errors found. "
        f"{len(tokens)} tokens generated."
    )

    return tokens, True


# ---------------------------------------------------------
# PHASE 2: SYNTAX ANALYSIS
# ---------------------------------------------------------

def run_parser(tokens, show_tree):

    print("\n" + "=" * 80)
    print("PHASE 2: SYNTAX ANALYSIS (RECURSIVE DESCENT)")
    print("=" * 80)

    parser = Parser(tokens, trace=show_tree)

    try:

        parser.parse()

        if show_tree:

            print("\nPARSE TREE")
            print("-" * 80)

            for line in parser.trace_lines:
                print(line)

            print("-" * 80)

        print("No syntax errors found.")

        return True

    except SyntaxAnalysisError as error:

        print(error)

        return False


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    # -----------------------------------------------------
    # Check command-line arguments
    # -----------------------------------------------------

    args = sys.argv[1:]

    show_tokens = "-tokens" in args
    show_tree = "-tree" in args

    files = [
        arg for arg in args
        if not arg.startswith("-")
    ]

    if len(files) != 1:

        print("\nUsage:")
        print("python parser_main.py <source_file> [-tokens] [-tree]")

        print("\nExamples:")
        print("python parser_main.py syntax_valid.viper")
        print("python parser_main.py syntax_valid.viper -tree")
        print("python parser_main.py syntax_errors.viper")

        sys.exit(1)

    filename = files[0]

    # -----------------------------------------------------
    # Read source
    # -----------------------------------------------------

    source = read_source(filename)

    print("\n" + "#" * 80)
    print("VIPER SYNTAX ANALYZER")
    print("#" * 80)

    print(f"\nSource File: {filename}")
    print(f"Source Length: {len(source)} characters")

    # -----------------------------------------------------
    # Phase 1 -> Phase 2
    # -----------------------------------------------------

    tokens, lexer_ok = run_lexer(source, show_tokens)

    if not lexer_ok:

        print("\n" + "=" * 80)
        print("SYNTAX ANALYSIS SKIPPED: FIX LEXICAL ERRORS FIRST.")
        print("=" * 80)

        sys.exit(1)

    parser_ok = run_parser(tokens, show_tree)

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    print("\n" + "=" * 80)

    if parser_ok:
        print("PARSING SUCCESSFUL: PROGRAM IS SYNTACTICALLY CORRECT.")
    else:
        print("PARSING FAILED: PROGRAM HAS A SYNTAX ERROR.")

    print("=" * 80)

    sys.exit(0 if parser_ok else 1)


# ---------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":

    sys.setrecursionlimit(10000)

    main()
