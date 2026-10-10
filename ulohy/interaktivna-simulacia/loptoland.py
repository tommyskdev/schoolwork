import tkinter as tk

root = tk.Tk()
root.title("LoptoLand")
root.geometry("1000x700")

canvas = tk.Canvas(root, bg="#11151c", highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1.0, relheight=0.74)

def draw_arena(event):
    canvas.delete("all")
    w, h = event.width, event.height
    canvas.create_rectangle(w * 0.03, h * 0.05, w * 0.97, h * 0.95, outline="#3d4654", width=3)

canvas.bind("<Configure>", draw_arena)

panel = tk.Frame(root, bg="#262c37")
panel.place(x=0, rely=1.0, anchor="sw", relwidth=1.0, relheight=0.26)

tk.Button(panel, text="PAUSE").place(relx=0.02, rely=0.16, anchor="w")
tk.Button(panel, text="RESET").place(relx=0.11, rely=0.16, anchor="w")
tk.Button(panel, text="SAVE").place(relx=0.19, rely=0.16, anchor="w")
tk.Button(panel, text="EXIT").place(relx=0.27, rely=0.16, anchor="w")
tk.Button(panel, text="World Physics").place(relx=0.68, rely=0.16, anchor="w")
tk.Button(panel, text="Surfaces & Environment").place(relx=0.99, rely=0.16, anchor="e")

for i, text in enumerate(["SPEED (V)", "STRIKE FORCE (F)", "SPIN", "KINETIC ENERGY", "VECTOR (VX / VY)"]):
    tk.Label(panel, text=text, bg="#262c37", fg="#8b98a9").place(relx=0.02 + i * 0.19, rely=0.47, anchor="w")

tk.Label(panel, text="SPAWN OBJECTS:", bg="#262c37", fg="#e6edf3").place(relx=0.02, rely=0.80, anchor="w")
for i, text in enumerate(["Balls", "Cube", "Ramp", "Bumper", "Wall Barrier"]):
    tk.Button(panel, text=text).place(relx=0.16 + i * 0.16, rely=0.79, anchor="w")

root.mainloop()
