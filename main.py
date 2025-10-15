from lexer import Lexer
from parser_ import *
from evaluate import evaluate
from solver import Solver

string = ""

while string != "exit":
    string = input("> ")
    
    SOLVER = Solver(string)
    RESULT = SOLVER.solve()

    print(RESULT)