import tkinter as tk
import math
import random
from ctypes import windll

timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)

window = tk.Tk()
window.geometry('1300x768')

window.columnconfigure(0, weight=1, uniform="a")
window.rowconfigure(0, weight=4, uniform="a")
window.rowconfigure(1, weight=1, uniform="a")

data = [random.randint(1, 30) for _ in range(8)]
print(data)
afterTasks = []
MAXSCREENWIDTH = 1300
MAXSCREENHEIGHT = 500
padX = 100 / 2
MAXBARWIDTH = 100
MAXBARHEIGHT = 200
rectIdData = []
posCoords = []
canvas = tk.Canvas(window, bg='light grey')
canvas.grid(row=0, column=0, sticky="nesw")

def bubble(data, speed):
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
    
    bPositions, aPositions, idOrder = createStages(swapList, 0, [(i + 1) for i in range(len(data))])
    if len(aPositions) != 0:
        moveBars(swapList, 0, 0, bPositions, aPositions, idOrder, False, speed)

def moveBars(swapList, swapIndex, index, bPositions, aPositions, idOrder, pauseComplete, speed):
    timePause = int((1/speed)*15)
    if timePause == 0:
        timePause = 1

    canvas.itemconfig(idOrder[swapList[swapIndex][1]], fill='light blue')
    canvas.itemconfig(idOrder[swapList[swapIndex][0]], fill='light blue')

    if index < len(aPositions):
        bars = [idOrder[swapList[swapIndex][1]], idOrder[swapList[swapIndex][0]]] 
        canvas.move(bars[0], bPositions[index][0] - canvas.coords(bars[0])[0], bPositions[index][1] - canvas.coords(bars[0])[3])
        canvas.move(bars[1], aPositions[index][0] - canvas.coords(bars[1])[0], aPositions[index][1] - canvas.coords(bars[1])[3])
        index += 1
        canvas.after(timePause, moveBars, swapList, swapIndex, index ,bPositions, aPositions, idOrder, False, speed)
    else:
        if not pauseComplete:
            canvas.after(timePause*20, moveBars, swapList, swapIndex, index ,bPositions, aPositions, idOrder, True, speed)
        else:
            canvas.itemconfig(idOrder[swapList[swapIndex][1]], fill='')
            canvas.itemconfig(idOrder[swapList[swapIndex][0]], fill='')
            swapIndex += 1
            if swapIndex < len(swapList):
                bPositions, aPositions, idOrder = createStages(swapList, swapIndex, idOrder)
                canvas.after(timePause, moveBars, swapList, swapIndex, 0, bPositions, aPositions, idOrder, False, speed)
            else:
                for obj in idOrder:
                    canvas.itemconfig(obj, fill="light green")

def createStages(swapList, swapIndex, idOrder):
    aStages = []
    bStages = []

    swapStages = [[1, 100], [1, 100], [2, canvas.coords(idOrder[swapList[swapIndex][1]])[0]], [0, canvas.coords(idOrder[swapList[swapIndex][0]])[0]], [3, MAXSCREENHEIGHT], [3, MAXSCREENHEIGHT]]
    
    bars = [[canvas.coords(idOrder[swapList[swapIndex][0]])[0], canvas.coords(idOrder[swapList[swapIndex][0]])[3]], [canvas.coords(idOrder[swapList[swapIndex][1]])[0], canvas.coords(idOrder[swapList[swapIndex][1]])[3]]]

    for i in range(len(swapStages)):
        limit = swapStages[i][1]
        odd = 1 if i % 2 == 1 else 0

        if i != 2 and i != 3:
            while bars[odd][1] != limit :
                if swapStages[i][0] == 1:
                    if bars[odd][1] - 5 <= limit:
                        bars[odd][1] = limit
                        aStages.append([bars[odd][0], bars[odd][1]]) if odd == 0 else bStages.append([bars[odd][0], bars[odd][1]])
                    elif bars[odd][1] != limit:
                        bars[odd][1] -= 5
                        aStages.append([bars[odd][0], bars[odd][1]]) if odd == 0 else bStages.append([bars[odd][0], bars[odd][1]])

                if swapStages[i][0] == 3:
                    if bars[odd][1] + 5 >= limit:
                        bars[odd][1] = limit
                        aStages.append([bars[odd][0], bars[odd][1]]) if odd == 0 else bStages.append([bars[odd][0], bars[odd][1]])
                    elif bars[odd][1] != limit:
                        bars[odd][1] += 5
                        aStages.append([bars[odd][0], bars[odd][1]]) if odd == 0 else bStages.append([bars[odd][0], bars[odd][1]])

        else:
            while bars[odd][0] != limit:
                if swapStages[i][0] == 0:
                    if bars[odd][0] - 5 <= limit:
                        bars[odd][0] = limit
                        aStages.append([bars[odd][0], bars[odd][1]]) if odd == 0 else bStages.append([bars[odd][0], bars[odd][1]])
                    elif bars[odd][0] != limit:
                        bars[odd][0] -= 5
                        aStages.append([bars[odd][0], bars[odd][1]]) if odd == 0 else bStages.append([bars[odd][0], bars[odd][1]])

                if swapStages[i][0] == 2:
                    if bars[odd][0] + 5 >= limit:
                        bars[odd][0] = limit
                        aStages.append([bars[odd][0], bars[odd][1]]) if odd == 0 else bStages.append([bars[odd][0], bars[odd][1]])
                    elif bars[odd][0] != limit:
                        bars[odd][0] += 5
                        aStages.append([bars[odd][0], bars[odd][1]]) if odd == 0 else bStages.append([bars[odd][0], bars[odd][1]])

    idOrder[swapList[swapIndex][0]], idOrder[swapList[swapIndex][1]] = idOrder[swapList[swapIndex][1]], idOrder[swapList[swapIndex][0]]
    return aStages, bStages, idOrder
  
swapStage = 0

barWidth = math.floor((MAXSCREENWIDTH - (padX*2)) / ((len(data) * 2) - 1))
if barWidth > 100:
    barWidth = 100

largestElement = max(data)

barHeight = math.floor
print(barWidth)

for i in range(len(data)):
    # x y x+wid y+wid
    x = padX + 2*i*barWidth
    y = MAXSCREENHEIGHT - MAXBARHEIGHT * (data[i] / largestElement)
    xWid = padX + ((2*i)+1)*barWidth 
    yWid = MAXSCREENHEIGHT
    rect = canvas.create_rectangle(int(x), int(y), int(xWid), int(yWid))
    rectIdData.append(rect)
    posCoords.append([x, y, xWid, yWid])

speed = 5
y = tk.Button(window, command=lambda speed = speed: bubble(data, speed))
y.grid(row=1, column=0, sticky="nesw")
window.mainloop()