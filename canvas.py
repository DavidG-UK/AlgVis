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

data = [random.randint(1, 30) for _ in range(20)]
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

