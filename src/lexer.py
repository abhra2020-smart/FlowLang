from AM.src.tokens import Token, TokenType

WHITESPACE = ' \n\t'
DIGITS = '0123456789'


class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == '.' or self.current_char in DIGITS:
                yield self.generate_number()
            elif self.current_char == '+':
                self.advance()
                yield Token(TokenType.PLUS)
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.MINUS)
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.MULTIPLY)
            elif self.current_char == '/':
                self.advance()
                yield Token(TokenType.DIVIDE)
            elif self.current_char == '(':
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenType.RPAREN)
            elif self.current_char == '^':
                self.advance()
                yield Token(TokenType.POWER)
            elif self.current_char == '%':
                self.advance()
                yield Token(TokenType.MOD)
            elif self.current_char == '|':
                self.advance()
                yield Token(TokenType.INTDIV)
            elif self.current_char in 'lL':
                self.advance()
                yield Token(TokenType.LS)
            elif self.current_char in 'rR':
                self.advance()
                yield Token(TokenType.RS)
            elif self.current_char == '<':
                self.advance()
                yield Token(TokenType.ST)
            elif self.current_char == '>':
                self.advance()
                yield Token(TokenType.GT)
            elif self.current_char in 'eE':
                self.advance()
                yield Token(TokenType.EQU)
            else:
                raise Exception(f"Illegal character '{self.current_char}'")

    def generate_number(self):
        decimal_point_count = 0
        number_str = self.current_char
        type_ = int
        self.advance()

        while self.current_char != None and (self.current_char == '.' or self.current_char in DIGITS):
            if self.current_char == '.':
                decimal_point_count += 1
                type_ = float
                if decimal_point_count > 1:
                    raise SyntaxError('Invalid syntax')

            number_str += self.current_char
            self.advance()

        if number_str.startswith('.'):
            number_str = '0' + number_str
        if number_str.endswith('.'):
            number_str += '0'

        return Token(TokenType.NUMBER, type_(number_str))