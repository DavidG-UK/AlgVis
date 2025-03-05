import tkinter as tk
import math

window = tk.Tk()
window.geometry('1300x768')

window.columnconfigure(0, weight=1, uniform="a")
window.rowconfigure(0, weight=4, uniform="a")
window.rowconfigure(1, weight=1, uniform="a")

speed = 5
data = [4, 5, 6, 2, 1]
MAXSCREENWIDTH = 1300
MAXSCREENHEIGHT = 500
padX = 100 / 2
MAXBARWIDTH = 100
MAXBARHEIGHT = 200
rectIdData = []
posCoords = []
canvas = tk.Canvas(window, bg='light grey')
canvas.grid(row=0, column=0, sticky="nesw")

def bubble(data, speed, swaps, index, idOrder):
    sort_completed = False
    if index == len(data) - 1:
        if swaps == 0:
            sort_completed = True
        else:
            index = 0

    if sort_completed == True:
        print("done")

    if data[index] > data[index + 1]:
        swap([idOrder[index], idOrder[index + 1]], speed, data, swaps, index, 0, idOrder)
    else:
        bubble(data, speed, swaps, (index + 1), idOrder)

def swap(rects, speed, data, swaps, index, swapStage, idOrder):
    swapStages = [[1, 100], [1, 100], [2, canvas.coords(rects[1])[2]], [0, canvas.coords(rects[0])[0]], [3, MAXSCREENHEIGHT], [3, MAXSCREENHEIGHT]]

    if swapStage == 6:
        idOrder[index], idOrder[index + 1] = idOrder[index + 1], idOrder[index]
        data[index], data[index + 1] = data[index + 1], data[index]
        swaps += 1
        bubble(data, speed, (swaps + 1), (index + 1), idOrder)
    else:
        for i in range(2):
            update(idOrder[index + i], [idOrder[index], idOrder[index + 1]], swapStages[swapStage][0], speed, swapStages[swapStage][1], data, swaps, index, swapStage, idOrder)
            swapStage += 1

def update(obj, rects, moveDir, speed, limit, data, swaps, index, swapStage, idOrder):
    import time
    print('this ran', time.time())

    if moveDir == 0: #left
        if canvas.coords(obj)[0] - 5 < limit:
            canvas.move(obj, -(canvas.coords(obj)[0] - limit), 0)
            if swapStage % 2 == 0:
                swap(rects, speed, data, swaps, index, swapStage + 2, idOrder)

        elif canvas.coords(obj)[0] != limit:
            canvas.move(obj, -5, 0)
            canvas.after(round((1 / speed) * 10), update, obj, rects, moveDir, speed, limit, data, swaps, index, swapStage, idOrder)
    
    if moveDir == 1: #up
        if canvas.coords(obj)[3] - 5 < limit:
            canvas.move(obj, 0, -(canvas.coords(obj)[3] - limit))
            if swapStage % 2 == 0:
                swap(rects, speed, data, swaps, index, swapStage + 2, idOrder)

        elif canvas.coords(obj)[3] != limit:
            canvas.move(obj, 0, -5)
            canvas.after(round((1 / speed) * 10), update, obj, rects, moveDir, speed, limit, data, swaps, index, swapStage, idOrder)

    if moveDir == 2: #right
        if canvas.coords(obj)[2] + 5 > limit:
            canvas.move(obj, canvas.coords(obj)[2] - limit, 0)
            if swapStage % 2 == 0:
                swap(rects, speed, data, swaps, index, swapStage + 2, idOrder)

        elif canvas.coords(obj)[2] != limit:
            canvas.move(obj, 5, 0)
            canvas.after(round((1 / speed) * 10), update, obj, rects, moveDir, speed, limit, data, swaps, index, swapStage, idOrder)

    if moveDir == 3: #down
        if canvas.coords(obj)[3] + 5 > limit:
            canvas.move(obj, 0, canvas.coords(obj)[3] - limit)
            if swapStage % 2 == 0:
                swap(rects, speed, data, swaps, index, swapStage + 2, idOrder)

        elif canvas.coords(obj)[3] != limit:
            canvas.move(obj, 0, 5)
            canvas.after(round((1 / speed) * 10), update, obj, rects, moveDir, speed, limit, data, swaps, index, swapStage, idOrder)

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

y = tk.Button(window, command=lambda speed = speed: bubble(data, speed, 0, 0, [1, 2, 3, 4, 5]))
y.grid(row=1, column=0, sticky="nesw")
window.mainloop()