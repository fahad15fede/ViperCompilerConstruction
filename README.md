# VIPER

VIPER is a custom programming language with snake-themed keywords, together with the front end of its compiler, written in Python.
The project currently covers the first two compiler phases:

| Phase | Component | Input → Output | Status |
|-------|-----------|----------------|--------|
| 1 | **Lexical Analyzer** (`lexer/`) | source text → tokens | Done |
| 2 | **Syntax Analyzer**, a recursive descent parser (`syntax/`) | tokens → parse tree / syntax errors | Done |
| 3 | Semantic Analyzer (types, scopes, symbol table) | parse tree → checked program | Planned |

---

## Table of Contents

1. [Requirements](#requirements)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Language Overview](#language-overview)
5. [Phase 1: Lexical Analyzer](#phase-1-lexical-analyzer)
6. [Phase 2: Syntax Analyzer](#phase-2-syntax-analyzer)
7. [Grammar (LL(1) CFG)](#grammar-ll1-cfg)
8. [Testing](#testing)
9. [Known Limitations](#known-limitations)
10. [Roadmap](#roadmap)

---

## Requirements

- Python **3.8 or newer**
- No external libraries

> On Windows, use `py` if `python` is not recognised. On Mac or Linux, use `python3`.

---

## Quick Start

Run every command from the project root (the folder that contains `main.py`).

```bash
# Phase 1 only: print the token table and any lexical errors
python main.py source_valid.viper

# Phase 1 + Phase 2: lex, then parse
python parser_main.py syntax_valid.viper

# Also print the token table and/or the parse tree
python parser_main.py syntax_valid.viper -tokens
python parser_main.py syntax_valid.viper -tree

# Run the tests
python tests/test_lexer.py
python tests/test_parser.py
```

---

## Project Structure

```
VIPER/
├── lexer/                        # PHASE 1: Lexical analysis
│   ├── definitions.py            # Keywords, data types, operators, symbols, limits
│   ├── errors.py                 # Lexical error classes
│   ├── tokens.py                 # Token dataclass (type, lexeme, line, column)
│   └── lexer.py                  # Lexer / tokenizer
│
├── syntax/                       # PHASE 2: Syntax analysis
│   ├── grammar.py                # FIRST / FOLLOW sets and operator groups
│   ├── errors.py                 # SyntaxAnalysisError (line + column)
│   └── parser.py                 # Recursive descent parser, one method per non-terminal
│
├── tests/
│   ├── test_lexer.py             # Lexer tests
│   └── test_parser.py            # Parser tests
│
├── syntax_error_cases/           # 10 programs, each with exactly one syntax error
│
├── main.py                       # Runs Phase 1 only
├── parser_main.py                # Runs Phase 1 then Phase 2
│
├── source_valid.viper            # Lexically valid program (lexer test)
├── source_errors.viper           # Program with lexical errors (lexer test)
├── syntax_valid.viper            # Program that uses every grammar rule (parser test)
└── README.md
```

---

## Language Overview

### Program boundaries

Every VIPER program starts with `HOLD` and ends with `RELEASE`.

```
HOLD
    # your code here
RELEASE
```

### Data types

| Keyword | Meaning     | Example                   |
|---------|-------------|---------------------------|
| `fang`  | integer     | `fang age = 20;`          |
| `venom` | float       | `venom price = 19.95;`    |
| `scale` | char        | `scale grade = 'A';`      |
| `coil`  | string      | `coil name = "Fahad";`    |
| `hiss`  | boolean     | `hiss ready = true;`      |
| `shed`  | void        | `nest shed greet() { }`   |

### Keywords

| Keyword    | Role               | Syntax |
|------------|--------------------|--------|
| `strike`   | if                 | `strike (cond) { ... }` |
| `shift`    | else if            | `shift (cond) { ... }` |
| `slither`  | else               | `slither { ... }` |
| `coilrun`  | for loop           | `coilrun (fang i = 0; i < n; i += 1) { ... }` |
| `stalk`    | while loop         | `stalk (cond) { ... }` |
| `lurk`     | do-while loop      | `lurk { ... } stalk (cond);` |
| `escape`   | break              | `escape;` |
| `slide`    | continue           | `slide;` |
| `nest`     | function           | `nest fang add(fang a, fang b) { ... }` |
| `fangback` | return             | `fangback a + b;` |
| `sense`    | input              | `sense(x);` |
| `hissout`  | output / print     | `hissout("x =", x);` |

### Operators (highest to lowest precedence)

| Level | Category        | Operators                       | Associativity |
|-------|-----------------|---------------------------------|---------------|
| 1     | Grouping        | `( )`                           | n/a           |
| 2     | Logical NOT     | `!`                             | right         |
| 3     | Multiplicative  | `*` `/` `%`                     | left          |
| 4     | Additive        | `+` `-`                         | left          |
| 5     | Relational      | `<` `>` `<=` `>=`               | left          |
| 6     | Equality        | `==` `!=`                       | left          |
| 7     | Logical AND     | `&&`                            | left          |
| 8     | Logical OR      | `\|\|`                          | left          |
| 9     | Assignment      | `=` `+=` `-=` `*=` `/=`         | right         |

### Literals

| Kind      | Example            |
|-----------|--------------------|
| Integer   | `25`               |
| Float     | `87.50`            |
| Character | `'A'`              |
| String    | `"Hello"`          |
| Boolean   | `true`, `false`    |

### Comments

```
# single-line comment

##
   multi-line comment
   everything here is ignored
##
```

### Example program

```
HOLD

fang marks = 85;
coil name = "Fahad";

strike (marks >= 80) {
    hissout(name, "got an A");
}
shift (marks >= 50) {
    hissout(name, "passed");
}
slither {
    hissout(name, "failed");
}

coilrun (fang i = 0; i < 3; i += 1) {
    hissout(i);
}

nest fang add(fang a, fang b) {
    fangback a + b;
}

RELEASE
```

---

## Phase 1: Lexical Analyzer

The lexer reads the source character by character. It groups the characters into **tokens**, skips whitespace and comments, and records lexical errors with their line and column.

```bash
python main.py source_valid.viper
```

### Token types

| Token type     | Produced for                                    | Example lexeme   |
|----------------|-------------------------------------------------|------------------|
| `DT`           | data type keywords                              | `fang`, `shed`   |
| `ID`           | identifiers                                     | `studentCount`   |
| `DIGIT`        | integer literals                                | `25`             |
| `FLOAT_CONST`  | float literals                                  | `87.50`          |
| `CHAR_CONST`   | character literals                              | `A`              |
| `STRING_CONST` | string literals                                 | `Hello`          |
| `BOOL_CONST`   | `true`, `false`                                 | `true`           |
| keyword itself | `HOLD`, `RELEASE`, `strike`, `stalk`, ...       | `strike`         |
| operator itself| `+`, `+=`, `==`, `&&`, `!`, ...                  | `+=`             |
| symbol itself  | `(` `)` `{` `}` `[` `]` `;` `,` `:`             | `;`              |

### Lexical rules

- An identifier starts with a letter or `_`, followed by letters, digits or `_`.
- Identifiers can be at most **16 characters** long.
- Numbers can be at most **16 digits** long.
- A float needs digits on both sides of the `.` (`19.` is invalid).
- Two-character operators are matched first, so `>=` is one token, not `>` followed by `=`.

### Lexical errors

| Error                       | Trigger                                  | Example        |
|-----------------------------|------------------------------------------|----------------|
| `IllegalCharacterError`     | character not in the VIPER alphabet      | `@`            |
| `InvalidIdentifierError`    | identifier starting with a digit         | `123student`   |
| `UnterminatedStringError`   | string missing its closing `"`           | `"Fahad`       |
| Unterminated multiline comment | `##` never closed                     | `## ...`       |
| `NumberTooLongError`        | number longer than 16 digits             | `12345678901234567` |
| `IdentifierTooLongError`    | identifier longer than 16 characters     | `averyveryverylongname` |
| Invalid float / character   | malformed literal                        | `19.`, `'ab'`  |

The lexer does **not** stop at the first error. It collects all of them:

```
Lexical Error at line 14, column 21: Illegal character '@'
Lexical Error at line 21, column 6: Invalid identifier '123student'
Lexical Error at line 27, column 19: Number exceeds maximum length: '1234567890123456789012345678901234567890'
Lexical Error at line 34, column 13: Unterminated string literal
Lexical Error at line 41, column 1: Unterminated multiline comment
```

---

## Phase 2: Syntax Analyzer

The syntax analyzer is a **recursive descent parser** for an **LL(1)** grammar. It takes the tokens produced by the lexer, unchanged, and checks that their order follows the VIPER grammar.

```bash
python parser_main.py syntax_valid.viper
```

### How it works

- **One method per non-terminal.** For example, `<conditional>` becomes `conditional()`, and the production is written as a comment above each method.
- **One token of lookahead.** When a rule has alternatives, the parser compares the current token with that alternative's **FIRST** set. For an `ε` alternative, it checks the **FOLLOW** set instead. These sets live in `syntax/grammar.py`.
- **`match(t)`** consumes the current token if its type is `t`. Otherwise it raises a syntax error.
- An end-of-input marker `$` is added after the last token.
- If the lexer reports any error, parsing is **skipped**, because a token stream with errors in it can't be parsed reliably.
- The parser stops at the **first** syntax error and reports its line, its column, what was expected, and what was found.

### Pipeline

```
 source.viper ──► Lexer ──► tokens ──► Parser ──► "PARSING SUCCESSFUL"
                    │                     │
                    ▼                     ▼
             lexical errors          syntax error
            (parsing skipped)     (line, column, expected)
```

### Example: syntax error

`syntax_error_cases/01_missing_semicolon.viper`:
```
HOLD

fang age = 20
hissout(age);

RELEASE
```

Output:
```
================================================================================
PHASE 1: LEXICAL ANALYSIS
================================================================================
No lexical errors found. 11 tokens generated.

================================================================================
PHASE 2: SYNTAX ANALYSIS (RECURSIVE DESCENT)
================================================================================
Syntax Error at line 4, column 1: Expected an operator, ')', ',' or ';' but found 'hissout'

================================================================================
PARSING FAILED: PROGRAM HAS A SYNTAX ERROR.
================================================================================
```

The error is reported at line 4 because the parser only finds out that the `;` is missing when it reaches the next token, `hissout`.

### Parse tree

Add `-tree` to print the parse tree as indented text:

```
<program>
  match HOLD
  <statements>
    <statement>
      <typed_statement>
        <data_type>
          match fang
        match x
        <typed_tail>
          match =
          <expression>
            ...
```

---

## Grammar (LL(1) CFG)

Terminals are the **token types** listed above. `ε` is the empty string.
The grammar has **no left recursion**, is **left-factored**, and was checked to have **0 LL(1) conflicts**: for every non-terminal, the predict sets of its alternatives are pairwise disjoint.

```
<program>             → HOLD <statements> RELEASE
<statements>          → <statement> <statements> | ε
<statement>           → <typed_statement> | <expr_statement> | <conditional>
                      | <loop> | <function> | <io_statement>
                      | <return_statement> | <escape> | <slide>

<typed_statement>     → <data_type> ID <typed_tail>
<typed_tail>          → ; | = <expression> ;
<data_type>           → DT
<expr_statement>      → <expression> ;

<expression>          → <logical_or> <assignment_tail>
<assignment_tail>     → <assign_op> <expression> | ε
<assign_op>           → = | += | -= | *= | /=
<logical_or>          → <logical_and> <logical_or_tail>
<logical_or_tail>     → || <logical_and> <logical_or_tail> | ε
<logical_and>         → <equality> <logical_and_tail>
<logical_and_tail>    → && <equality> <logical_and_tail> | ε
<equality>            → <relational> <equality_tail>
<equality_tail>       → <equality_op> <relational> <equality_tail> | ε
<equality_op>         → == | !=
<relational>          → <additive> <relational_tail>
<relational_tail>     → <ordering_op> <additive> <relational_tail> | ε
<ordering_op>         → < | > | <= | >=
<additive>            → <multiplicative> <additive_tail>
<additive_tail>       → <add_op> <multiplicative> <additive_tail> | ε
<add_op>              → + | -
<multiplicative>      → <unary> <multiplicative_tail>
<multiplicative_tail> → <mul_op> <unary> <multiplicative_tail> | ε
<mul_op>              → * | / | %
<unary>               → ! <unary> | <primary>
<primary>             → ID | <value> | ( <expression> )
<value>               → DIGIT | FLOAT_CONST | CHAR_CONST | STRING_CONST | BOOL_CONST

<conditional>         → strike ( <expression> ) <block> <shift_chain> <optional_slither>
<shift_chain>         → shift ( <expression> ) <block> <shift_chain> | ε
<optional_slither>    → slither <block> | ε
<block>               → { <statements> }

<loop>                → <coilrun_loop> | <stalk_loop> | <lurk_loop>
<coilrun_loop>        → coilrun ( <typed_statement> <expression> ; <update> ) <block>
<stalk_loop>          → stalk ( <expression> ) <block>
<lurk_loop>           → lurk <block> stalk ( <expression> ) ;
<update>              → <expression>
<escape>              → escape ;
<slide>               → slide ;

<function>            → nest <return_type> ID ( <parameters> ) <block>
<return_type>         → <data_type>
<parameters>          → <parameter_list> | ε
<parameter_list>      → <parameter> <parameter_tail>
<parameter_tail>      → , <parameter> <parameter_tail> | ε
<parameter>           → <data_type> ID
<return_statement>    → fangback <expression> ;

<io_statement>        → <input_statement> | <output_statement>
<input_statement>     → sense ( ID ) ;
<output_statement>    → hissout ( <output_list> ) ;
<output_list>         → <expression> <output_list_tail>
<output_list_tail>    → , <expression> <output_list_tail> | ε
```

### Key FIRST / FOLLOW sets

| Set                       | Members |
|---------------------------|---------|
| FIRST(`<expression>`)     | `ID` `DIGIT` `FLOAT_CONST` `CHAR_CONST` `STRING_CONST` `BOOL_CONST` `!` `(` |
| FIRST(`<statement>`)      | `DT` ∪ FIRST(`<expression>`) ∪ `strike` `coilrun` `stalk` `lurk` `nest` `sense` `hissout` `fangback` `escape` `slide` |
| FOLLOW(`<statements>`)    | `RELEASE` `}` |
| FOLLOW(`<expression>`)    | `)` `,` `;` |
| FOLLOW(`<parameters>`)    | `)` |
| FOLLOW(`<shift_chain>`)   | `slither` ∪ FOLLOW(`<statement>`) |

### How the grammar was made LL(1)

| Problem in the original CFG | Fix |
|-----------------------------|-----|
| Left recursion in the expression rules (`E → E + T`) | Rewritten as `E → T E'`, `E' → + T E' \| ε` (the `_tail` rules) |
| `<declaration>` and `<initialization>` both start with `DT ID` | Left-factored into `<typed_statement>` + `<typed_tail>` |
| `<assignment>` and `<logical_or>` both start with `ID` | `<expression> → <logical_or> <assignment_tail>` |
| `<value> → <expression>` with `<primary> → <value>` (indirect left recursion) | `<value>` holds only constants |
| `<parameter_list>` alternatives share the prefix `<parameter>` | Left-factored into `<parameter_tail>` |
| Ambiguous if / else-if / else | `strike` → `<shift_chain>` → `<optional_slither>`, with every body a `<block>` |
| Operator precedence not encoded | One grammar level per precedence level |

---

## Testing

### Run all tests

```bash
python tests/test_lexer.py     # Phase 1
python tests/test_parser.py    # Phase 2
```

Each script ends with `ALL ... TESTS COMPLETED SUCCESSFULLY` when everything passes.

### What the parser tests check

| Test | Files | Expected result |
|------|-------|-----------------|
| Valid program | `syntax_valid.viper` | accepted |
| Syntax errors | every file in `syntax_error_cases/` | each one rejected |

### Syntax error cases

| File | Mistake | Reported |
|------|---------|----------|
| `01_missing_semicolon.viper`            | `fang age = 20` without `;`        | line 4, col 1 |
| `02_strike_without_parentheses.viper`   | `strike age > 18 { }`              | line 5, col 8 |
| `03_slither_with_condition.viper`       | `slither (marks > 0) { }`          | line 8, col 9 |
| `04_lurk_missing_semicolon.viper`       | `lurk { } stalk (x > 0)`           | line 9, col 1 |
| `05_function_without_return_type.viper` | `nest add(...)`                    | line 3, col 6 |
| `06_unclosed_parenthesis.viper`         | `(5 + 3;`                          | line 3, col 20 |
| `07_missing_release.viper`              | no `RELEASE`                       | end of file |
| `08_missing_closing_brace.viper`        | `{` never closed                   | line 6, col 1 |
| `09_incomplete_expression.viper`        | `5 +;`                             | line 3, col 13 |
| `10_sense_needs_identifier.viper`       | `sense(5);`                        | line 3, col 7 |

### Adding a test

- **For a program that should pass:** write it in a `.viper` file and run `python parser_main.py yourfile.viper`.
- **For a program that should fail:** put **exactly one** mistake in it, because the parser stops at the first error. Save it in `syntax_error_cases/`, then rerun `python tests/test_parser.py`. The new file is picked up automatically.

### Checking precedence

```bash
python parser_main.py prec.viper -tree     # prec.viper: HOLD fang x = 1 + 2 * 3; RELEASE
```

In the tree, `* 3` must appear deeper (under `<multiplicative_tail>`) than `+` (under `<additive_tail>`). That shows `*` binds tighter than `+`.

---

## Known Limitations

- **`source_valid.viper` is a lexer test, not a parser test.** It is lexically valid but not syntactically valid: it contains `nest()`, `slither (cond)`, a bare `stalk;`, arrays and `fang x = 10, y = 20;`. The parser correctly rejects it at line 86. Use `syntax_valid.viper` to test the parser.
- **No function calls.** Functions can be declared with `nest`, but there is no rule for calling them, so `add(1, 2)` is a syntax error.
- **No arrays.** The lexer produces `[` and `]` tokens, but the grammar doesn't use them yet.
- **No multiple declarations in one statement.** Write `fang x = 10; fang y = 20;` instead of `fang x = 10, y = 20;`.
- **`shed` is a `DT` token**, so `shed x;` is syntactically valid. Rejecting void variables belongs in semantic analysis.
- **Assignment targets aren't restricted by the parser.** `a + b = 5;` parses, and checking that the left side is a variable belongs in semantic analysis, as in C and Java.
- **Error recovery.** The parser stops at the first syntax error. It doesn't use panic-mode recovery.

---

## Roadmap

- [x] Language specification (tokens + CFG)
- [x] Grammar transformed to LL(1) (left recursion removed, left-factored, FIRST/FOLLOW)
- [x] Phase 1: Lexical analyzer
- [x] Phase 2: Recursive descent parser
- [ ] Function calls and arrays in the grammar
- [ ] Phase 3: Semantic analyzer (symbol table, type checking, scope checking)
- [ ] Intermediate code generation (three-address code)
