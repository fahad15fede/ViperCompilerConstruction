from lexer.tokens import Token

from .errors import SyntaxAnalysisError

from .grammar import (
    FIRST_DATA_TYPE,
    FIRST_VALUE,
    FIRST_EXPRESSION,
    FIRST_STATEMENT,
    FOLLOW_STATEMENTS,
    FOLLOW_ASSIGNMENT_TAIL,
    FOLLOW_PARAMETERS,
    FOLLOW_PARAMETER_TAIL,
    FOLLOW_OUTPUT_LIST_TAIL,
    ASSIGN_OPS,
    EQUALITY_OPS,
    ORDERING_OPS,
    ADD_OPS,
    MUL_OPS,
    LOOP_KEYWORDS,
    IO_KEYWORDS
)


class Parser:
    """
    Recursive descent parser for the VIPER LL(1) grammar.

    One method per non-terminal. The production is written
    above each method. Alternatives are chosen by looking at
    the current token (lookahead) and checking FIRST / FOLLOW sets.
    """

    def __init__(self, tokens, trace=False):

        self.tokens = list(tokens)
        self.position = 0

        # Add end-of-input marker $
        if self.tokens:
            last = self.tokens[-1]
            end_line = last.line
            end_column = last.column + len(last.lexeme)
        else:
            end_line = 1
            end_column = 1

        self.tokens.append(
            Token("$", "$", end_line, end_column)
        )

        # Parse trace (indented parse tree)
        self.trace = trace
        self.depth = 0
        self.trace_lines = []

    # ---------------------------------------------------------
    # BASIC TOKEN FUNCTIONS
    # ---------------------------------------------------------

    def current_token(self):
        return self.tokens[self.position]

    def lookahead(self):
        return self.tokens[self.position].type

    def error(self, expected):
        raise SyntaxAnalysisError(
            expected,
            self.current_token()
        )

    def match(self, expected_type):

        if self.lookahead() == expected_type:

            if self.trace:
                self.trace_lines.append(
                    "  " * self.depth
                    + f"match {self.current_token().lexeme}"
                )

            self.position += 1

        else:

            self.error(f"'{expected_type}'")

    # ---------------------------------------------------------
    # TRACE HELPERS
    # ---------------------------------------------------------

    def enter(self, name):

        if self.trace:
            self.trace_lines.append(
                "  " * self.depth + f"<{name}>"
            )

        self.depth += 1

    def leave(self):
        self.depth -= 1

    # ---------------------------------------------------------
    # START
    # ---------------------------------------------------------

    def parse(self):

        self.program()

        if self.lookahead() != "$":
            self.error("end of file after RELEASE")

        return True

    # =========================================================
    # PROGRAM AND STATEMENTS
    # =========================================================

    # <program> -> HOLD <statements> RELEASE
    def program(self):
        self.enter("program")

        self.match("HOLD")
        self.statements()
        self.match("RELEASE")

        self.leave()

    # <statements> -> <statement> <statements> | ε
    def statements(self):
        self.enter("statements")

        if self.lookahead() in FIRST_STATEMENT:
            self.statement()
            self.statements()

        elif self.lookahead() in FOLLOW_STATEMENTS:
            pass  # ε

        else:
            self.error("a statement, '}' or RELEASE")

        self.leave()

    # <statement> -> <typed_statement> | <expr_statement>
    #              | <conditional>     | <loop>
    #              | <function>        | <io_statement>
    #              | <return_statement>| <escape> | <slide>
    def statement(self):
        self.enter("statement")

        token_type = self.lookahead()

        if token_type in FIRST_DATA_TYPE:
            self.typed_statement()

        elif token_type in FIRST_EXPRESSION:
            self.expr_statement()

        elif token_type == "strike":
            self.conditional()

        elif token_type in LOOP_KEYWORDS:
            self.loop()

        elif token_type == "nest":
            self.function()

        elif token_type in IO_KEYWORDS:
            self.io_statement()

        elif token_type == "fangback":
            self.return_statement()

        elif token_type == "escape":
            self.escape()

        elif token_type == "slide":
            self.slide()

        else:
            self.error("a statement")

        self.leave()

    # =========================================================
    # DECLARATION / INITIALIZATION
    # =========================================================

    # <typed_statement> -> <data_type> ID <typed_tail>
    def typed_statement(self):
        self.enter("typed_statement")

        self.data_type()
        self.match("ID")
        self.typed_tail()

        self.leave()

    # <typed_tail> -> ; | = <expression> ;
    def typed_tail(self):
        self.enter("typed_tail")

        if self.lookahead() == ";":
            self.match(";")

        elif self.lookahead() == "=":
            self.match("=")
            self.expression()
            self.match(";")

        else:
            self.error("';' or '='")

        self.leave()

    # <data_type> -> DT
    def data_type(self):
        self.enter("data_type")

        if self.lookahead() == "DT":
            self.match("DT")
        else:
            self.error("a data type (fang, venom, scale, coil, hiss, shed)")

        self.leave()

    # <expr_statement> -> <expression> ;
    def expr_statement(self):
        self.enter("expr_statement")

        self.expression()
        self.match(";")

        self.leave()

    # =========================================================
    # EXPRESSIONS  (lowest precedence first)
    # =========================================================

    # <expression> -> <logical_or> <assignment_tail>
    def expression(self):
        self.enter("expression")

        self.logical_or()
        self.assignment_tail()

        self.leave()

    # <assignment_tail> -> <assign_op> <expression> | ε
    def assignment_tail(self):
        self.enter("assignment_tail")

        if self.lookahead() in ASSIGN_OPS:
            self.assign_op()
            self.expression()

        elif self.lookahead() in FOLLOW_ASSIGNMENT_TAIL:
            pass  # ε

        else:
            self.error("an operator, ')', ',' or ';'")

        self.leave()

    # <assign_op> -> = | += | -= | *= | /=
    def assign_op(self):
        self.enter("assign_op")

        if self.lookahead() in ASSIGN_OPS:
            self.match(self.lookahead())
        else:
            self.error("an assignment operator")

        self.leave()

    # <logical_or> -> <logical_and> <logical_or_tail>
    def logical_or(self):
        self.enter("logical_or")

        self.logical_and()
        self.logical_or_tail()

        self.leave()

    # <logical_or_tail> -> || <logical_and> <logical_or_tail> | ε
    def logical_or_tail(self):
        self.enter("logical_or_tail")

        if self.lookahead() == "||":
            self.match("||")
            self.logical_and()
            self.logical_or_tail()

        self.leave()

    # <logical_and> -> <equality> <logical_and_tail>
    def logical_and(self):
        self.enter("logical_and")

        self.equality()
        self.logical_and_tail()

        self.leave()

    # <logical_and_tail> -> && <equality> <logical_and_tail> | ε
    def logical_and_tail(self):
        self.enter("logical_and_tail")

        if self.lookahead() == "&&":
            self.match("&&")
            self.equality()
            self.logical_and_tail()

        self.leave()

    # <equality> -> <relational> <equality_tail>
    def equality(self):
        self.enter("equality")

        self.relational()
        self.equality_tail()

        self.leave()

    # <equality_tail> -> <equality_op> <relational> <equality_tail> | ε
    def equality_tail(self):
        self.enter("equality_tail")

        if self.lookahead() in EQUALITY_OPS:
            self.equality_op()
            self.relational()
            self.equality_tail()

        self.leave()

    # <equality_op> -> == | !=
    def equality_op(self):
        self.enter("equality_op")

        if self.lookahead() in EQUALITY_OPS:
            self.match(self.lookahead())
        else:
            self.error("'==' or '!='")

        self.leave()

    # <relational> -> <additive> <relational_tail>
    def relational(self):
        self.enter("relational")

        self.additive()
        self.relational_tail()

        self.leave()

    # <relational_tail> -> <ordering_op> <additive> <relational_tail> | ε
    def relational_tail(self):
        self.enter("relational_tail")

        if self.lookahead() in ORDERING_OPS:
            self.ordering_op()
            self.additive()
            self.relational_tail()

        self.leave()

    # <ordering_op> -> < | > | <= | >=
    def ordering_op(self):
        self.enter("ordering_op")

        if self.lookahead() in ORDERING_OPS:
            self.match(self.lookahead())
        else:
            self.error("'<', '>', '<=' or '>='")

        self.leave()

    # <additive> -> <multiplicative> <additive_tail>
    def additive(self):
        self.enter("additive")

        self.multiplicative()
        self.additive_tail()

        self.leave()

    # <additive_tail> -> <add_op> <multiplicative> <additive_tail> | ε
    def additive_tail(self):
        self.enter("additive_tail")

        if self.lookahead() in ADD_OPS:
            self.add_op()
            self.multiplicative()
            self.additive_tail()

        self.leave()

    # <add_op> -> + | -
    def add_op(self):
        self.enter("add_op")

        if self.lookahead() in ADD_OPS:
            self.match(self.lookahead())
        else:
            self.error("'+' or '-'")

        self.leave()

    # <multiplicative> -> <unary> <multiplicative_tail>
    def multiplicative(self):
        self.enter("multiplicative")

        self.unary()
        self.multiplicative_tail()

        self.leave()

    # <multiplicative_tail> -> <mul_op> <unary> <multiplicative_tail> | ε
    def multiplicative_tail(self):
        self.enter("multiplicative_tail")

        if self.lookahead() in MUL_OPS:
            self.mul_op()
            self.unary()
            self.multiplicative_tail()

        self.leave()

    # <mul_op> -> * | / | %
    def mul_op(self):
        self.enter("mul_op")

        if self.lookahead() in MUL_OPS:
            self.match(self.lookahead())
        else:
            self.error("'*', '/' or '%'")

        self.leave()

    # <unary> -> ! <unary> | <primary>
    def unary(self):
        self.enter("unary")

        if self.lookahead() == "!":
            self.match("!")
            self.unary()
        else:
            self.primary()

        self.leave()

    # <primary> -> ID | <value> | ( <expression> )
    def primary(self):
        self.enter("primary")

        if self.lookahead() == "ID":
            self.match("ID")

        elif self.lookahead() in FIRST_VALUE:
            self.value()

        elif self.lookahead() == "(":
            self.match("(")
            self.expression()
            self.match(")")

        else:
            self.error("an identifier, a constant or '('")

        self.leave()

    # <value> -> DIGIT | FLOAT_CONST | CHAR_CONST | STRING_CONST | BOOL_CONST
    def value(self):
        self.enter("value")

        if self.lookahead() in FIRST_VALUE:
            self.match(self.lookahead())
        else:
            self.error("a constant")

        self.leave()

    # =========================================================
    # CONDITIONAL
    # =========================================================

    # <conditional> -> strike ( <expression> ) <block> <shift_chain> <optional_slither>
    def conditional(self):
        self.enter("conditional")

        self.match("strike")
        self.match("(")
        self.expression()
        self.match(")")
        self.block()
        self.shift_chain()
        self.optional_slither()

        self.leave()

    # <shift_chain> -> shift ( <expression> ) <block> <shift_chain> | ε
    def shift_chain(self):
        self.enter("shift_chain")

        if self.lookahead() == "shift":
            self.match("shift")
            self.match("(")
            self.expression()
            self.match(")")
            self.block()
            self.shift_chain()

        self.leave()

    # <optional_slither> -> slither <block> | ε
    def optional_slither(self):
        self.enter("optional_slither")

        if self.lookahead() == "slither":
            self.match("slither")
            self.block()

        self.leave()

    # <block> -> { <statements> }
    def block(self):
        self.enter("block")

        self.match("{")
        self.statements()
        self.match("}")

        self.leave()

    # =========================================================
    # LOOPS AND JUMPS
    # =========================================================

    # <loop> -> <coilrun_loop> | <stalk_loop> | <lurk_loop>
    def loop(self):
        self.enter("loop")

        if self.lookahead() == "coilrun":
            self.coilrun_loop()

        elif self.lookahead() == "stalk":
            self.stalk_loop()

        elif self.lookahead() == "lurk":
            self.lurk_loop()

        else:
            self.error("coilrun, stalk or lurk")

        self.leave()

    # <coilrun_loop> -> coilrun ( <typed_statement> <expression> ; <update> ) <block>
    def coilrun_loop(self):
        self.enter("coilrun_loop")

        self.match("coilrun")
        self.match("(")
        self.typed_statement()
        self.expression()
        self.match(";")
        self.update()
        self.match(")")
        self.block()

        self.leave()

    # <stalk_loop> -> stalk ( <expression> ) <block>
    def stalk_loop(self):
        self.enter("stalk_loop")

        self.match("stalk")
        self.match("(")
        self.expression()
        self.match(")")
        self.block()

        self.leave()

    # <lurk_loop> -> lurk <block> stalk ( <expression> ) ;
    def lurk_loop(self):
        self.enter("lurk_loop")

        self.match("lurk")
        self.block()
        self.match("stalk")
        self.match("(")
        self.expression()
        self.match(")")
        self.match(";")

        self.leave()

    # <update> -> <expression>
    def update(self):
        self.enter("update")

        self.expression()

        self.leave()

    # <escape> -> escape ;
    def escape(self):
        self.enter("escape")

        self.match("escape")
        self.match(";")

        self.leave()

    # <slide> -> slide ;
    def slide(self):
        self.enter("slide")

        self.match("slide")
        self.match(";")

        self.leave()

    # =========================================================
    # FUNCTIONS
    # =========================================================

    # <function> -> nest <return_type> ID ( <parameters> ) <block>
    def function(self):
        self.enter("function")

        self.match("nest")
        self.return_type()
        self.match("ID")
        self.match("(")
        self.parameters()
        self.match(")")
        self.block()

        self.leave()

    # <return_type> -> <data_type>
    def return_type(self):
        self.enter("return_type")

        self.data_type()

        self.leave()

    # <parameters> -> <parameter_list> | ε
    def parameters(self):
        self.enter("parameters")

        if self.lookahead() in FIRST_DATA_TYPE:
            self.parameter_list()

        elif self.lookahead() in FOLLOW_PARAMETERS:
            pass  # ε

        else:
            self.error("a parameter or ')'")

        self.leave()

    # <parameter_list> -> <parameter> <parameter_tail>
    def parameter_list(self):
        self.enter("parameter_list")

        self.parameter()
        self.parameter_tail()

        self.leave()

    # <parameter_tail> -> , <parameter> <parameter_tail> | ε
    def parameter_tail(self):
        self.enter("parameter_tail")

        if self.lookahead() == ",":
            self.match(",")
            self.parameter()
            self.parameter_tail()

        elif self.lookahead() in FOLLOW_PARAMETER_TAIL:
            pass  # ε

        else:
            self.error("',' or ')'")

        self.leave()

    # <parameter> -> <data_type> ID
    def parameter(self):
        self.enter("parameter")

        self.data_type()
        self.match("ID")

        self.leave()

    # <return_statement> -> fangback <expression> ;
    def return_statement(self):
        self.enter("return_statement")

        self.match("fangback")
        self.expression()
        self.match(";")

        self.leave()

    # =========================================================
    # INPUT / OUTPUT
    # =========================================================

    # <io_statement> -> <input_statement> | <output_statement>
    def io_statement(self):
        self.enter("io_statement")

        if self.lookahead() == "sense":
            self.input_statement()

        elif self.lookahead() == "hissout":
            self.output_statement()

        else:
            self.error("sense or hissout")

        self.leave()

    # <input_statement> -> sense ( ID ) ;
    def input_statement(self):
        self.enter("input_statement")

        self.match("sense")
        self.match("(")
        self.match("ID")
        self.match(")")
        self.match(";")

        self.leave()

    # <output_statement> -> hissout ( <output_list> ) ;
    def output_statement(self):
        self.enter("output_statement")

        self.match("hissout")
        self.match("(")
        self.output_list()
        self.match(")")
        self.match(";")

        self.leave()

    # <output_list> -> <expression> <output_list_tail>
    def output_list(self):
        self.enter("output_list")

        self.expression()
        self.output_list_tail()

        self.leave()

    # <output_list_tail> -> , <expression> <output_list_tail> | ε
    def output_list_tail(self):
        self.enter("output_list_tail")

        if self.lookahead() == ",":
            self.match(",")
            self.expression()
            self.output_list_tail()

        elif self.lookahead() in FOLLOW_OUTPUT_LIST_TAIL:
            pass  # ε

        else:
            self.error("',' or ')'")

        self.leave()
