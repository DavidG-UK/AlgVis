import random
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry("1980x1200")
window.configure(background="black")
currentScreen = ""
algData = []
tutButtons = [None, None, None]
tutStage = 0

options = [["Live Code Display", True, None], ["O(n)", True, None], ["O(n) description", True, None]]
algorithms = [["Linear Search", "placeholder text", "O(n)", "placeholder text"], 
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
    global currentScreen, tutStage
    clearScreen(True)
    currentScreen = "home"
    
    window.columnconfigure((0, 2), weight=1, uniform="a")
    window.columnconfigure(1, weight=2, uniform="a")

    for i in range(10):
        if i == 3 or i == 5 or i == 7:
            window.rowconfigure(i, weight=3, uniform="a")
        else:
            window.rowconfigure(i, weight=2, uniform="a")

    algorithmButton = tk.Button(window, text="Algorithms", background="light blue", font=("Calibri", 14, "bold"), command=initialiseAlgSelect)
    optionsButton = tk.Button(window, text="Options", background="light blue", font=("Calibri", 14, "bold"), command=initialiseOptions)
    tutorialButton = tk.Button(window, text="Tutorial", background="light blue", font=("Calibri", 14, "bold"), command=lambda tutStage = tutStage: initialiseTutorial(tutStage))
    titleLabel = ttk.Label(window, text="ALGVIS", background="black", anchor="center", font=("Calibri", 30, "bold"), foreground="light blue")
    welcomeLabel = ttk.Label(window, text="Welcome to Algvis! here you can visualise many common algorithms", background="black", anchor="center", font=("Calibri", 15, "bold"), foreground="light blue")

    algorithmButton.grid(row=3, column=1, sticky="nesw")
    optionsButton.grid(row=5, column=1, sticky="nesw")
    tutorialButton.grid(row=7, column=1, sticky="nesw")
    titleLabel.grid(row=0, column=1, sticky="nesw")
    welcomeLabel.grid(row=1, column=1, sticky="nesw")

def initialiseOptions():
    global currentScreen

    clearScreen(True)
    currentScreen = "options"

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
        optionLabel = ttk.Label(window, text=options[i][0], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
        optionLabel.grid(row=(i*2)+1, column=1, sticky="nesw")

        optionButton = tk.Button(window, background="green" if options[i][1] == True else "red", font=("Calibri", 14, "bold"), command=lambda idx=i: updateButton(idx))
        options[i][2] = optionButton
        optionButton.grid(row=(i*2)+1, column=2, sticky="nesw")

def initialiseTutorial(stage):
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

    displayBack("home", "nw")
    expLabel = ttk.Label(window, text=labelText[stage], background="light blue", anchor="center", font=("Calibri", 18, "bold"), foreground="black")
    expLabel.grid(row=2, column=1, sticky="nesw", columnspan=2)
    forward = tk.Button(window, text="⏵", background="white", font=("Calibri", 14, "bold"), command=lambda stage = stage: initialiseTutorial(stage + 1) if stage < len(labelText) - 1 else initialiseHome())
    backward = tk.Button(window, text="⏴", background="white", font=("Calibri", 14, "bold"), command=lambda stage = stage: initialiseTutorial(stage - 1) if stage > 0 else None)
    backward.grid(row=1, column=1, sticky="nesw")
    forward.grid(row=1, column=2, sticky="nesw")
    tutFrame = ttk.Frame(window)

    if stage == 0:   
        tutFrame.columnconfigure((0, 2), weight=1, uniform="g")
        tutFrame.columnconfigure(1, weight=3, uniform="g")
        tutFrame.rowconfigure((0, 1, 2), weight=1, uniform="g")
        algorithmButton = tk.Button(tutFrame, text="Algorithms", background="light blue", font=("Calibri", 14, "bold"))
        algorithmButton.grid(row=1, column=1, sticky="nesw")

    if stage == 1:
        tutFrame.columnconfigure(0, weight=2, uniform="h")
        tutFrame.columnconfigure(1, weight=3, uniform="h")
        tutFrame.columnconfigure(2, weight=1, uniform="h")
        tutFrame.columnconfigure(3, weight=2, uniform="h")

        tutFrame.rowconfigure(0, weight=2, uniform="h")
        for i in range(1, len(options) * 2, 2):
            tutFrame.rowconfigure(i, weight=2, uniform="h")
            tutFrame.rowconfigure(i + 1, weight=1, uniform="h")

        for i in range(len(options)):
            opLabel = ttk.Label(tutFrame, text=options[i][0], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
            opLabel.grid(row=(i*2)+1, column=1, sticky="nesw")

            optionButton = tk.Button(tutFrame, background="green", font=("Calibri", 14, "bold"), command=lambda idx=i: updateTutButton(idx))
            tutButtons[i] = optionButton
            optionButton.grid(row=(i*2)+1, column=2, sticky="nesw")
    
    if stage == 2:
        tutFrame.rowconfigure((0, 2), weight=3, uniform="i")
        tutFrame.rowconfigure(1, weight=2, uniform="i")
        tutFrame.columnconfigure((0, 2), weight=1, uniform="i")
        tutFrame.columnconfigure(1, weight=10, uniform="i")
        taskFrame = createTaskbar(False, None, tutFrame)
        taskFrame.grid(row=1, column=1, sticky="nesw")
    
    if stage == 3:
        tutFrame.rowconfigure(0, weight=1, uniform="j")
        tutFrame.rowconfigure(1, weight=2, uniform="j")
        tutFrame.rowconfigure(2, weight=4, uniform="j")
        tutFrame.columnconfigure((0, 2), weight=1, uniform="j")
        tutFrame.columnconfigure(1, weight=10, uniform="j")
        taskFrame = createTaskbar(False, None, tutFrame)
        planeLabel = ttk.Label(tutFrame, text="plane", background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
        taskFrame.grid(row=1, column=1, sticky="nesw")
        planeLabel.grid(row=2, column=1, sticky="nesw")
    if stage == 4:
        pass
        # do when visualisation is complete
    if stage == 5:
        tutFrame.rowconfigure(0, weight=1, uniform="l")
        tutFrame.columnconfigure(0, weight=1, uniform="l")
        smileLabel = ttk.Label(tutFrame, text=":D", background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
        smileLabel.grid(row=0, column=0, sticky="nesw")
    tutFrame.grid(row=3, column=1, sticky="nesw", columnspan=2)

def initialiseAlgSelect():
    global currentScreen

    clearScreen(True)
    currentScreen = "algselect"

    algButtons = []

    window.columnconfigure((0, 1), weight=1, uniform="c")

    window.rowconfigure(0, weight=2, uniform="c")
    for i in range(1, len(algorithms) + 1):
        window.rowconfigure(i, weight=3, uniform="c")
    
    displayBack("home", "nw")

    for i in range(len(algorithms)):
        algButtons.append(tk.Button(window, text=algorithms[i][0], background="black", foreground="white", font=("Calibri", 14, "bold"), command=lambda idx=i: displayAlgInfo(idx)))
        algButtons[i].grid(row=i+1, column=0, sticky="nesw")

def initialiseVisualisation(algidx):
    global currentScreen

    clearScreen(True)
    currentScreen = "algselect"

    window.columnconfigure(0, weight=1, uniform="d")
    window.columnconfigure(1, weight=1, uniform="d")
    window.columnconfigure(2, weight=4, uniform="d")
    window.columnconfigure(3, weight=3, uniform="d")

    window.rowconfigure(0, weight=1, uniform="d")
    window.rowconfigure(1, weight=6, uniform="d")
    window.rowconfigure(2, weight=1, uniform="d")
    window.rowconfigure(3, weight=2, uniform="d")

    planeLabel = ttk.Label(window, text="plane", background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")

    taskbar = createTaskbar(True, algidx, window)
    displayBack("algSelect", "nesw")
    gridFrame = ttk.Frame(window)
    gridFrame.rowconfigure(0, weight=1, uniform="k")
    gridFrame.columnconfigure(0, weight=1, uniform="k")

    #label = ttk.Label(gridFrame, text="e", background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
    #label.grid(row=0, column=0, sticky="nesw")
    gridFrame.grid(row=2, column=2, sticky="nesw", rowspan=2)
    planeLabel.grid(row=1, column=0, sticky="nesw", columnspan=4)
    taskbar.grid(row=0, column=1, sticky="nesw", columnspan=3)
  

    if options[0][1] == True:
        codeFrame = tk.Frame(window)
        lineLabels = []
        codeFrame.columnconfigure(0, weight=1, uniform="f")
        codeFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform="f")
        currentLine = "placeholder text"
        for i in range(8):
            lineLabels.append(ttk.Label(codeFrame, text=currentLine, background="white", anchor="center", font=("Calibri", 14), foreground="black"))
            lineLabels[i].grid(row=i, column=0, sticky="nesw")

        codeFrame.grid(row=2, column=3, rowspan=2, sticky="nesw")

    if options[1][1] == True:
        onLabel = ttk.Label(window, text=algorithms[algidx][2], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
        onLabel.grid(row=2, column=0, rowspan=2 if options[2][1] == False else 1, columnspan=2, sticky="nesw")

    if options[2][1] == True:
        onDescLabel = ttk.Label(window, text=algorithms[algidx][3], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
        onDescLabel.grid(row=3, column=0, columnspan=2, sticky="nesw")

    print(algData)

def displayBack(backScreen, xyAlignment):
    if backScreen == "home":
        backButton = tk.Button(window, text="back", background="white", font=("Calibri", 14, "bold"), command=initialiseHome)
    elif backScreen == "algSelect":
        backButton = tk.Button(window, text="back", background="white", font=("Calibri", 14, "bold"), command=initialiseAlgSelect)
    backButton.grid(row=0, column=0, sticky=xyAlignment)

def createTaskbar(active, algidx, master):
    speed = 1

    taskFrame = tk.Frame(master)
    taskFrame.rowconfigure(0, weight=1, uniform="g")
    taskFrame.columnconfigure(0, weight=1, uniform="g")
    taskFrame.columnconfigure(1, weight=4, uniform="g")
    taskFrame.columnconfigure(2, weight=3, uniform="g")

    startButton = tk.Button(taskFrame, text="⏵", background="white", font=("Calibri", 14, "bold"), command=lambda algIdx = algidx: startAlgorithm(algIdx) if active == True else None)
    speedScale = tk.Scale(taskFrame, from_=0.1, to=10, orient="horizontal", variable=speed, label="Execution speed", resolution=0.1)
    speedScale.set(speed)

    inputFrame = tk.Frame(taskFrame)

    inputFrame.columnconfigure(1, weight=3, uniform="e")
    inputFrame.columnconfigure((0, 2), weight=1, uniform="e")
    inputFrame.rowconfigure(0, weight=1, uniform="e")

    inputVar = tk.StringVar()
    entryBox = ttk.Entry(inputFrame, textvariable=inputVar)
    randomButton = tk.Button(inputFrame, text="Random", background="white", font=("Calibri", 14, "bold"), command=generateRandomData if active == True else None)
    inputButton = tk.Button(inputFrame, text="Enter", background="white", font=("Calibri", 14, "bold"), command=lambda input = inputVar: submitAlgData(input) if active == True else None)

    inputButton.grid(row=0, column=0, sticky="nesw")
    entryBox.grid(row=0, column=1, sticky="nesw")
    randomButton.grid(row=0, column=2, sticky="nesw")

    startButton.grid(row=0, column=0, sticky="nesw")
    speedScale.grid(row=0, column=1, sticky="nesw")
    inputFrame.grid(row=0, column=2, sticky="nesw")
    return taskFrame

def submitAlgData(userInput):
    global algData
    userInput = userInput.get()
    algData = list(map(int, userInput.split(" ")))

def generateRandomData():
    global algData
    algData = []
    for i in range(5):
        algData.append(random.randint(1, 25))

def displayAlgInfo(algidx):
    titleLabel = ttk.Label(window, text=algorithms[algidx][0], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
    descLabel = ttk.Label(window, text=algorithms[algidx][1], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
    visualiseButton = tk.Button(window, text="visualise!", background="green", font=("Calibri", 20, "bold"), command=lambda idx=algidx: initialiseVisualisation(idx))

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

def startAlgorithm(algIdx):
    pass

initialiseHome()
window.mainloop()