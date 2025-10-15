from lexer import Lexer
from parser_ import *
from evaluate import evaluate
from solver import Solver
import time
import statistics

tests = [
"-(3+1) * (3 - 1)x / 2 + --+456.789",
"1 * (2 + 3) * 4 - (1 + 3)x / 5",
"(1 + (2 + 3)x) * (1 / x)",
"1 + 2 * 1 / x",
"1 - (x - 1)",
"( ( (100 - 5*2) / 10 ) + --1 ) * ( 10x - (5+20)x ) - +-( 50 + 2x - 30 + 100/5 - 4x )",
"1 + 2 - 3 + 4",
"100 + ( (10 - (5 - x)) - (5 * -(2 - x)) ) / 2",
"(-((3x - (4 / 2)) * -5)) + ((10x - (x + 5) + ---20) / --2)",
"(10x - 20) / ( ((x + 1) * 5) - (-( (10 - 4x) / --2)) )",
"( ((5 * 4x) + (80 / 2)) / --(30 / 3) ) + x - ( (x - -x) + -(8 - (4 * 3)) )",
"( (-(x - 5x) - (5 * --4)) / (x + -(15/3)) ) + ( 2x - ( ((8x - 4x) / 2) + (3 * -(4/2)) ) )",
"(2x + 10) / (5 + x)",
"2 / ((x + 5) / (x  + 10))",
"((x + 1) / (x + 2)) * 2",
"( (15 / 5) * (x - 1) + (20 - (18 / 2)) ) - ( 5x - ((4x - 8) / 2) - 1 )",
"( (100 - 5x + ((10x - 30) / 2)) / (3x - (4x - (x+1))) ) * ( ((10x - 5) / 5) - (2 * (x - 0.5)) ) + 1",
"( ( (12x / 3 + x) - 10 ) / ( ((6*x)/(2*x)) - ((5*2)/(8/2)) ) ) + ( x - (-5 * ( (-( (12/3) - (16/2) )) - (x+x) )) )",
"(1/x ) + 2",
"( ( ( (5*4/2) - (16/2) ) + ( (10x/2) - (x*(6/2)) ) ) / x ) / ( ((5/5)/x) + (x/(2x-x)) )",
"((2 + 2x) / x) / ((1 + x) / x)",
"(1/x) * (1/(1/x))",
"(1 / x)x",
"( (x+1) / x ) * ( x / ( x + 1 ) )",
"1/x = 2",
"2 = 1/(x+1)",
"x / 2 + x / 3",
"3/2x - 1/x",
"1 + 1/x",
"3+2 = ((3/2x) - (1/x))/2",
"3/2x",
"x + 1 = 5",
"x - 12 = 30",
"7y = 49",
"1/x = 2/4",
"5a + 10 = 55",
"(z / 4) - 3 = 7",
"9x + 2 = 4x + 12",
"6 - 5b = 10 - 4b",
"3 * (k - 2) = k + 10",
"5 * (2 * p + 1) = 2 * (p + 3) - 7",
"(x / 3) + 2 = 5",
"(y / 2) + (y / 5) = 7",
"4 * (a + 1) + 2 = 4 * a + 7",
"2 * (3 * m + 5) = 6 * m + 10",
"2 * (x - 3) + 3 * (x - 2) = 8",
"5 * x - (2 * x - 8) = 2 * (x + 1)",
"3.12 * (2.3516 / x) = 234.1231 * --+++--(123.42341 - 7645674)",
"5/x * (x + x/2) = (123.12451 / 2342342)x",
"x/(246.246x+2) = 1/(123.123x+1)"
]

s = time.perf_counter()

data = []

for j in range(100000):
    start = time.perf_counter()
    
    for i in tests: 
        SOLVER = Solver(i)
        RESULT = SOLVER.solve()
    
    end = time.perf_counter()
    
    data.append(end - start)

#Mean
mean = statistics.mean(data)

#Standard Deviation
sd = statistics.stdev(data)

#Median
median = statistics.median(data)

#Maximum
maximum = max(data)

#Minimum
minimum = min(data)

e = time.perf_counter()

print(f"Test cases: {len(tests)}\nSample Size: {len(data)}\nMean: {mean}s\nMedian: {median}s\nStandard Deviation: {sd}s\nMaximum: {maximum}s\nMinimum: {minimum}s\n")

print(f"Elapsed Time: {e - s} seconds.")