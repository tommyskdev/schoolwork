import tkinter as tk

root = tk.Tk()
root.title("LoptoLand")
root.geometry("1000x700")

canvas = tk.Canvas(root, bg="#11151c", highlightthickness=0)
canvas.pack(fill="both", expand=True)

ARENA = (0.03, 0.05, 0.97, 0.72)
BH = 0.028

BUTTONS = [
    ("PAUSE", 0.02, 0.80, 0.07, None),
    ("RESET", 0.10, 0.80, 0.07, None),
    ("SAVE", 0.18, 0.80, 0.07, None),
    ("EXIT", 0.26, 0.80, 0.07, None),
    ("World Physics", 0.52, 0.80, 0.14, None),
    ("Surfaces & Environment", 0.71, 0.80, 0.21, None),
    ("Balls", 0.16, 0.945, 0.08, "Balls"),
    ("Cube", 0.32, 0.945, 0.08, "Cube"),
    ("Ramp", 0.48, 0.945, 0.08, "Ramp"),
    ("Bumper", 0.64, 0.945, 0.08, "Bumper"),
    ("Wall Barrier", 0.80, 0.945, 0.13, "Wall Barrier"),
]
INFO = ["SPEED (V)", "STRIKE FORCE (F)", "SPIN", "KINETIC ENERGY", "VECTOR (VX / VY)"]
objects = []
hover = None

def rect(button):
    _, x, y, w, _ = button
    return x, y - BH, x + w, y + BH

def hit(x, y):
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    for b in BUTTONS:
        x1, y1, x2, y2 = rect(b)
        if x1 * cw <= x <= x2 * cw and y1 * ch <= y <= y2 * ch:
            return b
    return None

def draw_object(kind, x, y):
    if kind == "Balls":
        canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="#e0a33a", outline="")
    elif kind == "Cube":
        canvas.create_rectangle(x - 18, y - 18, x + 18, y + 18, fill="#5aa9e6", outline="")
    elif kind == "Ramp":
        canvas.create_polygon(x - 28, y + 18, x + 28, y + 18, x + 28, y - 18, fill="#8b98a9", outline="")
    elif kind == "Bumper":
        canvas.create_oval(x - 22, y - 22, x + 22, y + 22, outline="#e04f5f", width=5)
    elif kind == "Wall Barrier":
        canvas.create_rectangle(x - 40, y - 7, x + 40, y + 7, fill="#5c6b7a", outline="")

def redraw(event=None):
    canvas.delete("all")
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    canvas.create_rectangle(ARENA[0] * cw, ARENA[1] * ch, ARENA[2] * cw, ARENA[3] * ch, outline="#3d4654", width=3)
    canvas.create_rectangle(0, 0.74 * ch, cw, ch, fill="#262c37", outline="")
    for kind, x, y in objects:
        draw_object(kind, x * cw, y * ch)
    for i, text in enumerate(INFO):
        canvas.create_text((0.02 + i * 0.19) * cw, 0.87 * ch, text=text, fill="#8b98a9", anchor="w")
    canvas.create_text(0.02 * cw, 0.945 * ch, text="SPAWN OBJECTS:", fill="#e6edf3", anchor="w")
    for b in BUTTONS:
        x1, y1, x2, y2 = rect(b)
        canvas.create_rectangle(x1 * cw, y1 * ch, x2 * cw, y2 * ch, fill="#3d4654" if b is hover else "#2b3240", outline="#4a5666")
        canvas.create_text((x1 + x2) / 2 * cw, (y1 + y2) / 2 * ch, text=b[0], fill="#e6edf3")

def on_motion(event):
    global hover
    found = hit(event.x, event.y)
    if found is not hover:
        hover = found
        canvas.config(cursor="hand2" if found else "")
        redraw()

def on_click(event):
    b = hit(event.x, event.y)
    if b and b[4]:
        i = len(objects)
        cx = (ARENA[0] + ARENA[2]) / 2
        cy = (ARENA[1] + ARENA[3]) / 2
        objects.append((b[4], cx + (i % 5) * 0.04 - 0.08, cy + (i // 5) * 0.05))
        redraw()

canvas.bind("<Configure>", redraw)
canvas.bind("<Motion>", on_motion)
canvas.bind("<Button-1>", on_click)

root.mainloop()
