import random
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry("800x600")
window.configure(background="black")
currentScreen = ""
algData = []

options = [["tutorial", True, None],["code execution", False, None], ["O(n)", False, None], ["O(n) description", False, None]]
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

def clearScreen():
    window.configure(background="black")
    for widget in window.winfo_children():
        widget.destroy()
    
    for i in range(window.grid_size()[0]):
        window.columnconfigure(i, weight=0)
    for i in range(window.grid_size()[1]):
        window.rowconfigure(i, weight=0)

def initialiseHome():
    global currentScreen
    clearScreen()
    currentScreen = "home"
    
    window.columnconfigure(0, weight=2, uniform="a")
    window.columnconfigure(1, weight=4, uniform="a")
    window.columnconfigure(2, weight=2, uniform="a")

    for i in range(10):
        if i == 3 or i == 5 or i == 7:
            window.rowconfigure(i, weight=3, uniform="a")
        else:
            window.rowconfigure(i, weight=2, uniform="a")

    algorithmButton = tk.Button(window, text="Algorithms", background="light blue", font=("Calibri", 14, "bold"), command=lambda screen="algSelect": changeScreen(screen))
    optionsButton = tk.Button(window, text="Options", background="light blue", font=("Calibri", 14, "bold"), command=lambda screen="options": changeScreen(screen))
    tutorialButton = tk.Button(window, text="Tutorial", background="light blue", font=("Calibri", 14, "bold"), command=lambda screen="tutorial": changeScreen(screen))
    titleLabel = ttk.Label(window, text="ALGVIS", background="black", anchor="center", font=("Calibri", 30, "bold"), foreground="light blue")
    welcomeLabel = ttk.Label(window, text="Welcome to Algvis! here you can visualise many common algorithms", background="black", anchor="center", font=("Calibri", 15, "bold"), foreground="light blue")

    algorithmButton.grid(row=3, column=1, sticky="nesw")
    optionsButton.grid(row=5, column=1, sticky="nesw")
    tutorialButton.grid(row=7, column=1, sticky="nesw")
    titleLabel.grid(row=0, column=1, sticky="nesw")
    welcomeLabel.grid(row=1, column=1, sticky="nesw")

def initialiseOptions():
    global currentScreen

    clearScreen()
    currentScreen = "options"

    window.columnconfigure(0, weight=2, uniform="b")
    window.columnconfigure(1, weight=3, uniform="b")
    window.columnconfigure(2, weight=1, uniform="b")
    window.columnconfigure(3, weight=2, uniform="b")

    window.rowconfigure(0, weight=4, uniform="b")
    for i in range(1, len(options) * 2, 2):
        window.rowconfigure(i, weight=3, uniform="b")
        window.rowconfigure(i + 1, weight=1, uniform="b")
    
    backButton = tk.Button(window, text="back", background="white", font=("Calibri", 14, "bold"), command=lambda screen="home": changeScreen(screen))
    backButton.grid(row=0, column=0, sticky="nw")

    for i in range(len(options)):
        optionLabel = ttk.Label(window, text=options[i][0], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
        optionLabel.grid(row=(i*2)+1, column=1, sticky="nesw")

        optionButton = tk.Button(window, background="green" if options[i][1] == True else "red", font=("Calibri", 14, "bold"), command=lambda idx=i: updateButton(idx))
        options[i][2] = optionButton
        optionButton.grid(row=(i*2)+1, column=2, sticky="nesw")

def initialiseAlgSelect():
    global currentScreen

    clearScreen() # removes all widgets and formatting
    currentScreen = "algselect"

    algButtons = []

    window.columnconfigure((0, 1), weight=1, uniform="c") # Sets up formatting with enough rows for all algorithms

    window.rowconfigure(0, weight=2, uniform="c")
    for i in range(1, len(algorithms) + 1):
        window.rowconfigure(i, weight=3, uniform="c")
    
    displayBack("home", "nw")

    for i in range(len(algorithms)): # creates a button for each algorithm that can be visualised
        algButtons.append(tk.Button(window, text=algorithms[i][0], background="black", foreground="white", font=("Calibri", 14, "bold"), command=lambda idx=i: displayAlgInfo(idx)))
        algButtons[i].grid(row=i+1, column=0, sticky="nesw")

def displayAlgInfo(algidx):
    titleLabel = ttk.Label(window, text=algorithms[algidx][0], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black") # creates labels to describe the algorithm
    descLabel = ttk.Label(window, text=algorithms[algidx][1], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
    visualiseButton = tk.Button(window, text="visualise!", background="green", font=("Calibri", 20, "bold"), command=lambda idx=algidx: initialiseVisualisation(idx)) # creates a button used to move to the visualisation screen

    titleLabel.grid(row=1, column=1, sticky="nesw") # displays widgets
    descLabel.grid(row=2, column=1, sticky="nesw", rowspan=window.grid_size()[1] - 4)
    visualiseButton.grid(row=window.grid_size()[1] - 2, column=1, sticky="nesw", rowspan=2)



def displayBack(a, b):
    pass

def initialiseVisualisation(algidx):
    global currentScreen

    clearScreen()
    window.configure(background="light grey")
    currentScreen = "algselect"

    speed = 1

    window.columnconfigure((0, 1), weight=1, uniform="d")
    window.columnconfigure(2, weight=4, uniform="d")
    window.columnconfigure(3, weight=3, uniform="d")

    window.rowconfigure(0, weight=1, uniform="d")
    window.rowconfigure(1, weight=6, uniform="d")
    window.rowconfigure(2, weight=1, uniform="d")
    window.rowconfigure(3, weight=2, uniform="d")

    planeLabel = ttk.Label(window, text="plane", background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
    backButton = tk.Button(window, text="back", background="white", font=("Calibri", 14, "bold"), command=lambda screen="algSelect": changeScreen(screen))
    startButton = tk.Button(window, text="⏵", background="white", font=("Calibri", 14, "bold"), command=lambda algIdx = algidx: startAlgorithm(algIdx))
    speedScale = tk.Scale(window, from_=0.1, to=10, orient="horizontal", variable=speed, label="Execution speed", resolution=0.1)
    speedScale.set(speed)

    inputFrame = tk.Frame(window)

    inputFrame.columnconfigure(1, weight=3, uniform="e")
    inputFrame.columnconfigure((0, 2), weight=1, uniform="e")
    inputFrame.rowconfigure(0, weight=1, uniform="e")

    inputVar = tk.StringVar()
    entryBox = ttk.Entry(inputFrame, textvariable=inputVar)
    randomButton = tk.Button(inputFrame, text="Random", background="white", font=("Calibri", 14, "bold"), command=generateRandomData)
    inputButton = tk.Button(inputFrame, text="Enter", background="white", font=("Calibri", 14, "bold"), command=lambda input = inputVar: submitAlgData(input))

    inputButton.grid(row=0, column=0, sticky="nesw")
    entryBox.grid(row=0, column=1, sticky="nesw")
    randomButton.grid(row=0, column=2, sticky="nesw")

    planeLabel.grid(row=1, column=0, sticky="nesw", columnspan=4)
    backButton.grid(row=0, column=0, sticky="nesw")
    startButton.grid(row=0, column=1, sticky="nesw")
    speedScale.grid(row=0, column=2, sticky="nesw")
    inputFrame.grid(row=0, column=3, sticky="nesw")

    if options[1][1] == True:
        codeFrame = tk.Frame(window)
        lineLabels = []
        codeFrame.columnconfigure(0, weight=1, uniform="f")
        codeFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform="f")
        currentLine = "placeholder text"
        for i in range(8):
            lineLabels.append(ttk.Label(codeFrame, text=currentLine, background="white", anchor="center", font=("Calibri", 14), foreground="black"))
            lineLabels[i].grid(row=i, column=0, sticky="nesw")

        codeFrame.grid(row=2, column=3, rowspan=2, sticky="nesw")

    if options[2][1] == True:
        onLabel = ttk.Label(window, text=algorithms[algidx][2], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
        onLabel.grid(row=2, column=0, rowspan=2 if options[3][1] == False else 1, columnspan=2, sticky="nesw")

    if options[3][1] == True:
        onDescLabel = ttk.Label(window, text=algorithms[algidx][3], background="white", anchor="center", font=("Calibri", 20, "bold"), foreground="black")
        onDescLabel.grid(row=3, column=0, columnspan=2, sticky="nesw")

    print(algData)

def displayTutorial():
    blockLabel = ttk.Label(window, background="grey", anchor="center")

def submitAlgData(userInput):
    global algData
    userInput = userInput.get()
    algData = list(map(int, userInput.split(" ")))

def generateRandomData():
    global algData
    algData = []
    for i in range(5):
        algData.append(random.randint(1, 25))

def updateButton(buttonIndex):
    if options[buttonIndex][1] == False:
        options[buttonIndex][1] = True
        options[buttonIndex][2].config(background="green")
    else:
        options[buttonIndex][1] = False
        options[buttonIndex][2].config(background="red")

def startAlgorithm(algIdx):
    pass

def changeScreen(screen):
    if screen == "home":
        initialiseHome()
    if screen == "options":
        initialiseOptions()
    if screen == "algSelect":
        initialiseAlgSelect()

initialiseHome()
window.mainloop()