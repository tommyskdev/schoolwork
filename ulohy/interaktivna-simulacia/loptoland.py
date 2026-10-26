import json
import os
import time
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
drag_obj, last_time = None, 0.0

BG, PANEL, BTN, HVR = "#11151c", "#262c37", "#2b3240", "#3d4654"
FG, MUTED, EDGE, ACC = "#e6edf3", "#8b98a9", "#4a5666", "#5aa9e6"
GOLD, RED, GREEN = "#f2c94c", "#e04f5f", "#65c18c"
ARENA, BH = (0.03, 0.05, 0.97, 0.72), 0.028
POPUP_Y = (ARENA[1] + ARENA[3]) / 2
SIZE = {"Balls": (18, 18), "Cube": (18, 18), "Ramp": (28, 18),
        "Bumper": (22, 22), "Wall Barrier": (40, 7)}
PX_PER_M, REST = 100.0, 0.02  # pixels per metre, rest threshold
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

def shape(kind, x, y):
    if kind == "Ramp":
        return (x - 28, y + 18, x + 28, y + 18, x + 28, y - 18)
    hw, hh = SIZE[kind]
    return (x - hw, y - hh, x + hw, y + hh)

def draw_obj(kind, x, y):
    box = shape(kind, x, y)
    if kind == "Balls":
        return canvas.create_oval(*box, fill="#e0a33a", outline="", tags="scene")
    if kind == "Cube":
        return canvas.create_rectangle(*box, fill="#5aa9e6", outline="", tags="scene")
    if kind == "Ramp":
        return canvas.create_polygon(*box, fill="#8b98a9", outline="", tags="scene")
    if kind == "Bumper":
        return canvas.create_oval(*box, outline="#e04f5f", width=5, tags="scene")
    return canvas.create_rectangle(*box, fill="#5c6b7a", outline="", tags="scene")

def place_obj(obj):
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    canvas.coords(obj["id"], *shape(obj["kind"], obj["x"] * cw, obj["y"] * ch))

def pointer():
    return root.winfo_pointerx() - canvas.winfo_rootx(), root.winfo_pointery() - canvas.winfo_rooty()

def begin_drag(obj):
    global drag_obj
    obj["drag"], obj["rest"] = True, False
    obj["vx"] = obj["vy"] = 0.0
    drag_obj = obj
    canvas.tag_raise(obj["id"])

def spawn_at_cursor(kind):
    px, py = pointer()
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    obj = {"kind": kind, "x": px / cw, "y": py / ch, "vx": 0.0, "vy": 0.0,
           "drag": True, "rest": False, "new": True}
    obj["id"] = draw_obj(kind, px, py)
    objects.append(obj)
    begin_drag(obj)

def grab(event):
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    for obj in reversed(objects):
        hw, hh = SIZE[obj["kind"]]
        if abs(event.x - obj["x"] * cw) <= hw + 4 and abs(event.y - obj["y"] * ch) <= hh + 4:
            begin_drag(obj)
            return

def drag(event=None):
    if drag_obj is None:
        return
    px, py = pointer()
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    drag_obj["x"], drag_obj["y"] = px / cw, py / ch
    place_obj(drag_obj)

def drop(event=None):
    global drag_obj
    obj = drag_obj
    if obj is None:
        return
    drag_obj = None
    obj["drag"] = False
    ax1, ay1, ax2, ay2 = ARENA
    inside = ax1 <= obj["x"] <= ax2 and ay1 <= obj["y"] <= ay2
    if not inside:
        if obj["new"]:
            canvas.delete(obj["id"])
            objects.remove(obj)
            return
        obj["x"] = min(max(obj["x"], ax1), ax2)
        obj["y"] = min(max(obj["y"], ay1), ay2)
    obj["new"] = False
    place_obj(obj)
    set_status(f"Placed {obj['kind']}")

def physics(dt):
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    ax1, ay1, ax2, ay2 = ARENA
    gravity = S["gravity"] * PX_PER_M / ch
    bounce = S["restitution"]
    for obj in objects:
        if obj["drag"] or obj["rest"]:
            continue
        kind = obj["kind"]
        hw, hh = SIZE[kind][0] / cw, SIZE[kind][1] / ch
        left, right, top, bottom = ax1 + hw, ax2 - hw, ay1 + hh, ay2 - hh
        obj["vy"] += gravity * dt
        obj["x"] += obj["vx"] * dt
        obj["y"] += obj["vy"] * dt
        if obj["x"] < left:
            obj["x"] = left
            if obj["vx"] < 0:
                obj["vx"] = -obj["vx"] * bounce
                obj["vy"] *= 1.0 - S["wall_friction"]
        elif obj["x"] > right:
            obj["x"] = right
            if obj["vx"] > 0:
                obj["vx"] = -obj["vx"] * bounce
                obj["vy"] *= 1.0 - S["wall_friction"]
        if obj["y"] < top:
            obj["y"] = top
            if obj["vy"] < 0:
                obj["vy"] = -obj["vy"] * bounce
        if obj["y"] >= bottom:
            obj["y"] = bottom
            if obj["vy"] > 0:
                obj["vy"] = -obj["vy"] * bounce
            obj["vx"] *= max(0.0, 1.0 - S["ground_friction"] * 5.0 * dt)
            if abs(obj["vy"]) < REST and abs(obj["vx"]) < REST:
                obj["vx"] = obj["vy"] = 0.0
                obj["rest"] = True
        place_obj(obj)

def tick():
    global last_time
    now = time.perf_counter()
    dt = min(now - last_time, 0.05)
    last_time = now
    if not paused and any(not o["drag"] and not o["rest"] for o in objects):
        physics(dt)
    root.after(16, tick)

def redraw(event=None):
    canvas.delete("scene")
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    ax1, ay1, ax2, ay2 = ARENA
    canvas.create_rectangle(ax1 * cw, ay1 * ch, ax2 * cw, ay2 * ch, outline="#3d4654", width=3, tags="scene")
    canvas.create_rectangle(0, 0.74 * ch, cw, ch, fill=PANEL, outline="", tags="scene")
    for obj in objects:
        obj["id"] = draw_obj(obj["kind"], obj["x"] * cw, obj["y"] * ch)
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
    global paused, drag_obj
    objects.clear()
    drag_obj = None
    paused = False
    pause_btn.config(text="PAUSE")
    badge_lbl.config(text="")
    close_all()
    set_status("Simulation reset")
    redraw()

def mk_button(text, command, x, y, width):
    button = tk.Button(
        root, text=text, command=command, bg=BTN, fg=FG,
        activebackground=HVR, activeforeground=FG, relief="flat", bd=0,
        font=FB, cursor="hand2",
    )
    button.place(relx=x, rely=y - BH, relwidth=width, relheight=2 * BH)
    return button

def mk_spawn_button(kind, x, y, width):
    button = mk_button(kind, None, x, y, width)
    button.bind("<ButtonPress-1>", lambda _e: spawn_at_cursor(kind))
    return button

pause_btn = mk_button("PAUSE", toggle_pause, 0.02, 0.80, 0.07)
mk_button("RESET", reset, 0.10, 0.80, 0.07)
mk_button("SAVE", save_state, 0.18, 0.80, 0.07)
mk_button("EXIT", root.destroy, 0.26, 0.80, 0.07)
mk_button("World Physics", open_world, 0.52, 0.80, 0.14)
mk_button("Surfaces & Environment", open_surfaces, 0.71, 0.80, 0.21)
mk_spawn_button("Balls", 0.16, 0.945, 0.08)
mk_spawn_button("Cube", 0.32, 0.945, 0.08)
mk_spawn_button("Ramp", 0.48, 0.945, 0.08)
mk_spawn_button("Bumper", 0.64, 0.945, 0.08)
mk_spawn_button("Wall Barrier", 0.80, 0.945, 0.13)

for i, text in enumerate(INFO):
    tk.Label(root, text=text, bg=PANEL, fg=MUTED, font=FB, anchor="w").place(relx=0.02 + i * 0.19, rely=0.87, anchor="w")
tk.Label(root, text="SPAWN OBJECTS:", bg=PANEL, fg=FG, font=FB, anchor="w").place(relx=0.02, rely=0.945, anchor="w")
status_lbl = tk.Label(root, text="", bg=BG, fg=GOLD, font=FB, anchor="e")
status_lbl.place(relx=0.965, rely=0.068, anchor="e")
badge_lbl = tk.Label(root, text="", bg=BG, fg=GOLD, font=F14, anchor="n")
badge_lbl.place(relx=0.5, rely=0.085, anchor="n")

canvas.bind("<Configure>", redraw)
canvas.bind("<ButtonPress-1>", grab)
root.bind("<B1-Motion>", drag)
root.bind("<ButtonRelease-1>", drop)
root.bind("<Escape>", lambda _e: close_all())

if __name__ == "__main__":
    last_time = time.perf_counter()
    root.after(16, tick)
    root.mainloop()
