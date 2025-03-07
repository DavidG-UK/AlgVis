import random
import math

def merge(data): # MUST BE NON RECURSIVE
    if len(data) > 1:
        m = len(data) // 2
        l = data[0:m]
        r = data[m:len(data)]

        l = merge(l)
        r = merge(r)

        left_index = 0
        right_index = 0

        merged = []
        while left_index < len(l) and right_index < len(r):
            if l[left_index] < r[right_index]:
                merged.append(l[left_index])
                left_index += 1
            else:
                merged.append(r[right_index])
                right_index += 1

        while left_index < len(l):
            merged.append(l[left_index])
            left_index += 1

        while right_index < len(r):
            merged.append(r[right_index])
            right_index += 1

        return merged
    return data

def binary(data, value):
    found = False
    left = 0
    right = len(data)

    while not found:
        mid = ((right - left) // 2) + left
        if data[mid] == value:
            return mid
        if data[mid] < value:
            left = mid
        else:
            right = mid

        if right - left == 1:
            return "not in list"

def linear(data, value):
    for i in range(len(data)):
        if data[i] == value:
            return i
        
        elif i + 1 == len(data):
            return "not in list"

def insertion(data):
    swapList = []
    for i in range(1, len(data)):
        current = data[i]
        prev_index = i - 1

        while prev_index >= 0 and current < data[prev_index]:
            data[prev_index + 1], data[prev_index] = data[prev_index], data[prev_index + 1]
            swapList.append([prev_index, prev_index + 1])
            prev_index -= 1
    
    return swapList

def bubble(data):
    swapList = []
    sort_completed = False
    while sort_completed == False:
        swaps = 0
        for i in range(len(data) - 1):
            if data[i] > data[i + 1]:
                swapList.append([i, i + 1])
                swaps += 1
                data[i], data[i + 1] = data[i + 1], data[i]

        if swaps == 0:
            sort_completed = True
    
    return swapList

def quickPartition(data, swapList, pointerList, lowValue, highValue):
    pointerPos = lowValue - 1
    pivot = data[highValue]
    pointerList.append([highValue, len(swapList)])
    for i in range(lowValue, highValue):
        if data[i] <= pivot:
            pointerPos += 1
            if i != pointerPos:
                data[i], data[pointerPos] = data[pointerPos], data[i]
                swapList.append([pointerPos, i])

    # if data[highValue] != data[pointerPos + 1]:
    if highValue != pointerPos + 1:
        data[highValue], data[pointerPos + 1] = data[pointerPos + 1], data[highValue]
        swapList.append([pointerPos + 1, highValue])

    return pointerPos + 1, data

def quick(data, swapList, pointerList, lowValue, highValue):
    if lowValue < highValue:
        pivot, data = quickPartition(data, swapList, pointerList, lowValue, highValue)

        quick(data, swapList, pointerList, lowValue, pivot - 1)
        quick(data, swapList, pointerList, pivot + 1, highValue)

    return swapList, pointerList

def Radix(data):
    buckets = []
    for i in range(10):
        buckets.append([])

    digitCount = len(str(max(data)))

    for i in range(len(data)):
        data[i] = str(data[i]).rjust(digitCount, "0")
    
    for i in range(digitCount, 0, -1):
        for j in range(len(data)):
            digit = int(data[j][i - 1])
            buckets[digit].append(data[j])

        data = []
        popIndex = 0

        while popIndex != 10:
            for j in range(len(buckets[popIndex])):
                data.append(buckets[popIndex][j])
            buckets[popIndex] = []
            popIndex += 1
        
    return data

def dijkstra(adjMatrix, root, goal):
    nodeTable = []
    goalPath = []
    nextNode = 0
    currentNode = root

    for i in range(len(adjMatrix)):
        nodeTable.append([2**50, False, None]) # distance from start, visited, previous node
    nodeTable[root][0], nodeTable[root][2] = 0, 0

    # dijkstra'ing
    while nextNode != -1:
        for i in range(len(adjMatrix[currentNode])):
            if (adjMatrix[currentNode][i] + nodeTable[currentNode][0]) < nodeTable[i][0] and adjMatrix[currentNode][i] != 0:
                nodeTable[i][0] = adjMatrix[currentNode][i] + nodeTable[currentNode][0]
                nodeTable[i][2] = currentNode
        nodeTable[currentNode][1] = True

        # selecting next node
        shortest = 2**50
        nextNode = -1
        for i in range(len(nodeTable)):
            if nodeTable[i][0] != 0 and nodeTable[i][0] < shortest and nodeTable[i][1] == False:
                shortest = nodeTable[i][0]
                nextNode = i

            currentNode = nextNode
    
    # building path
    if nodeTable[goal][1] == True:       
        pathNode = goal
        while pathNode != root:
            goalPath.append(pathNode)
            pathNode = nodeTable[pathNode][2]
        goalPath.append(root)
        goalPath.reverse()

    return goalPath, nodeTable

def generateMatrix(n):
    adjMatrix = []
    adjList = []
    for i in range(n):
        adjList = []
        for j in range(n):
            if random.randint(1, 3) == 1:
                adjList.append(random.randint(1, 100))
            else:
                adjList.append(0)
        adjMatrix.append(adjList)
    
    for i in range(n):
        adjMatrix[i][i] = 0

    for i in range(n):
        for j in range(n):
            adjMatrix[j][i] = adjMatrix[i][j]

    return adjMatrix

def Astar(adjMatrix, root, goal):
    nodeTable = []
    goalPath = []
    nextNode = 0
    currentNode = root

    for i in range(len(adjMatrix)):
        nodeTable.append([2**50, 0, False, None]) # distance from start, h(x), visited, previous node
    nodeTable[root][0], nodeTable[root][3] = 0, 0

    heurTable = dijkstra(adjMatrix, goal, root)[1]
    for i in range(len(heurTable)):
        nodeTable[i][1] = math.floor(heurTable[i][0] / 10) * 10

    while nodeTable[goal][2] == False and currentNode != -1:
        for i in range(len(adjMatrix[currentNode])):
            if (adjMatrix[currentNode][i] + nodeTable[currentNode][0]) < nodeTable[i][0] and adjMatrix[currentNode][i] != 0:
                nodeTable[i][0] = adjMatrix[currentNode][i] + nodeTable[currentNode][0]
                nodeTable[i][3] = currentNode
        nodeTable[currentNode][2] = True

        shortest = 2**50
        nextNode = -1
        for i in range(len(nodeTable)):
            if nodeTable[i][0] != 0 and nodeTable[i][0] + nodeTable[i][1] < shortest and nodeTable[i][2] == False:
                shortest = nodeTable[i][0] + nodeTable[i][1]
                nextNode = i

            currentNode = nextNode
    
        # building path
    if nodeTable[goal][2] == True:  
        pathNode = goal
        while pathNode != root:
            goalPath.append(pathNode)
            pathNode = nodeTable[pathNode][3]
        goalPath.append(root)
        goalPath.reverse()

    return goalPath, nodeTable

def greedyBFS(adjMatrix, root, goal):
    nodeTable = []
    goalPath = []
    nextNode = 0
    currentNode = root

    for i in range(len(adjMatrix)):
        nodeTable.append([2**50, 0, False, None]) # distance from start, h(x), visited, previous node
    nodeTable[root][0], nodeTable[root][3] = 0, 0

    heurTable = dijkstra(adjMatrix, goal, root)[1]
    for i in range(len(heurTable)):
        nodeTable[i][1] = math.floor(heurTable[i][0] / 10) * 10

    while nodeTable[goal][2] == False and currentNode != -1:
        for i in range(len(adjMatrix[currentNode])):
            if (adjMatrix[currentNode][i] + nodeTable[currentNode][0]) < nodeTable[i][0] and adjMatrix[currentNode][i] != 0:
                nodeTable[i][0] = adjMatrix[currentNode][i] + nodeTable[currentNode][0]
                nodeTable[i][3] = currentNode
        nodeTable[currentNode][2] = True

        shortest = 2**50
        nextNode = -1
        for i in range(len(nodeTable)):
            if nodeTable[i][0] != 0 and nodeTable[i][0] != 2**50 and nodeTable[i][1] < shortest and nodeTable[i][2] == False:
                shortest = nodeTable[i][1]
                nextNode = i

            currentNode = nextNode
    
        # building path
    if nodeTable[goal][2] == True:  
        pathNode = goal
        while pathNode != root:
            goalPath.append(pathNode)
            pathNode = nodeTable[pathNode][3]
        goalPath.append(root)
        goalPath.reverse()

    return goalPath, nodeTable
#print(insertion([11, 4, 6, 3, 12, 7, 2, 4, 4]))