from .tokenizer import Tokenizer, TokenType, Token

from .astnodes import *


class TreeMaker:

    def __init__(self, source):
        self.source = source
        self.tokens = Tokenizer(self.source).run()
        self.pos = 0

    def _skip_xml_header(self):
        self.consume(TokenType.LBRACKET)
        self.consume(TokenType.QUESTION)
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.EQUAL)
        self.consume(TokenType.TEXT)
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.EQUAL)
        self.consume(TokenType.TEXT)
        self.consume(TokenType.QUESTION)
        self.consume(TokenType.RBRACKET)

    def make(self):
        # while not self.match(TokenType.EOF):
        self._skip_xml_header()
        ast = self.node()

        return ast

    def match(self, token_type: TokenType):
        current = self.get(0)
        if token_type != current.type:
            return False
        self.pos += 1
        return True

    def consume(self, token_type: TokenType):
        current = self.get(0)

        if token_type != current.type:
            assert False, f"expected {token_type}"

        self.pos += 1
        return current

    def get(self, relative):
        pos = self.pos + relative
        if pos >= len(self.tokens):
            return Token(TokenType.EOF, "")
        return self.tokens[pos]

    def lookahead(self, relative: int, token_type: TokenType):
        return self.get(relative).type == token_type

    def node(self):
        if not self.match(TokenType.LBRACKET):
            return self.atomic()

        tag_name = self.get(0).lexeme

        self.consume(TokenType.IDENTIFIER)
        tag_node = TagNode(
            name=tag_name,
            attrs=dict(),
            childrens=[]
        )

        if self.lookahead(0, TokenType.SLASH) and self.lookahead(1, TokenType.RBRACKET):
            self.consume(TokenType.SLASH)
            self.consume(TokenType.RBRACKET)
            return tag_node

        while not self.match(TokenType.RBRACKET):
            attribute_name = self.consume(TokenType.IDENTIFIER).lexeme
            self.consume(TokenType.EQUAL)
            attribute_value = self.atomic()
            tag_node.attrs[attribute_name] = attribute_value
            if self.lookahead(0, TokenType.SLASH):
                self.consume(TokenType.SLASH)
                self.consume(TokenType.RBRACKET)
                return tag_node

        while not self.is_closure(tag_name):
            tag_node.childrens.append(self.node())

        self.consume(TokenType.LBRACKET)
        self.consume(TokenType.SLASH)
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.RBRACKET)

        return tag_node

    def is_closure(self, tag_name):
        left = self.lookahead(0, TokenType.LBRACKET)
        slash = self.lookahead(1, TokenType.SLASH)
        tag_equal = self.get(2).lexeme == tag_name
        right = self.lookahead(3, TokenType.RBRACKET)
        return left and slash and tag_equal and right

    def atomic(self):
        current = self.get(0)

        if self.match(TokenType.NUMBER):
            if current.lexeme.find(".") != -1:
                return NumberNode(float(current.lexeme))
            return NumberNode(int(current.lexeme))
        elif self.match(TokenType.TEXT):
            return StringNode(current.lexeme)
        elif self.match(TokenType.IDENTIFIER):
            return ValueNode(current.lexeme)

        assert False, "unknown token"
