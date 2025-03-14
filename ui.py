import random
import math
import Algorithms
import tkinter as tk
import networkx as nx
import matplotlib as mpl
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from ctypes import windll

timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)

window = tk.Tk()
# w, h = window.winfo_screenwidth(), window.winfo_screenheight()
# window.geometry("%dx%d+0+0" % (w, h))
window.state("zoomed")

window.configure(background="black")
tutButtons = [None, None, None]
rectIdData = []
bucketIdData = []
textIdData = []
defaultRadixPositions = []
externalButtons = {}
speed = 1

MAXSCREENWIDTH = 1300
MAXSCREENHEIGHT = 400
MAXBARWIDTH = 100
MAXBARHEIGHT = 200

options = [["Live Code Display", True, None], ["O(n)", True, None], ["O(n) description", True, None]] #name, enabled, button
ALGORITHMS = [["Linear Search", "placeholder text", "O(n)", "placeholder text"], #name, desc, O(n), O(n) desc
              ["Binary Search", "placeholder text", "O(log(n))", "placeholder text"], 
              ["Bubble Sort", "placeholder text", "O(n²)", "placeholder text"], 
              ["Insertion Sort", "placeholder text", "O(n²)", "placeholder text"], 
              ["Merge Sort", "placeholder text", "O(nlog(n))", "placeholder text"], 
              ["Quick Sort", "placeholder text", "O(nlog(n))", "placeholder text"], 
              ["Radix Sort", "placeholder text", "O(nd)", "placeholder text"], 
              ["Dijkstra's Pathfinding", "placeholder text", "O((V+E)log(V))", "placeholder text"],
              ["A* Pathfinding", "placeholder text", "O(V+E)", "placeholder text"],
              ["Greedy Best First Search", "placeholder text", "O(bᵐ)", "placeholder text"]]

def clearScreen(gridClear):
    for widget in window.winfo_children():
        widget.destroy()

    if gridClear:
        for i in range(window.grid_size()[0]):
            window.columnconfigure(i, weight=0)
        for i in range(window.grid_size()[1]):
            window.rowconfigure(i, weight=0)

def initialiseHome():
    clearScreen(True)
    
    window.columnconfigure((0, 2), weight=1, uniform="a")
    window.columnconfigure(1, weight=2, uniform="a")

    for i in range(10):
        if i == 3 or i == 5 or i == 7:
            window.rowconfigure(i, weight=3, uniform="a")
        else:
            window.rowconfigure(i, weight=2, uniform="a")

    algorithmButton = tk.Button(window, text="Algorithms", background="light blue", font=("Roboto Mono", 14, "bold"), command=initialiseAlgSelect)
    optionsButton = tk.Button(window, text="Options", background="light blue", font=("Roboto Mono", 14, "bold"), command=initialiseOptions)
    tutorialButton = tk.Button(window, text="Tutorial", background="light blue", font=("Roboto Mono", 14, "bold"), command=lambda tutStage = 0: displayTutorial(tutStage))
    titleLabel = ttk.Label(window, text="ALGVIS", background="black", anchor="center", font=("Roboto Mono", 30, "bold"), foreground="light blue")
    welcomeLabel = ttk.Label(window, text="Welcome to Algvis! here you can visualise many common algorithms", background="black", anchor="center", font=("Roboto Mono", 15, "bold"), foreground="light blue")

    algorithmButton.grid(row=3, column=1, sticky="nesw")
    optionsButton.grid(row=5, column=1, sticky="nesw")
    tutorialButton.grid(row=7, column=1, sticky="nesw")
    titleLabel.grid(row=0, column=1, sticky="nesw")
    welcomeLabel.grid(row=1, column=1, sticky="nesw")

def initialiseOptions():
    clearScreen(True)

    window.columnconfigure(0, weight=2, uniform="b")
    window.columnconfigure(1, weight=3, uniform="b")
    window.columnconfigure(2, weight=1, uniform="b")
    window.columnconfigure(3, weight=2, uniform="b")

    window.rowconfigure(0, weight=2, uniform="b")
    for i in range(1, len(options) * 2, 2):
        window.rowconfigure(i, weight=2, uniform="b")
        window.rowconfigure(i + 1, weight=1, uniform="b")
    
    displayBack("home", "nw")

    for i in range(len(options)):
        optionLabel = ttk.Label(window, text=options[i][0], background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
        optionLabel.grid(row=(i*2)+1, column=1, sticky="nesw")

        optionButton = tk.Button(window, background="green" if options[i][1] == True else "red", font=("Roboto Mono", 14, "bold"), command=lambda idx=i: updateButton(idx))
        options[i][2] = optionButton
        optionButton.grid(row=(i*2)+1, column=2, sticky="nesw")

def displayTutorial(stage):
    clearScreen(True)
    
    labelText = ["To enter the visualisation screen, click algorithms and then the algorithm you wish to visualise",
                 "To change what additional information is displayed, you can toggle options in the options menu", 
                 "To change the speed and data used in the algorithm, you can edit the taskbar as shown", 
                 "To view the algorithm you selected, click the play button and watch the visualisation",
                 "You can also view some additional information beneath the visualisation plane. You can \nturn these displays on or off in the options menu",
                 "graph",
                 "good luck and have fun!"]

    window.columnconfigure((0, 3), weight=1, uniform="f")
    window.columnconfigure((1, 2), weight=4, uniform="f")
    window.rowconfigure((0, 1, 4), weight=1, uniform="f")
    window.rowconfigure(2, weight=2, uniform="f")
    window.rowconfigure(3, weight=4, uniform="f")

    displayBack("home", "nw")
    expLabel = ttk.Label(window, text=labelText[stage], background="light blue", anchor="center", font=("Roboto Mono", 18, "bold"), foreground="black")
    expLabel.grid(row=2, column=1, sticky="nesw", columnspan=2)
    forward = tk.Button(window, text="⏵", background="white", font=("Roboto Mono", 14, "bold"), command=lambda stage = stage: displayTutorial(stage + 1) if stage < len(labelText) - 1 else initialiseHome())
    backward = tk.Button(window, text="⏴", background="white", font=("Roboto Mono", 14, "bold"), command=lambda stage = stage: displayTutorial(stage - 1) if stage > 0 else None)
    backward.grid(row=1, column=1, sticky="nesw")
    forward.grid(row=1, column=2, sticky="nesw")
    tutFrame = ttk.Frame(window)

    if stage == 0: # menu navigation
        tutFrame.columnconfigure((0, 2), weight=1, uniform="g")
        tutFrame.columnconfigure(1, weight=3, uniform="g")
        tutFrame.rowconfigure((0, 1, 2), weight=1, uniform="g")
        algorithmButton = tk.Button(tutFrame, text="Algorithms", background="light blue", font=("Roboto Mono", 14, "bold"))
        algorithmButton.grid(row=1, column=1, sticky="nesw")

    if stage == 1: # options tutorial
        tutFrame.columnconfigure(0, weight=2, uniform="h")
        tutFrame.columnconfigure(1, weight=3, uniform="h")
        tutFrame.columnconfigure(2, weight=1, uniform="h")
        tutFrame.columnconfigure(3, weight=2, uniform="h")

        tutFrame.rowconfigure(0, weight=2, uniform="h")
        for i in range(1, len(options) * 2, 2):
            tutFrame.rowconfigure(i, weight=2, uniform="h")
            tutFrame.rowconfigure(i + 1, weight=1, uniform="h")

        for i in range(len(options)):
            opLabel = ttk.Label(tutFrame, text=options[i][0], background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
            opLabel.grid(row=(i*2)+1, column=1, sticky="nesw")

            optionButton = tk.Button(tutFrame, background="green", font=("Roboto Mono", 14, "bold"), command=lambda idx=i: updateTutButton(idx))
            tutButtons[i] = optionButton
            optionButton.grid(row=(i*2)+1, column=2, sticky="nesw")
    
    if stage == 2: # taskbar tutorial
        tutFrame.rowconfigure((0, 2), weight=3, uniform="i")
        tutFrame.rowconfigure(1, weight=2, uniform="i")
        tutFrame.columnconfigure((0, 2), weight=1, uniform="i")
        tutFrame.columnconfigure(1, weight=10, uniform="i")
        taskFrame = createTaskbar(False, None, tutFrame, None)
        taskFrame.grid(row=1, column=1, sticky="nesw")
    
    if stage == 3: # visualisation tutorial
        tutFrame.rowconfigure(0, weight=1, uniform="j")
        tutFrame.rowconfigure(1, weight=2, uniform="j")
        tutFrame.rowconfigure(2, weight=4, uniform="j")
        tutFrame.columnconfigure((0, 2), weight=1, uniform="j")
        tutFrame.columnconfigure(1, weight=10, uniform="j")
        taskFrame = createTaskbar(False, None, tutFrame, None)
        planeLabel = ttk.Label(tutFrame, text="plane", background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
        taskFrame.grid(row=1, column=1, sticky="nesw")
        planeLabel.grid(row=2, column=1, sticky="nesw")
    if stage == 4:
        pass
        # do when visualisation is complete
    if stage == 6: # end
        tutFrame.rowconfigure(0, weight=1, uniform="l")
        tutFrame.columnconfigure(0, weight=1, uniform="l")
        smileLabel = ttk.Label(tutFrame, text=":D", background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
        smileLabel.grid(row=0, column=0, sticky="nesw")
    tutFrame.grid(row=3, column=1, sticky="nesw", columnspan=2)

def initialiseAlgSelect():
    clearScreen(True)

    algButtons = []

    window.columnconfigure((0, 1), weight=1, uniform="c")

    window.rowconfigure(0, weight=2, uniform="c")
    for i in range(1, len(ALGORITHMS) + 1):
        window.rowconfigure(i, weight=3, uniform="c")
    
    displayBack("home", "nw")

    for i in range(len(ALGORITHMS)):
        algButtons.append(tk.Button(window, text=ALGORITHMS[i][0], background="light blue", foreground="black", font=("Roboto Mono", 14, "bold"), command=lambda idx=i: displayAlgInfo(idx)))
        algButtons[i].grid(row=i+1, column=0, sticky="nesw")

def initialiseVisualisation(algidx):
    global visCanvas
    
    clearScreen(True) # removes all formatting and widgets

    algData = [356, 1293, 5544, 3298, 5098, 8812, 3795, 12] # random.randint(1, 50) for _ in range(10)
    window.columnconfigure(0, weight=1, uniform="d") 
    window.columnconfigure(1, weight=1, uniform="d")
    window.columnconfigure(2, weight=4, uniform="d")
    window.columnconfigure(3, weight=3, uniform="d")

    window.rowconfigure(0, weight=1, uniform="d")
    window.rowconfigure(1, weight=6, uniform="d")
    window.rowconfigure(2, weight=1, uniform="d")
    window.rowconfigure(3, weight=2, uniform="d")

    taskbar = createTaskbar(True, algidx, window, algData) # calls function to create taskbar frame
    visCanvas = tk.Canvas(window, bg='light grey')

    if algidx <= 5:
        setupCanvas(algData)
    else:
        setupRadix(algData)

    displayBack("algSelect", "nesw")
    gridFrame = ttk.Frame(window)
    gridFrame.rowconfigure(0, weight=1, uniform="k")
    gridFrame.columnconfigure(0, weight=1, uniform="k")

    gridFrame.grid(row=2, column=2, sticky="nesw", rowspan=2)
    taskbar.grid(row=0, column=1, sticky="nesw", columnspan=3)
    visCanvas.grid(row=1, column=0, sticky="nesw", columnspan=4)

    if options[0][1] == True: # display of optional featres
        codeFrame = tk.Frame(window)
        lineLabels = []
        codeFrame.columnconfigure(0, weight=1, uniform="f")
        codeFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform="f")
        currentLine = "placeholder text"
        for i in range(8):
            lineLabels.append(ttk.Label(codeFrame, text=currentLine, background="white", anchor="center", font=("Roboto Mono", 14), foreground="black"))
            lineLabels[i].grid(row=i, column=0, sticky="nesw")

        codeFrame.grid(row=2, column=3, rowspan=2, sticky="nesw")

    if options[1][1] == True:
        onLabel = ttk.Label(window, text=ALGORITHMS[algidx][2], background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
        onLabel.grid(row=2, column=0, rowspan=2 if options[2][1] == False else 1, columnspan=2, sticky="nesw")

    if options[2][1] == True:
        onDescLabel = ttk.Label(window, text=ALGORITHMS[algidx][3], background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
        onDescLabel.grid(row=3, column=0, columnspan=2, sticky="nesw")

def displayBack(backScreen, xyAlignment):
    if backScreen == "home":
        backButton = tk.Button(window, text="back", background="white", font=("Roboto Mono", 14, "bold"), command=initialiseHome)
    elif backScreen == "algSelect":
        backButton = tk.Button(window, text="back", background="white", font=("Roboto Mono", 14, "bold"), command=initialiseAlgSelect)
    backButton.grid(row=0, column=0, sticky=xyAlignment)

def updateSpeed(event):
    global speedScale, speed
    speed = speedScale.get()

def createTaskbar(active, algidx, master, algData):
    global speedScale, speed

    taskFrame = tk.Frame(master) # frame definition with formatting
    taskFrame.rowconfigure(0, weight=1, uniform="g")
    taskFrame.columnconfigure(0, weight=1, uniform="g")
    taskFrame.columnconfigure(1, weight=4, uniform="g")
    taskFrame.columnconfigure(2, weight=3, uniform="g")

    speedScale = tk.Scale(taskFrame, from_=0.1, to=10, orient="horizontal", variable=speed, command=updateSpeed, label="Execution speed", resolution=0.1)
    speedScale.set(speed)
    
    startButton = tk.Button(taskFrame, text="⏵", background="white", font=("Roboto Mono", 14, "bold"), command=lambda algIdx = algidx, data = algData: startAlgorithm(algIdx, data) if active == True else None) # creating widgets and defining behaviour
    externalButtons["startButton"] = startButton

    inputFrame = tk.Frame(taskFrame)

    inputFrame.columnconfigure(1, weight=3, uniform="e")
    inputFrame.columnconfigure((0, 2), weight=1, uniform="e")
    inputFrame.rowconfigure(0, weight=1, uniform="e")

    dataInput = tk.StringVar()
    entryBox = ttk.Entry(inputFrame, textvariable=dataInput)
    randomButton = tk.Button(inputFrame, text="Random", background="white", font=("Roboto Mono", 14, "bold"), command=lambda algIdx = algidx: validateCount(algIdx) if active == True else None)
    inputButton = tk.Button(inputFrame, text="Enter", background="white", font=("Roboto Mono", 14, "bold"), command=lambda input = dataInput, algIdx = algidx: validateData(input, algIdx) if active == True else None)

    inputButton.grid(row=0, column=0, sticky="nesw") # displaying widgets within frame
    entryBox.grid(row=0, column=1, sticky="nesw")
    randomButton.grid(row=0, column=2, sticky="nesw")

    startButton.grid(row=0, column=0, sticky="nesw")
    speedScale.grid(row=0, column=1, sticky="nesw")
    inputFrame.grid(row=0, column=2, sticky="nesw")
    return taskFrame

def setupCanvas(data):
    global visCanvas

    padX = 50
    rectIdData.clear()
    posCoords = []

    barWidth = math.floor((MAXSCREENWIDTH - (padX*2)) / ((len(data) * 2) - 1))
    if barWidth > 100:
        barWidth = 100

    largestElement = max(data)

    for i in range(len(data)):
        # x y x+wid y+wid
        x = padX + 2*i*barWidth
        y = MAXSCREENHEIGHT - MAXBARHEIGHT * (data[i] / largestElement)
        xWid = padX + ((2*i)+1)*barWidth 
        yWid = MAXSCREENHEIGHT
        rect = visCanvas.create_rectangle(int(x), int(y), int(xWid), int(yWid))
        rectIdData.append(rect)
        posCoords.append([x, y, xWid, yWid])

def verifySearchValue():
    value = simpledialog.askstring("tk", "What is the value of the element you wish to search for")

    if value == None:
        return None
    
    try:
        value = int(value)
    except:
        messagebox.showwarning(message="Please enter a single integer")
        return None

    if not isinstance(value, int):
        messagebox.showwarning(message="Please enter a single integer")
        return None
    
    return value
    
def searchVisualisation(data, pointerList, value, pointerIndex):
    global visCanvas, speed

    timePause = int(14/speed)
    if timePause == 0:
        timePause = 1

    for i in range(len(data)):
        visCanvas.itemconfig(rectIdData[i], fill="")

    if pointerIndex == len(pointerList) - 1:
        if data[pointerList[pointerIndex]] == value:
            visCanvas.itemconfig(rectIdData[0] + pointerList[pointerIndex], fill="light green")
        else:
            for i in range(len(data)):
                visCanvas.itemconfig(rectIdData[i], fill="red")
    else:
        visCanvas.itemconfig(rectIdData[0] + pointerList[pointerIndex], fill="red")
        pointerIndex += 1
        visCanvas.after(timePause * 100, searchVisualisation, data, pointerList, value, pointerIndex)

def moveBars(swapList, swapIndex, index, bPositions, aPositions, idOrder, pauseComplete):
    global visCanvas, speed
    timePause = int(14/speed)
    if timePause == 0:
        timePause = 1

    if swapIndex == len(swapList):
        for obj in idOrder:
            visCanvas.itemconfig(obj, fill="light green")

    elif swapList[swapIndex][1] == "pointer":         
        for obj in idOrder:
            visCanvas.itemconfig(obj, fill="")

        for i in range(len(swapList[swapIndex][0])):
            visCanvas.itemconfig(idOrder[swapList[swapIndex][0][i]], fill='red')
        visCanvas.after(timePause * 150, moveBars, swapList, swapIndex + 1, 0, bPositions, aPositions, idOrder, False)
    
    else:
        if aPositions == []:
            bPositions, aPositions, idOrder = createStages(swapList, swapIndex, rectIdData)

        visCanvas.itemconfig(idOrder[swapList[swapIndex][0][1]], fill='light blue')
        visCanvas.itemconfig(idOrder[swapList[swapIndex][0][0]], fill='light blue')

        if index < len(aPositions):
            bars = [idOrder[swapList[swapIndex][0][1]], idOrder[swapList[swapIndex][0][0]]] 
            visCanvas.move(bars[0], bPositions[index][0] - visCanvas.coords(bars[0])[0], bPositions[index][1] - visCanvas.coords(bars[0])[3])
            visCanvas.move(bars[1], aPositions[index][0] - visCanvas.coords(bars[1])[0], aPositions[index][1] - visCanvas.coords(bars[1])[3])
            index += 1
            visCanvas.after(timePause, moveBars, swapList, swapIndex, index ,bPositions, aPositions, idOrder, False)
        else:
            if not pauseComplete:
                visCanvas.after(timePause*20, moveBars, swapList, swapIndex, index ,bPositions, aPositions, idOrder, True)
            else:
                visCanvas.itemconfig(idOrder[swapList[swapIndex][0][1]], fill='')
                visCanvas.itemconfig(idOrder[swapList[swapIndex][0][0]], fill='')

                if swapIndex < len(swapList):
                    swapIndex += 1
                    visCanvas.after(timePause, moveBars, swapList, swapIndex, 0, [], [], idOrder, False)         

def createStages(swapList, swapIndex, idOrder):
    global visCanvas
    aStages = []
    bStages = []

    swapStages = [[1, 100], [1, 100], [2, visCanvas.coords(idOrder[swapList[swapIndex][0][1]])[0]], [0, visCanvas.coords(idOrder[swapList[swapIndex][0][0]])[0]], [3, MAXSCREENHEIGHT], [3, MAXSCREENHEIGHT]]
    
    bars = [[visCanvas.coords(idOrder[swapList[swapIndex][0][0]])[0], visCanvas.coords(idOrder[swapList[swapIndex][0][0]])[3]], [visCanvas.coords(idOrder[swapList[swapIndex][0][1]])[0], visCanvas.coords(idOrder[swapList[swapIndex][0][1]])[3]]]

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

    idOrder[swapList[swapIndex][0][0]], idOrder[swapList[swapIndex][0][1]] = idOrder[swapList[swapIndex][0][1]], idOrder[swapList[swapIndex][0][0]]
    return aStages, bStages, idOrder

def setupRadix(data):
    global visCanvas
    SPACING = 10
    padX = 100
    rectIdData.clear()
    
    availableSpace = MAXSCREENWIDTH - (2 * padX)
    textLength = len(str(max(data)))
    intermediatePauses = (len(data) - 1) * SPACING

    allocatedCharLength = math.floor((availableSpace - intermediatePauses) / (textLength * len(data)))

    bucketSpace = math.floor((availableSpace - 9*SPACING) / 10)
    if (textLength * allocatedCharLength) > bucketSpace:
        allocatedCharLength = int(bucketSpace / textLength)

    for i in range(len(data)):
        x, y = padX + (textLength * allocatedCharLength * i) + (SPACING * i), MAXSCREENHEIGHT - 300
        defaultRadixPositions.append([x, y])
        textIdData.append(visCanvas.create_text(x, y, text=str(data[i]).rjust(textLength, "0"), fill="black", font=("Roboto Mono", allocatedCharLength)))
    
    for i in range(10):
        bucketIdData.append(visCanvas.create_text(padX + (bucketSpace * i) + (SPACING * i), MAXSCREENHEIGHT - SPACING, text = str(i), fill="black", font=("Roboto Mono", 15)))
    
def radixVisualisation(data, swapList, swapIndex, stageIndex, stages, buckets):
    global visCanvas, speed
    timePause = int(14/speed)
    if timePause == 0:
        timePause = 1
    
    textX, textY = visCanvas.coords(swapList[swapIndex][0][0])[0], visCanvas.coords(swapList[swapIndex][0][0])[1]
    if stages == []:
        stages = animateMove(swapList[swapIndex], len(data), len(buckets[swapList[swapIndex][0][1]]), (swapIndex % len(data)) if swapIndex != 0 else len(data))

    if stageIndex == len(stages):
        visCanvas.after(timePause * 100, radixVisualisation, data, swapList, swapIndex + 1, stageIndex, stages, buckets)

    visCanvas.move(swapList[swapIndex][0][0], stages[stageIndex][0] - textX, stages[stageIndex][1] - textY)
    if stageIndex + 1 == len(stages):
        if swapList[swapIndex][1] == "move in":
            buckets[swapList[swapIndex][0][1]].append(swapList[swapIndex][0][0])
        else:
            del buckets[swapList[swapIndex][0][1]][0]
        visCanvas.after(timePause, radixVisualisation, data, swapList, swapIndex + 1, 0, [], buckets)
    else:
        visCanvas.after(timePause, radixVisualisation, data, swapList, swapIndex, stageIndex + 1, stages, buckets)

def animateMove(event, dataSize, bucketSize, dataLength):
    print(visCanvas.find_all(), visCanvas.coords(event[0][0]))
    textX, textY = visCanvas.coords(event[0][0])[0], visCanvas.coords(event[0][0])[1]
    bucketX, bucketY = visCanvas.coords(event[0][1] + dataSize + 1)[0], visCanvas.coords(event[0][1] + dataSize + 1)[1] - 20 - (30 * bucketSize)
    stages = []
    
    if event[1] == "move in":
        destX, destY = bucketX, bucketY
    else:
        destX, destY = defaultRadixPositions[dataLength][0], defaultRadixPositions[dataLength][1]

    if destX - textX >= 0:
        moveX = 5
    else:
        moveX = -5
    
    if destY - textY >= 0:
        moveY = 5
    else:
        moveY = -5

    if event[1] == "move in":
        for _ in range(10):
            textY += moveY
            stages.append([textX, textY])

        xStages, textX, textY = radixX(textX, destX, moveX, textY)
        for stage in xStages:
            stages.append(stage)
        yStages, textX, textY = radixY(textY, destY, moveY, textX)
        for stage in yStages:
            stages.append(stage)
    
    else:
        yStages, textX, textY = radixY(textY, destY, moveY, textX)
        for stage in yStages:
            stages.append(stage)
        xStages, textX, textY = radixX(textX, destX, moveX, textY)
        for stage in xStages:
            stages.append(stage)
    
    return stages

def radixX(textX, destX, moveX, textY):
    stages = []
    while textX != destX:
        reachedLimit = False
        if textX + moveX >= destX and moveX >= 0:
            reachedLimit = True
        elif textX + moveX <= destX and moveX <= 0:
            reachedLimit = True  

        if reachedLimit:
            textX = destX       
        elif textX + moveX != destX:
            textX += moveX
        
        stages.append([textX, textY])
    return stages, textX, textY

def radixY(textY, destY, moveY, textX):
    stages = []
    while textY != destY:
        reachedLimit = False
        if textY + moveY >= destY and moveY >= 0:
            reachedLimit = True
        elif textY + moveY <= destY and moveY <= 0:
            reachedLimit = True   

        if reachedLimit:
            textY = destY
        elif textY + moveY != destY:
            textY += moveY

        stages.append([textX, textY])
    return stages, textX, textY

def validateCount(algidx):
    valid = True
    count = simpledialog.askstring("tk", "How many random elements should be generated")

    if count == None:
        return
    
    try:
        count = int(count)
    except:
        messagebox.showwarning(message="Please enter a single integer")
        return None

    if not isinstance(count, int):
        messagebox.showwarning(message="Please enter a single integer")
        return None

    if count < 1 or count > 50:
        valid = False
        messagebox.showwarning(message="Please enter a number between 1 and 50")
    
    if valid == True:
        algData = []
        visCanvas.delete("all")
        for _ in range(count):
            if algidx == 6:
                algData.append(random.randint(1, 9999))
            else:
                algData.append(random.randint(1, 50))

        if algidx < 6:
            setupCanvas(algData)
        if algidx == 6:
            setupRadix(algData)

        if "startButton" in externalButtons:
            externalButtons["startButton"].config(command=lambda algIdx = algidx, data = algData: startAlgorithm(algIdx, data))

def validateData(userInput, algidx):
    userInput = userInput.get()
    data = None
    try:
        data = list(map(int, userInput.split(" ")))
    except:
        try:
            data = list(map(int, userInput.split(", ")))
            messagebox.showwarning(message="In future, please enter data in the form 'x y z'")
        except:
            try:
                data = list(map(int, userInput.split(",")))
                messagebox.showwarning(message="In future, please enter data in the form 'x y z'")
            except:
                messagebox.showwarning(message="entered data could not be read. please enter data in the form 'x y z'")
    
    if data != None:
        algData = data  
        visCanvas.delete("all")

        if algidx == 6:
            setupRadix(algData)
        else:
            setupCanvas(algData)

        if "startButton" in externalButtons:
            externalButtons["startButton"].config(command=lambda algIdx = algidx, data = algData: startAlgorithm(algIdx, data))

def displayAlgInfo(algidx):
    titleLabel = ttk.Label(window, text=ALGORITHMS[algidx][0], background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
    descLabel = ttk.Label(window, text=ALGORITHMS[algidx][1], background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
    visualiseButton = tk.Button(window, text="visualise!", background="light green", font=("Roboto Mono", 20, "bold"), command=lambda idx=algidx: initialiseVisualisation(idx))

    titleLabel.grid(row=1, column=1, sticky="nesw")
    descLabel.grid(row=2, column=1, sticky="nesw", rowspan=window.grid_size()[1] - 4)
    visualiseButton.grid(row=window.grid_size()[1] - 2, column=1, sticky="nesw", rowspan=2)

def updateButton(buttonIndex):
    if options[buttonIndex][1] == False:
        options[buttonIndex][1] = True
        options[buttonIndex][2].config(background="green")
    else:
        options[buttonIndex][1] = False
        options[buttonIndex][2].config(background="red")

def updateTutButton(bIdx):
    if tutButtons[bIdx].cget("bg") == "red":
        tutButtons[bIdx].config(background="green")
    else:
        tutButtons[bIdx].config(background="red")

def startAlgorithm(algIdx, data):
    global speed
    pointerList = []
    if algIdx <= 1:
        value = verifySearchValue()
    
    if algIdx == 0 and value != None:
        pointerList, value = Algorithms.linear(data, value)
    if algIdx == 1 and value != None:
        data = sorted(data)
        visCanvas.delete("all")
        setupCanvas(data)
        pointerList, value = Algorithms.binary(data, value)
    if algIdx == 2:
        swapList = Algorithms.bubble(data)
    elif algIdx == 3:
        swapList = Algorithms.insertion(data)
    elif algIdx == 4:
        swapList = Algorithms.mergeStart(data, [], 0, len(data) - 1)
    elif algIdx == 5:
        swapList = Algorithms.quick(data, [], 0, len(data) - 1)
    elif algIdx == 6:
        swapList = Algorithms.Radix(data, textIdData)

    if algIdx <= 1:
        searchVisualisation(data, pointerList, value, 0)
    if algIdx >= 2 and algIdx <= 5:
        moveBars(swapList, 0, 0, [], [], rectIdData, False)
    if algIdx == 6:
        radixVisualisation(data, swapList, 0, 0, [], [[] for _ in range(10)])

initialiseHome()
window.mainloop()