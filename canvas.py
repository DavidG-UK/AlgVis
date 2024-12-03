import tkinter as tk
import math

window = tk.Tk()
window.geometry('1300x768')

window.columnconfigure(0, weight=1, uniform="a")
window.rowconfigure(0, weight=4, uniform="a")
window.rowconfigure(1, weight=1, uniform="a")

speed = 3
data = [2, 4, 8, 5, 1, 2, 4, 8, 5, 1]
MAXSCREENWIDTH = 1300
MAXSCREENHEIGHT = 500
padX = 100 / 2
MAXBARWIDTH = 100
MAXBARHEIGHT = 400
rectIdData = []
posCoords = []
canvas = tk.Canvas(window, bg='light grey')
canvas.grid(row=0, column=0, sticky="nesw")

def bubble(data):
    sort_completed = False
    while sort_completed == False:
        swaps = 0
        for i in range(len(data) - 1):
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                swap([data[i], i], [data[i + 1], 1])
                swaps += 1
        if swaps == 0:
            sort_completed = True
    
    return data

def swap(element1, element2):
    # for i in range(2):
    #     update
    return

def update(obj, moveDir, speed, limit):
    if moveDir == 0:
        if canvas.coords(obj)[0] - 5 < limit:
            canvas.move(obj, -(canvas.coords(obj)[0] - limit), 0)
        elif canvas.coords(obj)[0] != limit:
            canvas.move(obj, -5, 0)
            window.after(round((1 / speed) * 10), lambda obj = obj: update(obj, moveDir, speed, limit))
    
    if moveDir == 1:
        print(canvas.coords(obj), limit)
        if canvas.coords(obj)[1] - 5 < limit:
            canvas.move(obj, 0, -(canvas.coords(obj)[1] - limit))
        elif canvas.coords(obj)[1] != limit:
            canvas.move(obj, 0, -5)
            window.after(round((1 / speed) * 10), lambda obj = obj: update(obj, moveDir, speed, limit))

    if moveDir == 2:
        if canvas.coords(obj)[2] + 5 > limit:
            canvas.move(obj, canvas.coords(obj)[2] - limit, 0)
        elif canvas.coords(obj)[2] != limit:
            canvas.move(obj, 5, 0)
            window.after(round((1 / speed) * 10), lambda obj = obj: update(obj, moveDir, speed, limit))

    if moveDir == 3:
        if canvas.coords(obj)[3] + 5 > limit:
            canvas.move(obj, 0, canvas.coords(obj)[3] - limit)
        elif canvas.coords(obj)[3] != limit:
            canvas.move(obj, 0, 5)
            window.after(round((1 / speed) * 10), lambda obj = obj: update(obj, moveDir, speed, limit))


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
    rect = canvas.create_rectangle(x, y, xWid, yWid)
    rectIdData.append(rect)
    posCoords.append([x, y, xWid, yWid])

canvas.itemconfig(rectIdData[0], fill="blue")
print(canvas.coords(5))

print(posCoords)

moveMode = 2
rect = 5
y = tk.Button(window, command=lambda obj = rect, mode = moveMode, speed = speed: update(obj, mode, speed, 800))
bubble(data)
y.grid(row=1, column=0, sticky="nesw")
window.mainloop()