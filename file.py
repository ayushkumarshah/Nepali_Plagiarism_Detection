from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog

from tkinter import Canvas

tk=Tk()


filename='filename'
def browse_button():
    global filename
    filename= filedialog.askdirectory()
    canvas.create_text(10, 100, text=filename, font="Times 15 bold")

canvas = Canvas(tk, width=600, height=600)
# print(filename+"Hello")
button=Button(canvas,text="Choose the folder",width=30,command=browse_button)
# print(filename+"Hello")

canvas.create_window(200,200,window=button, height=25, width=100)
# canvas.create_text(100, 100, text=filename, font="Times 15 bold")

canvas.pack()

mainloop()
