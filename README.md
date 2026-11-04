# VIPER

VIPER is a custom programming language with its own lexer written in Python. The language uses snake-themed keywords and follows a structured syntax with program boundaries, typed variables, control flow, and I/O.

---

## Project Structure

```
VIPER/
├── lexer/
│   ├── definitions.py   # All language tokens, keywords, operators, and limits
│   ├── errors.py        # Lexical error classes
│   ├── tokens.py        # Token dataclass
│   └── lexer.py         # Core lexer / tokenizer
├── tests/
│   └── test_lexer.py
├── main.py
└── README.md
```

---

## Running the Lexer

```bash
cd VIPER/lexer
python lexer.py
```

---

## Language Overview

Every VIPER program must start with `HOLD` and end with `RELEASE`.

```
HOLD
  # your code here
RELEASE
```

---

## Data Types

| Keyword | Meaning         |
|---------|-----------------|
| `fang`  | integer         |
| `venom` | float           |
| `scale` | char            |
| `coil`  | string          |
| `hiss`  | boolean         |
| `shed`  | void / null     |

```
fang age = 20;
venom price = 19.95;
scale grade = 'A';
coil name = "Fahad";
hiss ready = true;
```

---

## Keywords

| Keyword    | Role                        |
|------------|-----------------------------|
| `strike`   | if                          |
| `shift`    | else if                     |
| `slither`  | else                        |
| `coilrun`  | for loop                    |
| `stalk`    | while loop                  |
| `lurk`     | do-while                    |
| `escape`   | break                       |
| `slide`    | continue                    |
| `nest`     | function declaration        |
| `fangback` | return                      |
| `sense`    | input                       |
| `hissout`  | output / print              |

---

## Operators

| Category    | Symbols                          |
|-------------|----------------------------------|
| Arithmetic  | `+` `-` `*` `/` `%`             |
| Relational  | `==` `!=` `<` `>` `<=` `>=`    |
| Logical     | `&&` `\|\|` `!`                  |
| Assignment  | `=` `+=` `-=` `*=` `/=`        |

---

## Comments

Single-line:
```
# this is a comment
```

Multi-line:
```
#comment
  this is all ignored
comment#
```

---

## Lexical Limits

- Max identifier length: **16 characters**
- Max number length: **16 digits**

---

## Token Types

| Token        | Description                  |
|--------------|------------------------------|
| `ID`         | Identifier                   |
| `DIGIT`      | Integer literal              |
| `FLOAT_CONST`| Float literal                |
| `STRING_CONST`| String literal              |
| `CHAR_CONST` | Character literal            |
| `True/False` | Boolean literals             |
| `Hold/Release`| Program boundary tokens     |
| `DT`         | Data type keyword            |

---

## Error Types

| Error                          | Trigger                                      |
|-------------------------------|----------------------------------------------|
| `IllegalCharacterError`        | Character not in VIPER alphabet              |
| `InvalidIdentifierError`       | Identifier starts with or contains digits    |
| `UnterminatedStringError`      | String missing closing `"`                   |
| `UnterminatedMultilineCommentError` | `#comment` block missing `comment#`   |
| `NumberTooLongError`           | Number exceeds 16 digits                     |
| `IdentifierTooLongError`       | Identifier exceeds 16 characters             |

---

## Example Program

```
HOLD

fang age = 20;
venom price = 19.95;
scale grade = 'A';
coil name = "Fahad";
hiss ready = true;

strike (age > 18) {
    hissout("Adult");
}
slither {
    hissout("Minor");
}

RELEASE
```
# ViperCompilerConstruction
