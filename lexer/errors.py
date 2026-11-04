class LexicalError(Exception):
    """Base class for all VIPER lexical errors."""

    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column

        super().__init__(message)

    def __str__(self):
        return (
            f"Lexical Error at line {self.line}, "
            f"column {self.column}: {self.message}"
        )


class IllegalCharacterError(LexicalError):
    """Raised when a character is not part of the VIPER language."""

    def __init__(self, character, line, column):
        message = f"Illegal character '{character}'"
        super().__init__(message, line, column)


class InvalidIdentifierError(LexicalError):
    """Raised when an identifier violates VIPER identifier rules."""

    def __init__(self, identifier, line, column):
        message = f"Invalid identifier '{identifier}'"
        super().__init__(message, line, column)


class UnterminatedStringError(LexicalError):
    """Raised when a string does not have a closing double quote."""

    def __init__(self, lexeme, line, column):
        message = "Unterminated string literal"
        super().__init__(message, line, column)


class UnterminatedMultilineCommentError(LexicalError):
    """Raised when a multiline comment does not have a closing delimiter."""

    def __init__(self, line, column):
        message = "Unterminated multiline comment"
        super().__init__(message, line, column)


class NumberTooLongError(LexicalError):
    """Raised when a numeric literal exceeds the allowed length."""

    def __init__(self, number, line, column):
        message = f"Number exceeds maximum length: '{number}'"
        super().__init__(message, line, column)


class IdentifierTooLongError(LexicalError):
    """Raised when an identifier exceeds the allowed length."""

    def __init__(self, identifier, line, column):
        message = f"Identifier exceeds maximum length: '{identifier}'"
        super().__init__(message, line, column)