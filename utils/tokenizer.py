from enum import Enum, auto


class Token:

    def __init__(self, type_, lexeme):
        self.type = type_
        self.lexeme = lexeme

    def __str__(self):
        return f"[{self.type}, {self.lexeme}]"

    def __repr__(self):
        return self.__str__()


class TokenType(Enum):
    IDENTIFIER = auto(),
    LBRACKET = auto(),
    RBRACKET = auto(),
    QUESTION = auto(),
    EQUAL= auto(),
    SLASH = auto(),
    TEXT = auto(),
    NUMBER = auto(),
    EOF = auto()


class Tokenizer:
    __RESERVED_OPS = {
        "<": TokenType.LBRACKET,
        ">": TokenType.RBRACKET,
        "?": TokenType.QUESTION,
        "/": TokenType.SLASH,
        "=": TokenType.EQUAL
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.pos = 0

    def add_token(self, type_: TokenType, lexeme: str):
        instance = Token(type_, lexeme)
        self.tokens.append(instance)

    def peek(self, relative: int) -> str:
        pos = self.pos + relative
        if pos >= len(self.source):
            return ""
        return self.source[pos]

    def next(self) -> str:
        self.pos += 1
        return self.peek(0)

    def tokenize_number(self):
        current = self.peek(0)
        buffer = ""

        while current.isdigit():
            buffer += current
            current = self.next()

            is_point = current == '.'
            is_first_point = buffer.find('.') == -1

            if is_point and is_first_point:
                buffer += current
                current = self.next()

        self.add_token(TokenType.NUMBER, buffer)

    def tokenize_identifier(self):
        buffer = ""
        current = self.peek(0)

        while True:
            if not (current.isalpha() or current.isdigit()) and current != "_":
                break
            buffer += current
            current = self.next()

        self.add_token(TokenType.IDENTIFIER, buffer)

    def tokenize_text(self):
        self.next()

        buffer = ""
        current = self.peek(0)

        while True:
            if current == "\\":
                current = self.next()
                if current == '"':
                    current = self.next()
                    buffer += '"'
                    continue
                if current == 'n':
                    current = self.next()
                    buffer += '\n'
                    continue
                if current == 't':
                    current = self.next()
                    buffer += '\t'
                    continue
                buffer += '\\'
                continue
            if current == '"':
                break
            buffer += current
            current = self.next()
        self.next()
        self.add_token(TokenType.TEXT, buffer)

    def run(self):
        while self.pos < len(self.source):
            current = self.peek(0)

            if current.isdigit():
                self.tokenize_number()
            elif current.isalpha() or current == '_':
                self.tokenize_identifier()
            elif current == '"':
                self.tokenize_text()
            elif ttype := Tokenizer.__RESERVED_OPS.get(current, None):
                self.add_token(ttype, current)
                self.next()
            else:
                self.next()

        self.add_token(TokenType.EOF, "")
        return self.tokens
