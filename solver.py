from typing import Any
from lexer import Lexer
from parser_ import *
from evaluate import evaluate
from dataclasses import dataclass

@dataclass
class Answer:
    variable: str
    value: int
    note: str

    def __repr__(self):
        return f"{self.variable} = {self.value}\n{self.note}"
    

class Solver:
    def __init__(self, equation: str):
        self.equation = equation

        LEXER = Lexer(equation)
        TOKENS = list(LEXER.scan())

        PARSER = Parser(TOKENS)
        self.tree = PARSER.parse()

        
    def find(self):
        pass

    def solve(self):
        try:
            if self.tree.r_node.type == TokenType.EOF:
                return evaluate(self.tree.l_node)
        except AttributeError:
            pass

        self.tree = BNode(evaluate(self.tree.l_node), evaluate(self.tree.r_node))

        if (isinstance(self.tree.l_node, ConstantNode) and isinstance(self.tree.r_node, ConstantNode)) or ((isinstance(self.tree.l_node, VariableNode) and isinstance(self.tree.r_node, VariableNode))):
            if self.tree.l_node.value.value == self.tree.r_node.value.value:
                return Answer(self.tree.l_node.value.value, self.tree.r_node.value.value, "There are infinite solutions for x")
            elif self.tree.l_node.value.value != self.tree.r_node.value.value:
                return Answer(self.tree.l_node.value.value, self.tree.r_node.value.value, "There is no solution for x")

        elif isinstance(self.tree.l_node, ConstantNode) and isinstance(self.tree.r_node, VariableNode):
            value = evaluate(DivideNode(self.tree.l_node, self.tree.r_node.coefficient)).value.value
            return Answer(self.tree.r_node.value.value, value, f"The only solution for {self.tree.r_node.value.value} is {value}")
        
        elif isinstance(self.tree.l_node, VariableNode) and isinstance(self.tree.r_node, ConstantNode):
            value = evaluate(DivideNode(self.tree.r_node, self.tree.l_node.coefficient)).value.value
            return Answer(self.tree.l_node.value.value, value, f"The only solution for {self.tree.l_node.value.value} is {value}")

        elif isinstance(self.tree.l_node, DivideNode):
            self.tree.r_node = evaluate(MultiplyNode(self.tree.l_node.r_node, self.tree.r_node))
            self.tree.l_node = self.tree.l_node.l_node
            return self.solve()
        
        elif isinstance(self.tree.r_node, DivideNode):
            self.tree.l_node = evaluate(MultiplyNode(self.tree.r_node.r_node, self.tree.l_node))
            self.tree.r_node = self.tree.r_node.l_node
            return self.solve()
        
        elif isinstance(self.tree.r_node, AddNode):
            if isinstance(self.tree.r_node.l_node, VariableNode):
                self.tree.l_node = evaluate(AddNode(MinusNode(self.tree.r_node.l_node), self.tree.l_node))
                self.tree.r_node = self.tree.r_node.r_node
                return self.solve()
            elif isinstance(self.tree.r_node.r_node, VariableNode):
                self.tree.l_node = evaluate(AddNode(MinusNode(self.tree.r_node.r_node), self.tree.l_node))
                self.tree.r_node = self.tree.r_node.l_node
                return self.solve()

        elif isinstance(self.tree.l_node, AddNode):
            if isinstance(self.tree.l_node.l_node, ConstantNode):
                self.tree.r_node = evaluate(AddNode(MinusNode(self.tree.l_node.l_node), self.tree.r_node))
                self.tree.l_node = self.tree.l_node.r_node
                return self.solve()
            elif isinstance(self.tree.l_node.r_node, ConstantNode):
                self.tree.r_node = evaluate(AddNode(MinusNode(self.tree.l_node.r_node), self.tree.r_node))
                self.tree.l_node = self.tree.l_node.l_node
                return self.solve()

        return self.tree