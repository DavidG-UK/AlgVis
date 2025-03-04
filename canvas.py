import tkinter as tk
import random
import math

window = tk.Tk()
window.geometry('1300x768')

window.columnconfigure(0, weight=1, uniform="a")
window.rowconfigure(0, weight=4, uniform="a")
window.rowconfigure(1, weight=1, uniform="a")

speed = 5
data = [2, 3, 1, 6, 5]
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
    
    swap(swapList, speed, 0, 0, [1, 2, 3, 4, 5])

def swap(swapList, speed, swapStage, swapIndex, idOrder):
    global afterTasks

    for task in afterTasks:
        window.after_cancel(task)
    afterTasks = []
    print("run")

    swapStages = [[1, 100], [1, 100], [2, canvas.coords(idOrder[swapList[swapIndex][1]])[2]], [0, canvas.coords(idOrder[swapList[swapIndex][0]])[0]], [3, MAXSCREENHEIGHT], [3, MAXSCREENHEIGHT]]

    if swapStage == 6:
        idOrder[swapList[swapIndex][0]], idOrder[swapList[swapIndex][1]] = idOrder[swapList[swapIndex][1]], idOrder[swapList[swapIndex][0]]
        swap(swapList, speed, 0, swapIndex + 1, idOrder)
    else:
        for i in range(2):
            update(idOrder[swapList[swapIndex][i]], swapStages[swapStage][0], swapStages[swapStage][1], speed, swapStage, idOrder, swapList, swapIndex)
            swapStage += 1

def update(obj, moveDir, limit, speed, swapStage, idOrder, swapList, swapIndex):
    global afterTasks
    if moveDir == 0: #left
        if canvas.coords(obj)[0] - 5 <= limit:
            canvas.move(obj, -(canvas.coords(obj)[0] - limit), 0)
            if swapStage % 2 == 0:
                swap(swapList, speed, swapStage + 2, swapIndex, idOrder)

        elif canvas.coords(obj)[0] != limit:
            canvas.move(obj, -5, 0)
            afterTasks.append(canvas.after(round((1 / speed) * 10), update, obj, moveDir, limit, speed, swapStage, idOrder, swapList, swapIndex))
    
    if moveDir == 1: #up
        if obj == 5 and swapIndex == 6:
            print(1)
        print(obj, canvas.coords(obj)[3], swapStage)
        if canvas.coords(obj)[3] - 5 <= limit:
            canvas.move(obj, 0, -(canvas.coords(obj)[3] - limit))
            if swapStage % 2 == 0:
                swap(swapList, speed, swapStage + 2, swapIndex, idOrder)

        elif canvas.coords(obj)[3] != limit:
            canvas.move(obj, 0, -5)
            afterTasks.append(canvas.after(round((1 / speed) * 10), update, obj, moveDir, limit, speed, swapStage, idOrder, swapList, swapIndex))

    if moveDir == 2: #right
        if canvas.coords(obj)[2] + 5 >= limit:
            canvas.move(obj, canvas.coords(obj)[2] - limit, 0)
            if swapStage % 2 == 0:
                swap(swapList, speed, swapStage + 2, swapIndex, idOrder)

        elif canvas.coords(obj)[2] != limit:
            canvas.move(obj, 5, 0)
            afterTasks.append(canvas.after(round((1 / speed) * 10), update, obj, moveDir, limit, speed, swapStage, idOrder, swapList, swapIndex))

    if moveDir == 3: #down
        if obj == 5 and swapIndex == 6:
            print(1)
        if canvas.coords(obj)[3] + 5 >= limit:
            canvas.move(obj, 0, canvas.coords(obj)[3] - limit)
            if swapStage % 2 == 0:
                swap(swapList, speed, swapStage + 2, swapIndex, idOrder)

        elif canvas.coords(obj)[3] != limit:
            canvas.move(obj, 0, 5)
            afterTasks.append(canvas.after(round((1 / speed) * 10), update, obj, moveDir, limit, speed, swapStage, idOrder, swapList, swapIndex))
  
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

canvas.itemconfig(rectIdData[0], fill="blue")
print(canvas.coords(5))

print(posCoords)

y = tk.Button(window, command=lambda speed = speed: bubble(data, speed))
y.grid(row=1, column=0, sticky="nesw")
window.mainloop()