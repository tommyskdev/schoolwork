import json
import os
import tkinter as tk
from datetime import datetime

SAVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loptoland_save.json")
DEF = {
    "gravity": 9.81, "gravity_angle": 0.0, "air_density": 1.225,
    "wind_speed": 0.0, "wind_angle": 0.0, "restitution": 0.75,
    "ground_friction": 0.35, "wall_friction": 0.20,
    "ball_mass": 0.43, "ball_radius": 0.30, "ball_spin": 0.0,
}
GROUPS = {
    "world_physics": ("gravity", "gravity_angle", "air_density", "wind_speed", "wind_angle"),
    "surfaces_environment": ("restitution", "ground_friction", "wall_friction"),
    "ball_defaults": ("ball_mass", "ball_radius", "ball_spin"),
}
WORLD = [
    ("gravity", "Gravity", "m/s²", 0, 100),
    ("gravity_angle", "Gravity direction", "°", 0, 360),
    ("air_density", "Air density (air drag) ρ", "kg/m³", 0, 20),
    ("wind_speed", "Wind speed", "m/s", 0, 100),
    ("wind_angle", "Wind direction", "°", 0, 360),
]
SURF = [
    ("restitution", "Bounce / restitution e", "", 0, 1),
    ("ground_friction", "Ground friction μ", "", 0, 1),
    ("wall_friction", "Wall friction μ", "", 0, 1),
]
INFO = ["SPEED (V)", "STRIKE FORCE (F)", "SPIN", "KINETIC ENERGY", "VECTOR (VX / VY)"]
S = dict(DEF)
objects, paused, status_job, popups = [], False, None, {}

BG, PANEL, BTN, HVR = "#11151c", "#262c37", "#2b3240", "#3d4654"
FG, MUTED, EDGE, ACC = "#e6edf3", "#8b98a9", "#4a5666", "#5aa9e6"
GOLD, RED, GREEN = "#f2c94c", "#e04f5f", "#65c18c"
ARENA, BH = (0.03, 0.05, 0.97, 0.72), 0.028
POPUP_Y = (ARENA[1] + ARENA[3]) / 2
FONT = "DejaVu Sans"
F8, F9, FB, F14 = (FONT, 8), (FONT, 9), (FONT, 9, "bold"), (FONT, 14, "bold")

root = tk.Tk()
root.title("LoptoLand")
root.geometry("1900x1200")
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
canvas.pack(fill="both", expand=True)

def set_status(text):
    global status_job
    status_lbl.config(text=text)
    if status_job:
        root.after_cancel(status_job)
    status_job = root.after(4000, lambda: status_lbl.config(text=""))

def close(key):
    entry = popups.pop(key, None)
    if entry:
        frame, window_id = entry
        canvas.delete(window_id)
        try:
            frame.destroy()
        except tk.TclError:
            pass

def close_all():
    for key in list(popups):
        close(key)

def popup_button(parent, text, command):
    return tk.Button(
        parent, text=text, command=command, bg=BTN, fg=FG,
        activebackground=HVR, activeforeground=FG, relief="flat", bd=0,
        padx=12, pady=6, font=FB, cursor="hand2",
    )

def popup(key, title, rows, note):
    close(key)
    frame = tk.Frame(root, bg=PANEL, padx=18, pady=16, highlightthickness=1, highlightbackground=EDGE)
    tk.Label(frame, text=title, bg=PANEL, fg=FG, font=F14).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))
    entries = {}
    first_entry = None

    def apply():
        try:
            values = {k: float(v.get().replace(",", ".")) for k, (v, _, _, _) in entries.items()}
        except ValueError:
            msg.config(text="Enter valid numbers", fg=RED)
            return
        for k, (_, label, low, high) in entries.items():
            if not low <= values[k] <= high:
                msg.config(text=f"{label}: {low:g} to {high:g}", fg=RED)
                return
        S.update(values)
        msg.config(text="Stored. Not simulated yet.", fg=GREEN)
        set_status(f"{title} updated")

    def defaults():
        for k, (var, _, _, _) in entries.items():
            S[k] = DEF[k]
            var.set(f"{S[k]:g}")
        msg.config(text="Defaults restored.", fg=GREEN)
    for i, (name, label, unit, low, high) in enumerate(rows, 1):
        tk.Label(frame, text=label, bg=PANEL, fg=MUTED, font=F9).grid(
            row=i, column=0, sticky="w", padx=(0, 10), pady=4)
        var = tk.StringVar(value=f"{S[name]:g}")
        entry = tk.Entry(
            frame, textvariable=var, width=11, justify="right", bg=BG, fg=FG,
            insertbackground=FG, relief="flat", highlightthickness=1,
            highlightbackground=EDGE, highlightcolor=ACC, font=(FONT, 10, "bold"),)
        entry.grid(row=i, column=1, sticky="ew", pady=4)
        entry.bind("<Return>", lambda _e: apply())
        first_entry = first_entry or entry
        tk.Label(frame, text=unit, bg=PANEL, fg=MUTED, font=F8).grid(
            row=i, column=2, sticky="w", padx=(8, 0), pady=4)
        entries[name] = (var, label, low, high)
    row = len(rows) + 1
    if note:
        tk.Label(frame, text=note, bg=PANEL, fg=MUTED, justify="left",
                 wraplength=360, font=F8).grid(row=row, column=0, columnspan=3, sticky="w", pady=(10, 4))
        row += 1
    msg = tk.Label(frame, text="", bg=PANEL, fg=RED, justify="left", wraplength=360, font=F8)
    msg.grid(row=row, column=0, columnspan=3, sticky="w", pady=(4, 8))
    row += 1
    bar = tk.Frame(frame, bg=PANEL)
    bar.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(4, 0))
    popup_button(bar, "Apply", apply).pack(side="left")
    popup_button(bar, "Defaults", defaults).pack(side="left", padx=(8, 0))
    popup_button(bar, "Close", lambda: close(key)).pack(side="right")
    if first_entry:
        first_entry.focus_set()
    cw = canvas.winfo_width()
    window_id = canvas.create_window(cw / 2, canvas.winfo_height() * POPUP_Y, window=frame, anchor="center", tags="popup")
    popups[key] = (frame, window_id)

def open_world():
    popup("world", "World Physics", WORLD,
          "Co sem cumis, aj tak tomu nechapes")

def open_surfaces():
    popup("surfaces", "Surfaces & Environment", SURF,
          "Co sem cumis, aj tak tomu nechapes")

def save_state():
    data = {
        "format": "loptoland-save", "version": 1,
        "saved_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        **{group: {name: S[name] for name in names} for group, names in GROUPS.items()},
    }
    try:
        with open(SAVE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except OSError as error:
        set_status(f"Save failed: {error}")
        return
    set_status(f"Saved to {os.path.basename(SAVE)}")

def draw_obj(kind, x, y):
    if kind == "Balls":
        canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="#e0a33a", outline="", tags="scene")
    elif kind == "Cube":
        canvas.create_rectangle(x - 18, y - 18, x + 18, y + 18, fill="#5aa9e6", outline="", tags="scene")
    elif kind == "Ramp":
        canvas.create_polygon(x - 28, y + 18, x + 28, y + 18, x + 28, y - 18, fill="#8b98a9", outline="", tags="scene")
    elif kind == "Bumper":
        canvas.create_oval(x - 22, y - 22, x + 22, y + 22, outline="#e04f5f", width=5, tags="scene")
    else:
        canvas.create_rectangle(x - 40, y - 7, x + 40, y + 7, fill="#5c6b7a", outline="", tags="scene")

def redraw(event=None):
    canvas.delete("scene")
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    ax1, ay1, ax2, ay2 = ARENA
    canvas.create_rectangle(ax1 * cw, ay1 * ch, ax2 * cw, ay2 * ch, outline="#3d4654", width=3, tags="scene")
    canvas.create_rectangle(0, 0.74 * ch, cw, ch, fill=PANEL, outline="", tags="scene")
    for kind, x, y in objects:
        draw_obj(kind, x * cw, y * ch)
    for _frame, window_id in popups.values():
        canvas.coords(window_id, cw / 2, ch * POPUP_Y)
        canvas.tag_raise(window_id)

def toggle_pause():
    global paused
    paused = not paused
    pause_btn.config(text="RESUME" if paused else "PAUSE")
    badge_lbl.config(text="PAUSED" if paused else "")
    set_status("Paused" if paused else "Resumed")

def reset():
    global paused
    objects.clear()
    paused = False
    pause_btn.config(text="PAUSE")
    badge_lbl.config(text="")
    close_all()
    set_status("Simulation reset")
    redraw()

def spawn(kind):
    index = len(objects)
    cx = (ARENA[0] + ARENA[2]) / 2
    cy = (ARENA[1] + ARENA[3]) / 2
    objects.append((kind, cx + (index % 5) * 0.04 - 0.08, cy + (index // 5) * 0.05))
    set_status(f"Spawned {kind}")
    redraw()

def mk_button(text, command, x, y, width):
    button = tk.Button(
        root, text=text, command=command, bg=BTN, fg=FG,
        activebackground=HVR, activeforeground=FG, relief="flat", bd=0,
        font=FB, cursor="hand2",
    )
    button.place(relx=x, rely=y - BH, relwidth=width, relheight=2 * BH)
    return button

pause_btn = mk_button("PAUSE", toggle_pause, 0.02, 0.80, 0.07)
mk_button("RESET", reset, 0.10, 0.80, 0.07)
mk_button("SAVE", save_state, 0.18, 0.80, 0.07)
mk_button("EXIT", root.destroy, 0.26, 0.80, 0.07)
mk_button("World Physics", open_world, 0.52, 0.80, 0.14)
mk_button("Surfaces & Environment", open_surfaces, 0.71, 0.80, 0.21)
mk_button("Balls", lambda: spawn("Balls"), 0.16, 0.945, 0.08)
mk_button("Cube", lambda: spawn("Cube"), 0.32, 0.945, 0.08)
mk_button("Ramp", lambda: spawn("Ramp"), 0.48, 0.945, 0.08)
mk_button("Bumper", lambda: spawn("Bumper"), 0.64, 0.945, 0.08)
mk_button("Wall Barrier", lambda: spawn("Wall Barrier"), 0.80, 0.945, 0.13)

for i, text in enumerate(INFO):
    tk.Label(root, text=text, bg=PANEL, fg=MUTED, font=FB, anchor="w").place(relx=0.02 + i * 0.19, rely=0.87, anchor="w")
tk.Label(root, text="SPAWN OBJECTS:", bg=PANEL, fg=FG, font=FB, anchor="w").place(relx=0.02, rely=0.945, anchor="w")
status_lbl = tk.Label(root, text="", bg=BG, fg=GOLD, font=FB, anchor="e")
status_lbl.place(relx=0.965, rely=0.068, anchor="e")
badge_lbl = tk.Label(root, text="", bg=BG, fg=GOLD, font=F14, anchor="n")
badge_lbl.place(relx=0.5, rely=0.085, anchor="n")

canvas.bind("<Configure>", redraw)
root.bind("<Escape>", lambda _e: close_all())

if __name__ == "__main__":
    root.mainloop()
