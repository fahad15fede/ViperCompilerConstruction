from .tokens import Token
from .errors import (
    LexicalError,
    IllegalCharacterError,
    InvalidIdentifierError,
    UnterminatedStringError,
    NumberTooLongError,
    IdentifierTooLongError
)

from .definitions import (
    KEYWORDS,
    DATA_TYPES,
    RESERVED_WORDS,
    DIGITS,
    IDENTIFIER_START_CHARS,
    IDENTIFIER_CHARS,
    SPECIAL_SYMBOLS,
    OPERATORS,
    MAX_NUMBER_LENGTH,
    MAX_IDENTIFIER_LENGTH,
    STRING_QUOTE,
    CHARACTER_QUOTE
)


class Lexer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

        self.tokens = []
        self.errors = []

        # Characters that can begin an operator.
        # This is important for operators such as && and ||.
        self.operator_start_chars = set()

        for operator in OPERATORS:
            self.operator_start_chars.add(operator[0])

    # ---------------------------------------------------------
    # BASIC CHARACTER FUNCTIONS
    # ---------------------------------------------------------

    def is_at_end(self):
        return self.position >= len(self.source)

    def current_char(self):
        if self.is_at_end():
            return "\0"

        return self.source[self.position]

    def peek(self):
        if self.position + 1 >= len(self.source):
            return "\0"

        return self.source[self.position + 1]

    def advance(self):
        if self.is_at_end():
            return

        char = self.source[self.position]

        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

    # ---------------------------------------------------------
    # TOKEN MANAGEMENT
    # ---------------------------------------------------------

    def add_token(self, token_type, lexeme, line, column):
        token = Token(
            token_type,
            lexeme,
            line,
            column
        )

        self.tokens.append(token)

    # ---------------------------------------------------------
    # WHITESPACE
    # ---------------------------------------------------------

    def skip_whitespace(self):

        while not self.is_at_end():

            if self.current_char() in " \t\r\n":
                self.advance()

            else:
                break

    # ---------------------------------------------------------
    # WORD / IDENTIFIER / KEYWORD
    # ---------------------------------------------------------

    def read_word(self):

        start_line = self.line
        start_column = self.column
        start_position = self.position

        while (
            not self.is_at_end()
            and self.current_char() in IDENTIFIER_CHARS
        ):
            self.advance()

        lexeme = self.source[start_position:self.position]

        # Check identifier length
        if len(lexeme) > MAX_IDENTIFIER_LENGTH:

            self.errors.append(
                IdentifierTooLongError(
                    lexeme,
                    start_line,
                    start_column
                )
            )

            return

        # Keyword
        if lexeme in KEYWORDS:

            self.add_token(
                lexeme,
                lexeme,
                start_line,
                start_column
            )

        # Data type
        elif lexeme in DATA_TYPES:

            self.add_token(
                "DT",
                lexeme,
                start_line,
                start_column
            )

        # Boolean constants
        elif lexeme == "true" or lexeme == "false":

            self.add_token(
                "BOOL_CONST",
                lexeme,
                start_line,
                start_column
            )

        # Normal identifier
        else:

            if lexeme in RESERVED_WORDS:

                self.errors.append(
                    InvalidIdentifierError(
                        lexeme,
                        start_line,
                        start_column
                    )
                )

            else:

                self.add_token(
                    "ID",
                    lexeme,
                    start_line,
                    start_column
                )

    # ---------------------------------------------------------
    # NUMBER / FLOAT
    # ---------------------------------------------------------

    def read_number(self):

        start_line = self.line
        start_column = self.column
        start_position = self.position

        # Read integer part
        while (
            not self.is_at_end()
            and self.current_char() in DIGITS
        ):
            self.advance()

        # Example:
        # 123age
        # 20student
        #
        # A number immediately followed by identifier
        # characters is an invalid identifier.

        if (
            not self.is_at_end()
            and self.current_char() in IDENTIFIER_START_CHARS
        ):

            while (
                not self.is_at_end()
                and self.current_char() in IDENTIFIER_CHARS
            ):
                self.advance()

            lexeme = self.source[
                start_position:self.position
            ]

            self.errors.append(
                InvalidIdentifierError(
                    lexeme,
                    start_line,
                    start_column
                )
            )

            return

        # Float
        if self.current_char() == ".":

            self.advance()

            # 19. is invalid
            if (
                self.is_at_end()
                or self.current_char() not in DIGITS
            ):

                lexeme = self.source[
                    start_position:self.position
                ]

                self.errors.append(
                    LexicalError(
                        f"Invalid float literal: '{lexeme}'",
                        start_line,
                        start_column
                    )
                )

                return

            while (
                not self.is_at_end()
                and self.current_char() in DIGITS
            ):
                self.advance()

            token_type = "FLOAT_CONST"

        else:

            token_type = "DIGIT"

        lexeme = self.source[
            start_position:self.position
        ]

        # Number too long
        if len(lexeme) > MAX_NUMBER_LENGTH:

            self.errors.append(
                NumberTooLongError(
                    lexeme,
                    start_line,
                    start_column
                )
            )

            return

        self.add_token(
            token_type,
            lexeme,
            start_line,
            start_column
        )

    # ---------------------------------------------------------
    # STRING
    # ---------------------------------------------------------

    def read_string(self):
        start_line = self.line
        start_column = self.column

        # Skip opening quote
        self.advance()

        start_position = self.position

        while not self.is_at_end():

            # Closing quote found
            if self.current_char() == '"':
                lexeme = self.source[start_position:self.position]

                self.advance()

                self.add_token(
                    "STRING_CONST",
                    lexeme,
                    start_line,
                    start_column
                )
                return

            # Newline means string was not closed
            if self.current_char() == "\n":
                lexeme = self.source[start_position:self.position]

                self.errors.append(
                    UnterminatedStringError(
                        lexeme,
                        self.line,
                        start_column
                    )
                )
                return

            self.advance()

        # End of file reached without closing quote
        lexeme = self.source[start_position:self.position]

        self.errors.append(
            UnterminatedStringError(
                lexeme,
                self.line,
                start_column
            )
        )

    # ---------------------------------------------------------
    # CHARACTER
    # ---------------------------------------------------------

    def read_character(self):

        start_line = self.line
        start_column = self.column

        # Skip opening '
        self.advance()

        start_position = self.position

        # Empty / unterminated character
        if self.is_at_end():

            self.errors.append(
                LexicalError(
                    "Unterminated character literal",
                    start_line,
                    start_column
                )
            )

            return

        if self.current_char() == "\n":

            self.errors.append(
                LexicalError(
                    "Unterminated character literal",
                    start_line,
                    start_column
                )
            )

            return

        # Read character
        self.advance()

        # Character must end with '
        if self.current_char() != CHARACTER_QUOTE:

            while (
                not self.is_at_end()
                and self.current_char() != CHARACTER_QUOTE
                and self.current_char() != "\n"
            ):
                self.advance()

            if (
                not self.is_at_end()
                and self.current_char() == CHARACTER_QUOTE
            ):
                self.advance()

            lexeme = self.source[
                start_position:self.position - 1
            ]

            self.errors.append(
                LexicalError(
                    f"Invalid character literal: '{lexeme}'",
                    start_line,
                    start_column
                )
            )

            return

        lexeme = self.source[
            start_position:self.position
        ]

        self.advance()

        self.add_token(
            "CHAR_CONST",
            lexeme,
            start_line,
            start_column
        )

    # ---------------------------------------------------------
    # OPERATORS
    # ---------------------------------------------------------

    def read_operator(self):

        start_line = self.line
        start_column = self.column

        # First check two-character operators.
        # This prevents:
        #
        # >=
        #
        # from becoming:
        #
        # > =
        #

        two_char = (
            self.current_char()
            + self.peek()
        )

        if two_char in OPERATORS:

            self.advance()
            self.advance()

            self.add_token(
                two_char,
                two_char,
                start_line,
                start_column
            )

            return

        # Single-character operator
        char = self.current_char()

        if char in OPERATORS:

            self.advance()

            self.add_token(
                char,
                char,
                start_line,
                start_column
            )

            return

        # Should normally never reach here
        self.errors.append(
            IllegalCharacterError(
                char,
                start_line,
                start_column
            )
        )

        self.advance()

    # ---------------------------------------------------------
    # SPECIAL SYMBOLS
    # ---------------------------------------------------------

    def read_symbol(self):

        start_line = self.line
        start_column = self.column

        char = self.current_char()

        if char in SPECIAL_SYMBOLS:

            self.advance()

            self.add_token(
                char,
                char,
                start_line,
                start_column
            )

    # ---------------------------------------------------------
    # COMMENTS
    # ---------------------------------------------------------

    def read_comment(self):

        start_line = self.line
        start_column = self.column

        # Multiline comment:
        #
        # ##
        #     anything
        # ##
        #
        # Check for ## the same way we check && or ||

        if self.peek() == "#":

            # Skip opening ##
            self.advance()
            self.advance()

            while not self.is_at_end():

                if (
                    self.current_char() == "#"
                    and self.peek() == "#"
                ):

                    # Skip closing ##
                    self.advance()
                    self.advance()

                    return

                self.advance()

            self.errors.append(
                LexicalError(
                    "Unterminated multiline comment",
                    start_line,
                    start_column
                )
            )

            return

        # Single-line comment
        while (
            not self.is_at_end()
            and self.current_char() != "\n"
        ):
            self.advance()

    # ---------------------------------------------------------
    # MAIN TOKENIZER
    # ---------------------------------------------------------

    def tokenize(self):

        while not self.is_at_end():

            self.skip_whitespace()

            if self.is_at_end():
                break

            char = self.current_char()

            # Comments
            if char == "#":

                self.read_comment()

            # Identifier / keyword
            elif char in IDENTIFIER_START_CHARS:

                self.read_word()

            # Number
            elif char in DIGITS:

                self.read_number()

            # String
            elif char == STRING_QUOTE:

                self.read_string()

            # Character
            elif char == CHARACTER_QUOTE:

                self.read_character()

            # Operator
            elif char in self.operator_start_chars:

                self.read_operator()

            # Special symbol
            elif char in SPECIAL_SYMBOLS:

                self.read_symbol()

            # Illegal character
            else:

                self.errors.append(
                    IllegalCharacterError(
                        char,
                        self.line,
                        self.column
                    )
                )

                self.advance()

        return self.tokens, self.errors