import tkinter as tk
 
root = tk.Tk()
 
def show(event):
    value = slider.get()
    label.config(text=f'Speed: {value}')
 
label = tk.Label(root, text='Speed: 0', anchor='w')
label.pack(fill='x')
def h():
    slider = tk.Scale(root, from_=0, to=100, orient='horizontal', command=show)
    slider.pack()
 
root.mainloop()