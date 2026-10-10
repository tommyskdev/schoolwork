import tkinter as tk
from random import *

root = tk.Tk()
root.title("daco")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack(padx=10, pady=10, expand=True, fill="both")

def create_circle(x, y, r, canvas, color):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, outline = color)

create_circle(400, 300, 20, canvas, "black")
last_value=20+randint(15, 25)
last_color="red"

while last_value < 300:
    create_circle(400, 300, last_value, canvas, last_color)
    last_value += randint(15, 25)
    if last_color == "black":
        last_color = "red"
    else:
        last_color = "black"

root.mainloop()
