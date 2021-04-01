from .tokens import TokenType
from .nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    def raise_error(self):
        raise Exception("Invalid syntax")

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        if self.current_token == None:
            return None

        result = self.expr()

        if self.current_token != None:
            self.raise_error()

        return result

    def expr(self):
        result = self.term()

        while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.RS, TokenType.LS):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = AddNode(result, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = SubtractNode(result, self.term())
            elif self.current_token.type == TokenType.RS:
                self.advance()
                result = RSNode(result, self.term())
            elif self.current_token.type == TokenType.LS:
                self.advance()
                result = LSNode(result, self.term())

        return result

    def term(self):
        result = self.factor()

        while self.current_token != None and self.current_token.type in (TokenType.EQU, TokenType.GT, TokenType.ST, TokenType.INTDIV, TokenType.MOD, TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.POWER):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = MultiplyNode(result, self.factor())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivideNode(result, self.factor())
            elif self.current_token.type == TokenType.POWER:
                self.advance()
                result = PowerNode(result, self.factor())
            elif self.current_token.type == TokenType.MOD:
                self.advance()
                result = ModNode(result, self.factor())
            elif self.current_token.type == TokenType.INTDIV:
                self.advance()
                result = IntDivNode(result, self.factor())
            elif self.current_token.type == TokenType.GT:
                self.advance()
                result = GreaterNode(result, self.factor())
            elif self.current_token.type == TokenType.ST:
                self.advance()
                result = SmallerNode(result, self.factor())
            elif self.current_token.type == TokenType.EQU:
                self.advance()
                result = EqualsNode(result, self.factor())

        return result

    def factor(self):
        token = self.current_token

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()

            if self.current_token.type != TokenType.RPAREN:
                self.raise_error()

            self.advance()
            return result

        elif token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)

        elif token.type == TokenType.PLUS:
            self.advance()
            return PlusNode(self.factor())

        elif token.type == TokenType.MINUS:
            self.advance()
            return MinusNode(self.factor())

        self.raise_error()