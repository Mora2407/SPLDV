from typing import Any
from dataclasses import dataclass
from enum import Enum

"""
Token Type:
- Constant = [0-9]
- Variable = [a-z][A-Z]
- Operator = +-*/()=
"""

OPERATOR: list[str] = ["+", "-", "*", "/", "(", ")", "="]

OP_DICT = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "(": "LPAREN",
    ")": "RPAREN",
    "=": "EQUAL"
}

class TokenType(Enum):
    EOF = 0
    CONSTANT = 1
    VARIABLE = 2
    LPAREN = 3
    RPAREN = 4
    MULTIPLY = 5
    DIVIDE = 6
    PLUS = 7
    MINUS = 8
    EQUAL = 9

@dataclass
class Token:
    type: TokenType
    value: str | float

    def __repr__(self) -> str:
        return f"{self.type}(\"{self.value}\")"

@dataclass
class Constant(Token):
    float: bool
    def __repr__(self) -> str:
        return super().__repr__()
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Constant):
            return self.value == other.value and self.type == other.type
        return False

@dataclass
class Variable(Token): 
    def __repr__(self) -> str:
        return super().__repr__()
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Variable):
            return self.value == other.value and self.type == other.type
        return False

@dataclass
class Operator(Token):
    def __repr__(self) -> str:
        return super().__repr__()
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Operator):
            return self.value == other.value and self.type == other.type
        return False


class Lexer:
    def __init__(self, text: str):
        self.text = iter(text)
        self.current_char: str = next(self.text)

    def next_token(self) -> None:
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = ""

    def scan(self):
        while self.current_char != "":
            if self.current_char.isnumeric() or self.current_char == ".":
                temp_str: str = ""
                is_float: bool = False
                
                while self.current_char.isnumeric() or (self.current_char == "." and is_float == False):
                    if self.current_char == ".":
                        is_float = True
                    temp_str += self.current_char
                    self.next_token()
                yield Constant(TokenType.CONSTANT, float(temp_str), is_float)
                continue
            elif self.current_char.isalpha():
                yield Variable(TokenType.VARIABLE, self.current_char)
            elif self.current_char in OPERATOR:
                yield Operator(TokenType[OP_DICT[self.current_char]], self.current_char)
            self.next_token()
        if self.current_char == "":
            yield Token(TokenType.EOF , "EOF")