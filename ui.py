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
window.state("zoomed")

window.config(background="black")
tutButtons = [None, None, None]
rectIdData = []
bucketIdData = []
textIdData = []
defaultRadixPositions = []
defaultData = [[12, 17, 6, 2, 5, 5, 8, 13, 12, 3, 15, 4], [6753, 1476, 9517, 5249, 2584, 8462, 6753, 6038, 1069, 2988, 6968, 8339]]

externalWidgets = {}
speed = 1
inProgress = False
newData = False
options = [["Live Process Display", True, None], ["O(n)", True, None], ["O(n) description", True, None]] #name, enabled, button

MAXSCREENWIDTH = 1300
MAXSCREENHEIGHT = 400
MAXBARWIDTH = 100
MAXBARHEIGHT = 200
ALGORITHMS = [["Linear Search", "A search algorithm that checks each element in a list\n sequentially, querying whether it is the same as a search value\n and returing it if true.", "O(n)", "Linear search iterates over each\n element once"], #name, desc, O(n), O(n) desc
              ["Binary Search", "A divide and conquer search algorithm that uses a sorted list.\n The middle element in the list is chosen and compared to the\n search value and half the list is discarded each time depending\n on whether the middle element is bigger than the search value or not.", "O(log(n))", "Binary search is a divide and\n conquer algorithm"], 
              ["Bubble Sort", "A sort which compares two adjacent elements and swaps them if\n they are out of order. This process repeats for multiple iterations\n until the list is sorted.", "O(n²)", "Bubble search has several\n passes in which it iterates over\n elements"], 
              ["Insertion Sort", "A sort that takes elements from a main list and places them in\n the correct place in a single sorted sublist.", "O(n²)", "Insertion sort searches for\n where to place elements in\n a sorted list n times (n * n)"], 
              ["Merge Sort", "A sort that divides the list until each element is in its own sublist.\n Each small sublist is merged, with elements being placed in the\n correct order.", "O(nlog(n))", "Merge sort divides the list and\n then merges them (logn * n)"], 
              ["Quick Sort", "A sort that chooses a pivot element and moves all elements\n smaller and larger than it to different sublists. A divide and conquer\n approach is used to continue selecting pivots until the data is sorted.", "O(nlog(n))", "Quick sort partitions the list\n logn times and then checks\n each element"], 
              ["Radix Sort", "A sort that uses several numbered buckets from 0 to 9. Each\n element is placed in a bucket based on the value of a selected digit\n (starting from least significant and progressing to most significant)\n and then dequeued out of them after each iteration.", "O(nd)", "Radix sort adds each element to\n a bucket d times\n (d is number of digits)"], 
              ["Dijkstra's Pathfinding", "A pathfinding algorithm that sequentially visits the nearest unvisited\n node until the correct node is found. Then the path that was taken\n to get there is returned.", "O((V+E)log(V))", "placeholder text"],
              ["A* Pathfinding", "A pathfinding algorithm that visits the next most promising node\n through the use of heuristic values and the distance from the start.\n Once the correct node is found the path that was taken to get\n there is returned.", "O(V+E)", "placeholder text"],
              ["Greedy Best First Search", "A pathfinding algorithm that selects the unvisited node with the\n lowest heuristic value. This continues until the correct node is found.\n Then the path that was taken is returned.", "O(bᵐ)", "placeholder text"]]

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
    window.config(background="black")
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
    global planeCanvas
    clearScreen(True)
    
    labelText = ["To enter the visualisation screen, click algorithms and then the algorithm you wish to visualise",
                 "To change what additional information is displayed, you can toggle options in the options menu", 
                 "To change the speed and data used in the algorithm, you can edit the taskbar as shown", 
                 "To view the algorithm you selected, click the play button and watch the visualisation",
                 "You can also view some additional information beneath the visualisation plane. You can \nturn these displays on or off in the options menu",
                 "good luck and have fun!"]

    window.columnconfigure((0, 3), weight=1, uniform="f")
    window.columnconfigure((1, 2), weight=4, uniform="f")
    window.rowconfigure((0, 1, 4), weight=1, uniform="f")
    window.rowconfigure(2, weight=2, uniform="f")
    window.rowconfigure(3, weight=4, uniform="f")

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
        tutFrame.columnconfigure(0, weight=1, uniform="i")
        taskFrame = createTaskbar(False, None, tutFrame, None)
        taskFrame.grid(row=1, column=0, sticky="nesw")
    
    if stage == 3: # visualisation tutorial
        tutFrame.rowconfigure(0, weight=1, uniform="j")
        tutFrame.rowconfigure(1, weight=2, uniform="j")
        tutFrame.rowconfigure(2, weight=4, uniform="j")
        tutFrame.columnconfigure(0, weight=1, uniform="j")
        taskFrame = createTaskbar(False, None, tutFrame, None)
        planeCanvas = tk.Canvas(tutFrame, bg="light grey")
        tutRects = []
        for i in range(3):
            tutRects.append(planeCanvas.create_rectangle(((planeCanvas.winfo_reqwidth()/2) + 100*(i-1)), 50, ((planeCanvas.winfo_reqwidth()/2) + 100*(i-1) + 50), 150))
        externalWidgets["TutorialRects"] = tutRects
        taskFrame.grid(row=1, column=0, sticky="nesw")
        planeCanvas.grid(row=2, column=0, sticky="nesw")

    if stage == 4:
        tutFrame.columnconfigure((0, 4), weight=1, uniform="j")
        tutFrame.columnconfigure((1, 3), weight=4, uniform="j")
        tutFrame.columnconfigure(2, weight=1, uniform="j")
        tutFrame.rowconfigure((0, 1, 2, 3), weight=1, uniform="j")

        exampleText = ["Selecting pointer", "Starting next swap", "Swapping elements as left element is bigger than right element", "Selecting pointer", "Selecting pointer", "Starting next swap","Swapping elements as left element is bigger than right element", "Starting next swap"]
        processFrame = tk.Frame(tutFrame)
        processFrame.columnconfigure(0, weight=1, uniform="j")
        processFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform="j")
        for i in range(8):
            ttk.Label(processFrame, text=exampleText[i], background="white" if i != 0 else "light blue", anchor="center", font=("Roboto Mono", 10, "bold"), foreground="black").grid(row=i, column=0, sticky="nesw")
        
        processFrame.grid(row=1, column=3, rowspan=2, sticky="nesw")

        onLabel = ttk.Label(tutFrame, text=ALGORITHMS[3][2], background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
        onLabel.grid(row=1, column=1, sticky="nesw")

        onDescLabel = ttk.Label(tutFrame, text=ALGORITHMS[3][3], background="white", anchor="center", font=("Roboto Mono", 10, "bold"), foreground="black")
        onDescLabel.grid(row=2, column=1, sticky="nesw")

    if stage == 5: # end
        tutFrame.rowconfigure(0, weight=1, uniform="l")
        tutFrame.columnconfigure(0, weight=1, uniform="l")
        smileLabel = ttk.Label(tutFrame, text=":D", background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
        smileLabel.grid(row=0, column=0, sticky="nesw")
    
    displayBack("home", "nesw")
    tutFrame.grid(row=3, column=1, sticky="nesw", columnspan=2)

def tutorialStartCommand():
    global planeCanvas
    for i in range(len(externalWidgets["TutorialRects"])):
        planeCanvas.itemconfig(externalWidgets["TutorialRects"][i], fill="light blue")
    
def initialiseAlgSelect():
    clearScreen(True)
    window.config(background="black")

    algButtons = []

    window.columnconfigure((0, 1), weight=1, uniform="c")

    window.rowconfigure(0, weight=2, uniform="c")
    for i in range(1, len(ALGORITHMS) + 1):
        window.rowconfigure(i, weight=3, uniform="c")
    
    displayBack("home", "nw")

    for i in range(len(ALGORITHMS)):
        algButtons.append(tk.Button(window, text=ALGORITHMS[i][0], background="light blue", foreground="black", font=("Roboto Mono", 14, "bold"), command=lambda idx=i: displayAlgInfo(idx)))
    for j in range(len(algButtons)):
        algButtons[j].grid(row=j+1, column=0, sticky="nesw")

def displayAlgInfo(algidx):
    titleLabel = ttk.Label(window, text=ALGORITHMS[algidx][0], background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
    descLabel = ttk.Label(window, text=ALGORITHMS[algidx][1], background="white", anchor="center", font=("Roboto Mono", 15), foreground="black")
    visualiseButton = tk.Button(window, text="Visualise!" if algidx <= 6 else "Coming soon", background="light green" if algidx <= 6 else "#CBC3E3", font=("Roboto Mono", 20, "bold"), command=lambda idx=algidx: initialiseVisualisation(idx) if algidx <= 6 else None)

    titleLabel.grid(row=1, column=1, sticky="nesw")
    descLabel.grid(row=2, column=1, sticky="nesw", rowspan=window.grid_size()[1] - 4)
    visualiseButton.grid(row=window.grid_size()[1] - 2, column=1, sticky="nesw", rowspan=2)

def initialiseVisualisation(algidx):
    global visCanvas
    
    clearScreen(True) # removes all formatting and widgets
    algData = defaultData[0].copy() if algidx != 6 else defaultData[1].copy()
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
    window.config(background="light grey")

    if options[0][1] == True: # display of optional featres
        lineLabels = []
        codeFrame = tk.Frame(window)
        codeFrame.columnconfigure(0, weight=1, uniform="f")
        codeFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform="f")
        for i in range(8):
            lineLabels.append(ttk.Label(codeFrame, text="", background="white", anchor="center", font=("Roboto Mono", 10, "bold"), foreground="black"))
            lineLabels[i].grid(row=i, column=0, sticky="nesw")

        externalWidgets["textLabels"] = [lineLabels[i] for i in range(len(lineLabels))]
        codeFrame.grid(row=2, column=3, rowspan=2, sticky="nesw")

    if options[1][1] == True:
        onLabel = ttk.Label(window, text=ALGORITHMS[algidx][2], background="white", anchor="center", font=("Roboto Mono", 20, "bold"), foreground="black")
        onLabel.grid(row=2, column=0, rowspan=2 if options[2][1] == False else 1, columnspan=2, sticky="nesw")

    if options[2][1] == True:
        onDescLabel = ttk.Label(window, text=ALGORITHMS[algidx][3], background="white", anchor="center", font=("Roboto Mono", 10, "bold"), foreground="black")
        onDescLabel.grid(row=3, column=0, columnspan=2, sticky="nesw")

    if algidx <= 5:
        setupCanvas(algData)
    else:
        setupRadix(algData)

    setupKeyFrame(algidx, algData)

    taskbar.grid(row=0, column=1, sticky="nesw", columnspan=3)
    visCanvas.grid(row=1, column=0, sticky="nesw", columnspan=4)

def setupKeyFrame(algidx, algData):
    keyFrame = ttk.Frame(window)
    if algidx != 6:
        keyFrame.rowconfigure((0, 1, 2), weight=1, uniform="l")
        keyFrame.columnconfigure(1, weight=1, uniform="l") 
        keyFrame.columnconfigure(0, weight=2, uniform="l")
        keyFrame.columnconfigure(2, weight=5, uniform="l")
    else:
        keyFrame.rowconfigure((0, 1), weight=1, uniform="l")
        keyFrame.columnconfigure(0, weight=1, uniform="l")

        textFrame = ttk.Frame(keyFrame)
        textFrame.rowconfigure(0, weight=1, uniform="m")
        for i in range(len(str(max(algData)))):
            textFrame.columnconfigure(i+1, weight=1, uniform="m")
        
        textFrame.columnconfigure((0, i+2), weight=1, uniform="m")
        textFrame.grid(row=0, column=0, sticky="nesw")

        subKeyFrame = ttk.Frame(keyFrame)
        subKeyFrame.rowconfigure((0, 1, 2), weight=1, uniform="n")
        subKeyFrame.columnconfigure(0, weight=2, uniform="n")
        subKeyFrame.columnconfigure(1, weight=1, uniform="n")
        subKeyFrame.columnconfigure(2, weight=5, uniform="n")
        subKeyFrame.grid(row=1, column=0, sticky="nesw")

    if algidx == 0 or algidx == 1:
        red = ttk.Label(keyFrame, text="", background="red").grid(row=0, column=0, sticky="nesw")
        green = ttk.Label(keyFrame, text="", background="light green").grid(row=1, column=0, sticky="nesw")
        redDesc = ttk.Label(keyFrame, text="Pointer, Element not found", font=("Roboto Mono", 10, "bold")).grid(row=0, column=2, sticky="nesw")
        greenDesc = ttk.Label(keyFrame, text="Element Found", font=("Roboto Mono", 10, "bold")).grid(row=1, column=2, sticky="nesw")

    if algidx == 2 or algidx == 3:
        blue = ttk.Label(keyFrame, text="", background="light blue").grid(row=0, column=0, sticky="nesw")
        green = ttk.Label(keyFrame, text="", background="light green").grid(row=1, column=0, sticky="nesw")
        blueDesc = ttk.Label(keyFrame, text="Bar swapping", font=("Roboto Mono", 10, "bold")).grid(row=0, column=2, sticky="nesw")
        greenDesc = ttk.Label(keyFrame, text="Sort completed", font=("Roboto Mono", 10, "bold")).grid(row=1, column=2, sticky="nesw")

    if algidx == 4 or algidx == 5:
        blue = ttk.Label(keyFrame, text="", background="light blue").grid(row=0, column=0, sticky="nesw")
        green = ttk.Label(keyFrame, text="", background="light green").grid(row=1, column=0, sticky="nesw")
        red = ttk.Label(keyFrame, text="", background="red").grid(row=2, column=0, sticky="nesw")
        blueDesc = ttk.Label(keyFrame, text="Bar swapping", font=("Roboto Mono", 10, "bold")).grid(row=0, column=2, sticky="nesw")
        greenDesc = ttk.Label(keyFrame, text="Sort completed", font=("Roboto Mono", 10, "bold")).grid(row=1, column=2, sticky="nesw")
        redDesc = ttk.Label(keyFrame, text="Pointer", font=("Roboto Mono", 10, "bold")).grid(row=2, column=2, sticky="nesw")

    if algidx == 6:
        index = 0
        keyDigits = []
        for i in range(len(str(max(algData)))):
            keyDigits.append(ttk.Label(textFrame, text=str(index), font=("Roboto Mono", 15, "bold")))
            keyDigits[i].grid(row=0, column=(i+1), sticky="nesw")
            if index == 9:
                index = 0
            else:
                index += 1
        
        externalWidgets["keyDigits"] = keyDigits
        
        blue = ttk.Label(subKeyFrame, text="", background="blue").grid(row=0, column=0, sticky="nesw")
        green = ttk.Label(subKeyFrame, text="", background="green").grid(row=1, column=0, sticky="nesw")   
        blueDesc = ttk.Label(subKeyFrame, text="Element being moved into or out of bucket", font=("Roboto Mono", 10, "bold")).grid(row=0, column=2, sticky="nesw")
        greenDesc = ttk.Label(subKeyFrame, text="Sort completed", font=("Roboto Mono", 10, "bold")).grid(row=1, column=2, sticky="nesw")

    keyFrame.grid(row=2, column=2, sticky="nesw", rowspan=2)

def updatelineText(data):
    global lineText
    if options[0][1] == True:
        if data != None:
            lineText.insert(0, data)
            if len(lineText) >= 9:
                lineText.pop()
        else: 
            lineText = ["" for _ in range(8)]

        for i in range(len(externalWidgets["textLabels"])):
            externalWidgets["textLabels"][i].config(text=lineText[i])

        if lineText[0] != "":
            externalWidgets["textLabels"][0].config(background = "light blue")

def displayBack(backScreen, xyAlignment):
    if backScreen == "home":
        backButton = tk.Button(window, text="back", background="white", font=("Roboto Mono", 14, "bold"), command=initialiseHome)
    elif backScreen == "algSelect":
        backButton = tk.Button(window, text="back", background="white", font=("Roboto Mono", 14, "bold"), command=initialiseAlgSelect)
    backButton.grid(row=0, column=0, sticky=xyAlignment)

def createTaskbar(active, algidx, master, algData):
    global speedScale, speed

    taskFrame = tk.Frame(master) # frame definition with formatting
    taskFrame.rowconfigure(0, weight=1, uniform="g")
    taskFrame.columnconfigure(0, weight=1, uniform="g")
    taskFrame.columnconfigure(1, weight=4, uniform="g")
    taskFrame.columnconfigure(2, weight=3, uniform="g")

    speedScale = tk.Scale(taskFrame, from_=0.1, to=10, orient="horizontal", variable=speed, command=updateSpeed, label="Execution speed", resolution=0.1)
    speedScale.set(speed)

    startButton = tk.Button(taskFrame, text="⏵", background="white", font=("Roboto Mono", 14, "bold"), command=lambda algIdx = algidx, data = algData: startAlgorithm(algIdx, data) if active == True else tutorialStartCommand()) # creating widgets and defining behaviour

    externalWidgets["startButton"] = startButton

    if active == True:
        displayBack("algSelect", "nesw") 

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
    speedScale.grid(row=0, column=1, sticky="nesw")
    inputFrame.grid(row=0, column=2, sticky="nesw")
    startButton.grid(row=0, column=0, sticky="nesw")

    return taskFrame

def updateSpeed(event):
    global speedScale, speed
    speed = speedScale.get()
    
def pauseAlgorithm():
    global inProgress
    inProgress = False
    externalWidgets["startButton"].config(text = "⏵", command=lambda: resumeAlgorithm())

def resumeAlgorithm():
    global inProgress
    inProgress = True
    externalWidgets["startButton"].config(text = "⏸", command=lambda: pauseAlgorithm())

def endAlgorithm(algidx):
    global inProgress
    inProgress = False
    externalWidgets["startButton"].config(text = "⟳", command=lambda algIdx = algidx: restartAlgortihm(algIdx))

def restartAlgortihm(algidx):
    data = defaultData[0].copy() if algidx != 6 else defaultData[1].copy()
    visCanvas.delete("all")
    setupCanvas(data) if algidx != 6 else setupRadix(data)
    startAlgorithm(algidx, data)

def setupCanvas(data):
    global visCanvas, inProgress, newData
    
    inProgress = False
    newData = False
    updatelineText(None)

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
    global inProgress
    value = simpledialog.askstring("tk", "What is the value of the element you wish to search for")

    if inProgress == True:
        messagebox.showwarning(message="Please pause the algorithm or wait for it to finish before entering a search value")
        return None
    
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
    
def searchVisualisation(data, pointerList, value, pointerIndex, algidx):
    global visCanvas, speed, newData

    timePause = int(14/speed)
    if timePause == 0:
        timePause = 1

    if inProgress == True:
        for i in range(len(data)):
            visCanvas.itemconfig(rectIdData[i], fill="")

        if pointerIndex == len(pointerList) - 1:
            if data[pointerList[pointerIndex]] == value:
                updatelineText("Element found, ending algorithm")
                visCanvas.itemconfig(rectIdData[0] + pointerList[pointerIndex], fill="light green")
                endAlgorithm(algidx)
            else:
                updatelineText("Element not found in list, ending algorithm")
                for i in range(len(data)):
                    visCanvas.itemconfig(rectIdData[i], fill="red")
                endAlgorithm(algidx)
        else:
            if algidx == 0:
                updatelineText("Checking next element in list")
            else:
                if pointerList[pointerIndex + 1] > pointerList[pointerIndex]:
                    updatelineText("Discarding smaller half, checking next element")
                else:
                    updatelineText("Discarding larger half, checking next element")
            visCanvas.itemconfig(rectIdData[0] + pointerList[pointerIndex], fill="red")
            pointerIndex += 1
            visCanvas.after(timePause * 100, searchVisualisation, data, pointerList, value, pointerIndex, algidx)

    elif newData == False:
        visCanvas.after(200, searchVisualisation, data, pointerList, value, pointerIndex, algidx)
    else:
        newData = False

def moveBars(swapList, swapIndex, index, bPositions, aPositions, idOrder, pauseComplete, algidx):
    global visCanvas, speed, inProgress, newData
    timePause = int(14/speed)
    if timePause == 0:
        timePause = 1

    if inProgress == True:
        if swapIndex == len(swapList):
            updatelineText("List is sorted, ending algorithm")
            for obj in idOrder:
                visCanvas.itemconfig(obj, fill="light green")
            endAlgorithm(algidx)

        elif swapList[swapIndex][1] == "pointer":         
            for obj in idOrder:
                visCanvas.itemconfig(obj, fill="")

            updatelineText("Selecting pointer")
            for i in range(len(swapList[swapIndex][0])):
                visCanvas.itemconfig(idOrder[swapList[swapIndex][0][i]], fill='red')
            visCanvas.after(timePause * 150, moveBars, swapList, swapIndex + 1, 0, bPositions, aPositions, idOrder, False, algidx)
        
        else:
            if aPositions == []:
                updatelineText("Swapping elements as left element is bigger than right element")
                bPositions, aPositions, idOrder = createStages(swapList, swapIndex, rectIdData)

            visCanvas.itemconfig(idOrder[swapList[swapIndex][0][1]], fill='light blue')
            visCanvas.itemconfig(idOrder[swapList[swapIndex][0][0]], fill='light blue')

            if index < len(aPositions):
                bars = [idOrder[swapList[swapIndex][0][1]], idOrder[swapList[swapIndex][0][0]]] 
                visCanvas.move(bars[0], bPositions[index][0] - visCanvas.coords(bars[0])[0], bPositions[index][1] - visCanvas.coords(bars[0])[3])
                visCanvas.move(bars[1], aPositions[index][0] - visCanvas.coords(bars[1])[0], aPositions[index][1] - visCanvas.coords(bars[1])[3])
                index += 1
                visCanvas.after(timePause, moveBars, swapList, swapIndex, index, bPositions, aPositions, idOrder, False, algidx)
            else:
                if not pauseComplete:
                    visCanvas.after(timePause*10, moveBars, swapList, swapIndex, index, bPositions, aPositions, idOrder, True, algidx)
                else:
                    visCanvas.itemconfig(idOrder[swapList[swapIndex][0][1]], fill='')
                    visCanvas.itemconfig(idOrder[swapList[swapIndex][0][0]], fill='')

                    if swapIndex < len(swapList):
                        updatelineText("Starting next swap")
                        swapIndex += 1
                        visCanvas.after(timePause, moveBars, swapList, swapIndex, 0, [], [], idOrder, False, algidx)     

    elif newData == False:
        visCanvas.after(200, moveBars, swapList, swapIndex, index, bPositions, aPositions, idOrder, False, algidx) 
    else:
        newData = False 

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
    global visCanvas, inProgress, newData

    inProgress = False
    newData = False
    updatelineText(None)
    setupKeyFrame(6, data)

    SPACING = 10
    padX = 100
    textIdData.clear()
    bucketIdData.clear()
    defaultRadixPositions.clear()
    
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
    
def radixVisualisation(data, swapList, swapIndex, stageIndex, stages, buckets, algidx, digit):
    global visCanvas, speed, inProgress, newData
    externalWidgets["keyDigits"][digit].config(foreground="red")
    if digit != len(str(max(data))) - 1:
        externalWidgets["keyDigits"][digit + 1].config(foreground="black")

    timePause = int(14/speed)
    if timePause == 0:
        timePause = 1

    if inProgress == True:
        if swapIndex == len(swapList):
            updatelineText("List is sorted, ending algorithm")
            externalWidgets["keyDigits"][0].config(foreground="black")
            for obj in textIdData:
                visCanvas.itemconfig(obj, fill="green")
            endAlgorithm(algidx)
        else:
            textX, textY = visCanvas.coords(textIdData[swapList[swapIndex][0][0] - 1])[0], visCanvas.coords(textIdData[swapList[swapIndex][0][0] - 1])[1]
            if stages == []:
                stages = animateMove(swapList[swapIndex], len(data), len(buckets[swapList[swapIndex][0][1]]), (swapIndex % len(data)) if swapIndex != 0 else len(data))
                visCanvas.itemconfig(textIdData[swapList[swapIndex][0][0] - 1], fill="blue")

            visCanvas.move(textIdData[swapList[swapIndex][0][0] - 1], stages[stageIndex][0] - textX, stages[stageIndex][1] - textY)

            if stageIndex + 1 == len(stages):
                if swapList[swapIndex][1] == "move in":
                    buckets[swapList[swapIndex][0][1]].append(textIdData[swapList[swapIndex][0][0] - 1])
                else:
                    del buckets[swapList[swapIndex][0][1]][0] 
                    if swapIndex + 1 != len(swapList):
                        if swapList[swapIndex + 1][1] == "move in":
                            digit -= 1

                visCanvas.itemconfig(textIdData[swapList[swapIndex][0][0] - 1], fill="black")
                visCanvas.after(timePause, radixVisualisation, data, swapList, swapIndex + 1, 0, [], buckets, algidx, digit)
            else:
                visCanvas.after(timePause, radixVisualisation, data, swapList, swapIndex, stageIndex + 1, stages, buckets, algidx, digit)

            if stageIndex == 0:
                if swapList[swapIndex][1] == "move in":
                    updatelineText("Moving element into bucket " + str(swapList[swapIndex][0][1]))
                    # if swapIndex - 1 != 0:
                    #     if swapList[swapIndex - 1][1] 
                else:
                    updatelineText("Moving element out of bucket " + str(swapList[swapIndex][0][1]))

    elif newData == False:
        visCanvas.after(200, radixVisualisation, data, swapList, swapIndex, stageIndex, stages, buckets, algidx)
    else:
        newData = False

def animateMove(event, dataSize, bucketSize, dataLength):
    textX, textY = visCanvas.coords(textIdData[event[0][0] - 1])[0], visCanvas.coords(textIdData[event[0][0] - 1])[1]
    bucketX, bucketY = visCanvas.coords(event[0][1] + bucketIdData[0])[0], visCanvas.coords(event[0][1] + bucketIdData[0])[1] - 20 - (30 * bucketSize)
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
    global inProgress, newData
    valid = True
    if inProgress == False:
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
                    defaultData[1] = algData.copy()
                else:
                    algData.append(random.randint(1, 50))
                    defaultData[0] = algData.copy()

            if algidx < 6:
                setupCanvas(algData)
            if algidx == 6:
                setupRadix(algData)

            if "startButton" in externalWidgets:
                externalWidgets["startButton"].config(command=lambda algIdx = algidx, data = algData: startAlgorithm(algIdx, data))
                newData = True
    else:
        messagebox.showwarning(message="Please pause the algorithm or wait for it to finish before entering new data")

def validateData(userInput, algidx):
    global inProgress, newData
    userInput = userInput.get()
    data = None
    if inProgress == False:
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
                    messagebox.showwarning(message="entered data could not be read. please enter data in the form 'x y z' using only integers")
        
        if data != None:
            algData = data  

            if algidx != 6:
                defaultData[0] = algData.copy()
            else:
                defaultData[1] = algData.copy()

            visCanvas.delete("all")

            if algidx == 6:
                setupRadix(algData)
            else:
                setupCanvas(algData)

            if "startButton" in externalWidgets:
                externalWidgets["startButton"].config(command=lambda algIdx = algidx, data = algData: startAlgorithm(algIdx, data))
                newData = True

    else:
        messagebox.showwarning(message="Please pause the algorithm or wait for it to finish before entering new data")

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
    global speed, inProgress
    pointerList = []

    if window.tk.call('after', 'info') == "":
        if algIdx <= 1:
            value = verifySearchValue()

        if algIdx == 0 and value != None:
            pointerList, value = Algorithms.linear(data, value)
        if algIdx == 1 and value != None:
            data = sorted(data)
            visCanvas.delete("all")
            setupCanvas(data)
            updatelineText("Sorting list (prerequisite for binary search)")
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

        inProgress = True

        if algIdx <= 1:
            searchVisualisation(data, pointerList, value, 0, algIdx)
        if algIdx >= 2 and algIdx <= 5:
            moveBars(swapList, 0, 0, [], [], rectIdData, False, algIdx)
        if algIdx == 6:
            radixVisualisation(data, swapList, 0, 0, [], [[] for _ in range(10)], algIdx, len(str(max(data))) - 1)

        externalWidgets["startButton"].config(text = "⏸", command=lambda: pauseAlgorithm())

initialiseHome()
window.mainloop()