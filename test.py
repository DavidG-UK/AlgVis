# code for Bubble Sort Visualizer using Python and Tkinter
from tkinter import *
from tkinter import ttk
import random
import time

# initialising root class for Tkinter
root = Tk()
root.title("Bubble Sort Visualizer")

# maximum window size
root.maxsize(900, 600)
root.config(bg="Black")
select_alg = StringVar()
data = []


def bubble(data, drawData, timer):
	n = len(data)
	
	for i in range(n):
		for j in range(0, n-i-1):
			
			if data[j] > data[j+1]:
				data[j], data[j+1] = data[j+1], data[j]
				
				# if swapped then color becomes Green else stays Red
				drawData(data, ['Green' if x == j +
								1 else 'Red' for x in range(len(data))])
				time.sleep(timer)
		
	# sorted elements generated with Green color
	drawData(data, ['Green' for x in range(len(data))])

def generate():
	global data

	# minval : minimum value of the range
	minval = int(minEntry.get())

	# maxval : maximum value of the range
	maxval = int(maxEntry.get())

	# sizeval : number of data values/bars to be generated
	sizeval = int(sizeEntry.get())

	# creating a blank data list which will be further
	# filled with random data values
	# within the entered range
	data = []
	for _ in range(sizeval):
		data.append(random.randrange(minval, maxval+1))

	drawData(data, ['Red' for x in range(len(data))])

# function to create the data bars by creating a canvas in Tkinter
def drawData(data, colorlist):
	canvas.delete("all")
	can_height = 380
	can_width = 550
	x_width = can_width/(len(data) + 1)
	offset = 30
	spacing = 10

	# normalizing data for rescaling real-valued numeric data within the
	# given range
	normalized_data = [i / max(data) for i in data]

	for i, height in enumerate(normalized_data):
		# top left corner
		x0 = i*x_width + offset + spacing
		y0 = can_height - height*340

		# bottom right corner
		x1 = ((i+1)*x_width) + offset
		y1 = can_height

		# data bars are generated as Red colored vertical rectangles
		canvas.create_rectangle(x0, y0, x1, y1, fill=colorlist[i])
		canvas.create_text(x0+2, y0, anchor=SE, text=str(data[i]))
	root.update_idletasks()

# function to initiate the sorting process by 
# calling the extension code
def start_algorithm():
	global data
	bubble(data, drawData, speedbar.get())


# creating main user interface frame and
# basic layout by creating a frame
Mainframe = Frame(root, width=600, height=200, bg="Grey")
Mainframe.grid(row=0, column=0, padx=10, pady=5)

canvas = Canvas(root, width=600, height=380, bg="Grey")
canvas.grid(row=1, column=0, padx=10, pady=5)

# creating user interface area in grid manner
# first row components
Label(Mainframe, text="ALGORITHM", bg='Grey').grid(
	row=0, column=0, padx=5, pady=5, sticky=W)

# algorithm menu for showing the name of the sorting algorithm
algmenu = ttk.Combobox(
	Mainframe, textvariable=select_alg, values=["Bubble Sort"])
algmenu.grid(row=0, column=1, padx=5, pady=5)
algmenu.current(0)

# creating Start Button to start the sorting visualization process
Button(Mainframe, text="START", bg="Blue", command=start_algorithm).grid(
	row=1, column=3, padx=5, pady=5)

# creating Speed Bar using scale in Tkinter
speedbar = Scale(Mainframe, from_=0.10, to=2.0, length=100, digits=2,
				resolution=0.2, orient=HORIZONTAL, label="Select Speed")
speedbar.grid(row=0, column=2, padx=5, pady=5)


# second row components
# sizeEntry : scale to select the size/number of data bars
sizeEntry = Scale(Mainframe, from_=3, to=60, resolution=1,
				orient=HORIZONTAL, label="Size")
sizeEntry.grid(row=1, column=0, padx=5, pady=5)

# minEntry : scale to select the minimum value of data bars
minEntry = Scale(Mainframe, from_=0, to=10, resolution=1,
				orient=HORIZONTAL, label="Minimum Value")
minEntry.grid(row=1, column=1, padx=5, pady=5)

# maxEntry : scale to select the maximum value of data bars
maxEntry = Scale(Mainframe, from_=10, to=100, resolution=1,
				orient=HORIZONTAL, label="Maximum Value")
maxEntry.grid(row=1, column=2, padx=5, pady=5)

# creating generate button
Button(Mainframe, text="Generate", bg="Red", command=generate).grid(
	row=0, column=3, padx=5, pady=5)

# to stop automatic window termination
root.mainloop()
