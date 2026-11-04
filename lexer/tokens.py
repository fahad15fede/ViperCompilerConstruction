from dataclasses import dataclass


@dataclass
class Token:
    type: str
    lexeme: str
    line: int
    column: int

    def __str__(self):
        return (
            f"{self.type:<15}"
            f"{self.lexeme:<20}"
            f"Line: {self.line:<4}"
            f"Column: {self.column}"
        )
