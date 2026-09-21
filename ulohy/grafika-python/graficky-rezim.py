import tkinter

canvas = tkinter.Canvas(width=450, height=400, bg="white")
canvas.pack()

# 1. vonkajsi obdlznik
canvas.create_rectangle(50, 50, 400, 350, outline="black", width=2)
# 2. lave oko
canvas.create_rectangle(110, 110, 170, 170, outline="black", width=2)
# 3. prave oko
canvas.create_rectangle(280, 110, 340, 170, outline="black", width=2)
# 4. lava cast 
canvas.create_rectangle(110, 200, 150, 250, outline="black", width=2)
# 5. prava cast
canvas.create_rectangle(300, 200, 340, 250, outline="black", width=2)
# 6. spodna cast
canvas.create_rectangle(110, 250, 340, 290, outline="black", width=2)

canvas.mainloop()
