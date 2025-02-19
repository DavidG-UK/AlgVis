import sys
import time
import math
import Algorithms

linesExecuted = 0

def traceLines(frame, event, arg):
    global linesExecuted
    if event == 'line':
        linesExecuted += 1
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        with open(filename) as f:
            currentLine = f.readlines()[lineno - 1].strip()
            print(f"Executing line {lineno}: {currentLine}")
        time.sleep(0.5)
    return traceLines

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
            return complexities[i]

N = 5
adjMatrix = Algorithms.generateMatrix(N)

sys.settrace(traceLines)
goalpath, nodetable = Algorithms.Astar(adjMatrix, 0, N - 1)
sys.settrace(None)
print(linesExecuted)

linesExecuted = 0
sys.settrace(traceLines)
goalpath, nodetable = Algorithms.dijkstra(adjMatrix, 0, N - 1)
sys.settrace(None)
print(linesExecuted)
