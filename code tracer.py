import sys
import Algortihms
import random
import math

linesExecuted = 0

def trace_lines(frame, event, arg):
    global current_line, linesExecuted
    if event == 'line':
        linesExecuted += 1
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        with open(filename) as f:
            current_line = f.readlines()[lineno - 1].strip()
            #print(f"Executing line {lineno}: {current_line}")
    return trace_lines

def estimate_On(numLines, dataInput):
    elementCount = dataInput
    complexities = [
        [1, "O(1)"],
        [math.log(elementCount), "O(log(n))"],
        [elementCount, "O(n)"],
        [elementCount * math.log(elementCount), "O(nlog(n)))"],
        [elementCount ** 2, "O(n²)"],
        [elementCount ** 3, "O(n³)"],
        [math.factorial(elementCount), "O(n!)"]
    ]

    for i in range(len(complexities)):
        if numLines < complexities[i][0]:
            #print(numLines)
            #print(complexities[i][0])
            #print(complexities[i][0] / numLines, numLines / complexities[i-1][0])
            return complexities[i]
    
#for i in range(2):
    # dataInput = []
    # linesExecuted = 0
    # for j in range(5 * (i+1)):
    #     dataInput.append(random.randint(1, 999))

N = 60
adjMatrix = Algortihms.generateMatrix(N)
sys.settrace(trace_lines)
#sorted = Algortihms.quick(dataInput)
goalpath, nodetable = Algortihms.Astar(adjMatrix, 0, N - 1)
sys.settrace(None)
On_complexity = estimate_On(linesExecuted, N)
print(linesExecuted, On_complexity) 
linesExecuted = 0
sys.settrace(trace_lines)
#sorted = Algortihms.quick(dataInput)
goalpath, nodetable = Algortihms.greedyBFS(adjMatrix, 0, N - 1)
sys.settrace(None)
On_complexity = estimate_On(linesExecuted, N)
print(linesExecuted, On_complexity)

    #print(goalpath, linesExecuted, On_complexity) # linesExecuted / On_complexity[0]