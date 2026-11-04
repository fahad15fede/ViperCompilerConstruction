class SyntaxAnalysisError(Exception):
    """Raised when the token stream does not follow the VIPER grammar."""

    def __init__(self, expected, token):
        self.expected = expected
        self.token = token
        self.line = token.line
        self.column = token.column

        if token.type == "$":
            found = "reached end of file"
        else:
            found = f"found '{token.lexeme}'"

        self.message = f"Expected {expected} but {found}"

        super().__init__(self.message)

    def __str__(self):
        return (
            f"Syntax Error at line {self.line}, "
            f"column {self.column}: {self.message}"
        )
