# VIPER Syntax Analyzer (Recursive Descent)

Phase 2 of the VIPER compiler. It takes the tokens from `lexer/lexer.py` without changing them
and checks them against the final LL(1) VIPER grammar.

## New files
```
syntax/
├── grammar.py   # FIRST / FOLLOW sets and operator groups (uses the lexer's token types)
├── errors.py    # SyntaxAnalysisError (line + column)
└── parser.py    # Parser: one method per non-terminal, production written above each
parser_main.py           # runs Phase 1 (lexer), then Phase 2 (parser)
syntax_valid.viper       # program that uses every grammar rule
syntax_error_cases/      # 10 programs, one syntax error each
tests/test_parser.py
```

## Running
```bash
python parser_main.py syntax_valid.viper            # lexer + parser
python parser_main.py syntax_valid.viper -tree      # also print the parse tree
python parser_main.py syntax_valid.viper -tokens    # also print the token table
python tests/test_parser.py                         # run parser tests
```
If the lexer finds errors, parsing is skipped.

## Grammar terminals = lexer token types
| Grammar        | Token type from lexer                 |
|----------------|---------------------------------------|
| data type      | `DT` (fang, venom, scale, coil, hiss, shed) |
| identifier     | `ID`                                  |
| constants      | `DIGIT`, `FLOAT_CONST`, `CHAR_CONST`, `STRING_CONST`, `BOOL_CONST` |
| NOT            | `!`                                   |
| keywords       | the keyword itself (`strike`, `HOLD`, ...) |
| operators / symbols | the symbol itself (`+=`, `&&`, `;`, ...) |
