import tkinter as tk

root = tk.Tk()

c = tk.Canvas(root)
c.pack(expand=1, fill=tk.BOTH)

words = '''I am writing a program that involves displaying some text in a create_text() box on a Tkinter canvas, within a loop. Each word is displayed, then replaced by the next. Sort of like flash cards. I need to color one letter of each word, close to the middle of the word, so that when the user is reading the words their eyes focus on the middle of the word. So if len(i)=1, color i[0], if len(i)>= 2 and <= 5, color i[1], and so on. It needs to be done using the Canvas, and using canvas.create_text(text = i[focus_index],fill = 'red') The result should print like this exaMple (but obviously "m" would be colored red, not be uppercase)'''
words = words.split()

def new_word(i):
    if i == len(words):
        i = 0

    word = words[i]
    middle = (len(word)+1)//2
    c.itemconfigure(t1, text=word[:middle-1]+' ')
    c.itemconfigure(t2, text=word[middle-1:middle])
    c.itemconfigure(t3, text=word[middle:])

    root.after(100, lambda: new_word(i+1))


t1 = c.create_text(200,100,text='', anchor='e', font=("Courier", 25))
t2 = c.create_text(200,100,text='', anchor='e', font=("Courier", 25), fill='red')
t3 = c.create_text(200,100,text='', anchor='w', font=("Courier", 25))
new_word(0)

root.geometry('400x200+200+200')
root.mainloop()