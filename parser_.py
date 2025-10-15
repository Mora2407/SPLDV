from typing import Any
from dataclasses import dataclass
from lexer import *
from copy import copy

"""
E: T + E | T - E | T
T: F * T | F / T | F
F: -F | +F | (E)F | Fv | c | v
"""

"""
w/o left recursion, left factoring
E: T E' | ε
E': + T E' | - T E' | ε
T: F T'
T': * F T' | / F T' | ε
F: -F' | +F' | F'
F': -F' | +F' | (E) | (E)v | cv | c | v
"""

type token = Token | Constant | Variable | Operator

#Expression
@dataclass
class BNode:
    l_node: Any
    r_node: Any

@dataclass
class AddNode(BNode):
    def __repr__(self) -> str:
        return f"Add({self.l_node} + {self.r_node})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, AddNode):
            return self.l_node == other.l_node and self.r_node == other.r_node
        return False

@dataclass
class SubtractNode(BNode):
    def __repr__(self) -> str:
        return f"Subtract({self.l_node} - {self.r_node})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SubtractNode):
            return self.l_node == other.l_node and self.r_node == other.r_node
        return False

type expr_node = AddNode | SubtractNode

#Term
@dataclass
class MultiplyNode(BNode):
    def __repr__(self) -> str:
        return f"Multiply({self.l_node} * {self.r_node})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, MultiplyNode):
            return self.l_node == other.l_node and self.r_node == other.r_node
        return False
    
@dataclass
class DivideNode(BNode):
    def __repr__(self) -> str:
        return f"Divide({self.l_node} / {self.r_node})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DivideNode):
            return self.l_node == other.l_node and self.r_node == other.r_node
        return False

type term_node = MultiplyNode | DivideNode

#Factor
@dataclass
class Node:
    value: Any

@dataclass
class ConstantNode(Node):
    def __repr__(self) -> str:
        return f"({self.value.value})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ConstantNode):
            return self.value == other.value
        return False

@dataclass
class PlusNode(Node):
    def __repr__(self) -> str:
        return f"(+{self.value})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, PlusNode):
            return self.value == other.value
        return False

@dataclass
class MinusNode(Node):
    def __repr__(self) -> str:
        return f"-({self.value})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, MinusNode):
            return self.value == other.value
        return False

@dataclass
class VariableNode(Node):
    coefficient: Any
    def __repr__(self) -> str:
        return f"({self.coefficient}{self.value.value})"
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, VariableNode):
            return self.value == other.value and self.coefficient == other.coefficient
        return False

type fact_node = ConstantNode | PlusNode | MinusNode | VariableNode

type all_node = expr_node | term_node | fact_node

class Parser:
    def __init__(self, tokens: list[token]):
        self.tokens = iter(tokens)
        self.current_token: token = next(self.tokens)

    def __repr__(self):
        return f""

    def raise_error(self) -> None:
        raise Exception(f"Unexpected Token \"{self.current_token.value}\" after {self.token_before}")

    def next_token(self) -> None:
        try:
            self.token_before = copy(self.current_token)
            self.current_token = next(self.tokens)
        except StopIteration:
            self.token_before = copy(self.current_token)
            self.current_token = Token(TokenType.EOF, "EOF")

    def match_type(self, token_type: TokenType, advance: bool = True) -> bool:
        if self.current_token.type == token_type:
            if advance:
                self.next_token()
            return True
        else:
            return False
        
    def match_value(self, token_value: str | float, advance: bool = True) -> bool:
        if self.current_token.value == token_value:
            if advance:
                self.next_token()
            return True
        else:
            return False

    def parse(self) -> all_node | None:

        temp = self.expression() or Token(TokenType.EOF, "EOF")

        if self.match_type(TokenType.RPAREN):
            self.raise_error()
        elif self.match_type(TokenType.EQUAL):
            temp2 = self.expression() or Token(TokenType.EOF, "EOF")

            if self.match_type(TokenType.EQUAL, False):
                self.raise_error()

            return BNode(temp, temp2)

        return BNode(temp, Token(TokenType.EOF, "EOF"))

        
    def expression(self) -> None | all_node:

        node: None | all_node = self.term()

        if node == None:
            self.raise_error()
        
        while self.match_type(TokenType.PLUS, False) or self.match_type(TokenType.MINUS, False):
            temp_op = self.current_token

            self.next_token()

            if temp_op.type == TokenType.PLUS:
                node = AddNode(node, self.term())
            elif temp_op.type == TokenType.MINUS:
                node = SubtractNode(node, self.term())

        return node
        
    def term(self) -> None | all_node:

        node: None | all_node = self.factor()

        if node == None:
            self.raise_error()

        while self.match_type(TokenType.MULTIPLY, False) or self.match_type(TokenType.DIVIDE, False):
            temp_op = self.current_token

            self.next_token()

            if temp_op.type == TokenType.MULTIPLY:
                node = MultiplyNode(node, self.factor())
            elif temp_op.type == TokenType.DIVIDE:
                node = DivideNode(node, self.factor())
        
        if self.current_token.type == TokenType.CONSTANT or self.current_token.type == TokenType.VARIABLE:
            self.raise_error()
        
        return node

    def factor(self) -> None | all_node:
        
        if self.match_type(TokenType.PLUS):

            return PlusNode(self.factor())
        
        elif self.match_type(TokenType.MINUS):

            return MinusNode(self.factor())
        
        elif self.match_type(TokenType.CONSTANT, False):

            temp_tokens = copy(self.tokens)
            temp_current_token = copy(self.current_token)

            self.next_token()
            if self.match_type(TokenType.VARIABLE, False):
                temp = self.current_token
                self.next_token()
                return VariableNode(temp, ConstantNode(temp_current_token))

            self.tokens = temp_tokens
            self.current_token = temp_current_token

            temp = self.current_token
            self.next_token()

            return ConstantNode(temp)
        
        elif self.match_type(TokenType.VARIABLE, False):

            temp = self.current_token
            self.next_token()

            return VariableNode(temp, ConstantNode(Constant(TokenType.CONSTANT, 1.0, True)))
        
        elif self.match_type(TokenType.LPAREN):

            temp_expr = self.expression()

            if self.match_type(TokenType.RPAREN, False) or (self.match_type(TokenType.EOF) and self.token_before.type == TokenType.RPAREN):
                temp_tokens = copy(self.tokens)
                temp_current_token = copy(self.current_token)

                self.next_token()
                if self.match_type(TokenType.VARIABLE, False):
                    temp = self.current_token
                    self.next_token()
                    return VariableNode(temp, temp_expr)

                self.tokens = temp_tokens
                self.current_token = temp_current_token        

                self.next_token()

                return temp_expr
            
            self.raise_error()

        self.raise_error()