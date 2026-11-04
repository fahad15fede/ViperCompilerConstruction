import sys
import os

from lexer.lexer import Lexer


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
# PRINT ERRORS
# ---------------------------------------------------------

def print_errors(errors):

    print("\n" + "=" * 80)
    print("LEXICAL ERRORS")
    print("=" * 80)

    if not errors:

        print("No lexical errors found.")

        return

    for error in errors:

        print(error)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    # -----------------------------------------------------
    # Check command-line argument
    # -----------------------------------------------------

    if len(sys.argv) != 2:

        print(
            "\nUsage:"
        )

        print(
            "python main.py <source_file>"
        )

        print(
            "\nExamples:"
        )

        print(
            "python main.py source_valid.viper"
        )

        print(
            "python main.py source_errors.viper"
        )

        sys.exit(1)

    filename = sys.argv[1]

    # -----------------------------------------------------
    # Read source
    # -----------------------------------------------------

    source = read_source(filename)

    # -----------------------------------------------------
    # Display source information
    # -----------------------------------------------------

    print("\n" + "#" * 80)
    print("VIPER LEXICAL ANALYZER")
    print("#" * 80)

    print(f"\nSource File: {filename}")
    print(f"Source Length: {len(source)} characters")

    # -----------------------------------------------------
    # Create lexer
    # -----------------------------------------------------

    lexer = Lexer(source)

    # -----------------------------------------------------
    # Tokenize source
    # -----------------------------------------------------

    tokens, errors = lexer.tokenize()

    # -----------------------------------------------------
    # Display results
    # -----------------------------------------------------

    print_tokens(tokens)

    print_errors(errors)

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    print("\n" + "=" * 80)

    if errors:

        print(
            f"LEXICAL ANALYSIS COMPLETED "
            f"WITH {len(errors)} ERROR(S)."
        )

    else:

        print(
            "LEXICAL ANALYSIS COMPLETED SUCCESSFULLY."
        )

    print("=" * 80)


# ---------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()