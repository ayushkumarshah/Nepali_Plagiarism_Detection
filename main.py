from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog

from tkinter import Canvas
import interface
tk=Tk()
filename="filename"
def browse_button():
    global filename
    filename= filedialog.askdirectory()
    canvas.create_text(600, 70, text=filename, font="Times 12 bold")
    final_list=interface.get_final_list(filename)
    x = 0
    canvas.create_text(400, 110, text="Jacard, Cosine", font="Purisa 10")

    for i in final_list:
        canvas.create_text(280, 150+x, text=i+"%", font="Purisa 10")
        x=x+20
    return filename

canvas = Canvas(tk, width=1200, height=720)

canvas.pack()
button=Button(canvas,text="Choose the folder",width=30,command=browse_button)


canvas.create_window(200,50,window=button, height=25, width=100)

print(filename)
mainloop()
