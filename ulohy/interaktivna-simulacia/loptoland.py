import json
import math
import os
import time
import tkinter as tk
from datetime import datetime

SAVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loptoland_save.json")
DEF = {
    "gravity": 9.81, "gravity_angle": 0.0, "air_density": 1.225,
    "restitution": 0.75, "ground_friction": 0.35, "wall_friction": 0.20,
    "ball_mass": 0.43, "ball_radius": 0.30, "ball_spin": 0.0,
}
GROUPS = {
    "world_physics": ("gravity", "gravity_angle", "air_density"),
    "surfaces_environment": ("restitution", "ground_friction", "wall_friction"),
    "ball_defaults": ("ball_mass", "ball_radius", "ball_spin"),
}
WORLD = [
    ("gravity", "Gravity", "m/s²", 0, 100),
    ("gravity_angle", "Gravity direction (0° = down)", "°", 0, 360),
    ("air_density", "Air density (air drag) ρ", "kg/m³", 0, 20),
]
SURF = [
    ("restitution", "Bounce / restitution e", "", 0, 1),
    ("ground_friction", "Ground friction μ", "", 0, 1),
    ("wall_friction", "Wall friction μ", "", 0, 1),
]
INFO = ["SPEED (V)", "STRIKE FORCE (F)", "SPIN", "KINETIC ENERGY", "VECTOR (VX / VY)"]
S = dict(DEF)
objects, paused, status_job, popups = [], False, None, {}
drag_obj, active_obj, last_time = None, None, 0.0
drag_samples = []
info_values = []

BG, PANEL, BTN, HVR = "#11151c", "#262c37", "#2b3240", "#3d4654"
FG, MUTED, EDGE, ACC = "#e6edf3", "#8b98a9", "#4a5666", "#5aa9e6"
GOLD, RED, GREEN = "#f2c94c", "#e04f5f", "#65c18c"
ARENA, BH = (0.03, 0.05, 0.97, 0.72), 0.028
POPUP_Y = (ARENA[1] + ARENA[3]) / 2
SIZE = {"Balls": (18, 18), "Cube": (18, 18), "Ramp": (28, 18),
        "Bumper": (22, 22), "Wall Barrier": (40, 7)}
PX_PER_M = 100.0
FONT = "DejaVu Sans"
F8, F9, FB, F14 = (FONT, 8), (FONT, 9), (FONT, 9, "bold"), (FONT, 14, "bold")

STATIC_KINDS = {"Ramp", "Bumper", "Wall Barrier"}
DRAG_CD = {"Balls": 0.47, "Cube": 1.05}
HOLD_DELAY = 0.40
CHARGE_TIME = 1.10
MIN_FORCE, MAX_FORCE = 50.0, 500.0
STRIKE_TIME = 0.02
FLICK_SPEED = 900.0
FLICK_BOOST = 1.45
MAX_THROW_SPEED = 5200.0
SLEEP_SPEED, SLEEP_TIME = 7.0, 0.55

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
        wake_all()
        msg.config(text="Applied to the simulation.", fg=GREEN)
        set_status(f"{title} updated")

    def defaults():
        for k, (var, _, _, _) in entries.items():
            S[k] = DEF[k]
            var.set(f"{S[k]:g}")
        wake_all()
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
          "zbytocne sem pozeras, aj tak ti to nepomoze.")

def open_surfaces():
    popup("surfaces", "Surfaces & Environment", SURF,
          "co tu hladas, aj tak tomu nerozumies")

def safe_float(value, default=0.0):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default

def snapshot_object(obj):
    return {
        "kind": obj["kind"],
        "x": safe_float(obj["x"]),
        "y": safe_float(obj["y"]),
        "vx": safe_float(obj["vx"]),
        "vy": safe_float(obj["vy"]),
        "spin": safe_float(obj.get("spin", 0.0)),
        "last_force": safe_float(obj.get("last_force", 0.0)),
        "static": obj["kind"] in STATIC_KINDS,
        "rest": bool(obj.get("rest", False)),
        "sleep_timer": safe_float(obj.get("sleep_timer", 0.0)),
    }

def save_state():
    data = {
        "format": "loptoland-save", "version": 2,
        "saved_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        **{group: {name: S[name] for name in names} for group, names in GROUPS.items()},
        "objects": [snapshot_object(obj) for obj in objects],
    }
    try:
        with open(SAVE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except OSError as error:
        set_status(f"Save failed: {error}")
        return
    set_status(f"Saved {len(objects)} object(s) to {os.path.basename(SAVE)}")

def load_state():
    global paused, drag_obj, active_obj, drag_samples, last_time
    try:
        with open(SAVE, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        set_status(f"No save file ({os.path.basename(SAVE)})")
        return
    except (OSError, ValueError) as error:
        set_status(f"Load failed: {error}")
        return
    if not isinstance(data, dict) or data.get("format") != "loptoland-save":
        set_status("Load failed: not a LoptoLand save")
        return
    bounds = {name: (low, high) for name, _label, _unit, low, high in WORLD + SURF}
    for group, names in GROUPS.items():
        saved = data.get(group)
        if not isinstance(saved, dict):
            continue
        for name in names:
            if name not in saved:
                continue
            value = safe_float(saved[name], DEF[name])
            if name in bounds:
                low, high = bounds[name]
                value = max(low, min(high, value))
            elif name in ("ball_mass", "ball_radius"):
                value = max(0.01, value)
            S[name] = value
    raw_objects = data.get("objects")
    if not isinstance(raw_objects, list):
        raw_objects = []
    cw, ch = max(1, canvas.winfo_width()), max(1, canvas.winfo_height())
    ax1, ay1, ax2, ay2 = ARENA
    loaded = []
    for raw in raw_objects:
        if not isinstance(raw, dict) or raw.get("kind") not in SIZE:
            continue
        kind = raw["kind"]
        hw, hh = SIZE[kind]
        x = safe_float(raw.get("x"), (ax1 + ax2) / 2)
        y = safe_float(raw.get("y"), (ay1 + ay2) / 2)
        x = min(max(x, ax1 + hw / cw), ax2 - hw / cw)
        y = min(max(y, ay1 + hh / ch), ay2 - hh / ch)
        vx = safe_float(raw.get("vx"))
        vy = safe_float(raw.get("vy"))
        speed = math.hypot(vx, vy)
        if speed > MAX_THROW_SPEED:
            vx, vy = vx * MAX_THROW_SPEED / speed, vy * MAX_THROW_SPEED / speed
        static = kind in STATIC_KINDS
        loaded.append({
            "kind": kind, "x": x, "y": y, "vx": vx, "vy": vy,
            "drag": False, "rest": False if static else bool(raw.get("rest", False)),
            "new": False, "static": static,
            "sleep_timer": max(0.0, safe_float(raw.get("sleep_timer"))),
            "last_force": max(0.0, safe_float(raw.get("last_force"))),
            "spin": safe_float(raw.get("spin")),
            "aiming": False, "charge": 0.0,
        })
    objects.clear()
    objects.extend(loaded)
    drag_obj = active_obj = None
    drag_samples = []
    paused = False
    pause_btn.config(text="PAUSE")
    badge_lbl.config(text="")
    canvas.delete("aim")
    close_all()
    redraw()
    last_time = time.perf_counter()
    set_status(f"Loaded {len(objects)} object(s) from {os.path.basename(SAVE)}")

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

def wake(obj):
    if obj.get("static"):
        return
    obj["rest"] = False
    obj["sleep_timer"] = 0.0

def wake_all():
    for obj in objects:
        wake(obj)

def body_mass(obj):
    kind = obj["kind"]
    if kind == "Balls":
        return max(0.01, S["ball_mass"])
    if kind == "Cube":
        return 1.0
    return float("inf")

def inv_mass(obj):
    if obj.get("static"):
        return 0.0
    mass = body_mass(obj)
    return 0.0 if mass == float("inf") else 1.0 / mass

def body_restitution(obj):
    if obj["kind"] == "Bumper":
        return 1.0
    return S["restitution"]

def body_half_extents(obj):
    kind = obj["kind"]
    if kind in ("Balls", "Bumper"):
        radius = SIZE[kind][0]
        return radius, radius
    return SIZE[kind]

def object_collider(obj, cw, ch):
    kind = obj["kind"]
    cx, cy = obj["x"] * cw, obj["y"] * ch
    if kind in ("Balls", "Bumper"):
        return ("circle", (cx, cy), SIZE[kind][0])
    if kind == "Ramp":
        return ("poly", [(cx - 28, cy + 18), (cx + 28, cy + 18), (cx + 28, cy - 18)])
    hw, hh = SIZE[kind]
    return ("poly", [(cx - hw, cy - hh), (cx + hw, cy - hh),
                     (cx + hw, cy + hh), (cx - hw, cy + hh)])

def centroid(poly):
    return (sum(p[0] for p in poly) / len(poly),
            sum(p[1] for p in poly) / len(poly))

def point_in_polygon(x, y, poly):
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside

def closest_on_segment(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    if length2 == 0.0:
        return ax, ay
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length2))
    return ax + t * dx, ay + t * dy

def circle_polygon(circle, poly):
    cx, cy, radius = circle[1][0], circle[1][1], circle[2]
    if point_in_polygon(cx, cy, poly):
        ccx, ccy = centroid(poly)
        best_dist, best_normal = -float("inf"), (0.0, -1.0)
        for i in range(len(poly)):
            ax, ay = poly[i]
            bx, by = poly[(i + 1) % len(poly)]
            ex, ey = bx - ax, by - ay
            nx, ny = ey, -ex
            length = math.hypot(nx, ny)
            if length == 0.0:
                continue
            nx, ny = nx / length, ny / length
            mx, my = (ax + bx) / 2, (ay + by) / 2
            if (mx - ccx) * nx + (my - ccy) * ny < 0:
                nx, ny = -nx, -ny
            dist = (cx - ax) * nx + (cy - ay) * ny
            if dist > best_dist:
                best_dist, best_normal = dist, (nx, ny)
        nx, ny = best_normal
        return (-nx, -ny), radius - best_dist
    best_dist = float("inf")
    best_point = (cx, cy)
    best_normal = (0.0, -1.0)
    for i in range(len(poly)):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % len(poly)]
        qx, qy = closest_on_segment(cx, cy, ax, ay, bx, by)
        dist = math.hypot(qx - cx, qy - cy)
        if dist < best_dist:
            best_dist = dist
            best_point = (qx, qy)
    if best_dist > radius:
        return None
    dx, dy = best_point[0] - cx, best_point[1] - cy
    if best_dist < 1e-9:
        ccx, ccy = centroid(poly)
        dx, dy = cx - ccx, cy - ccy
        length = math.hypot(dx, dy) or 1.0
        best_normal = (-dx / length, -dy / length)
    else:
        best_normal = (dx / best_dist, dy / best_dist)
    return best_normal, radius - best_dist

def project_polygon(poly, nx, ny):
    values = [x * nx + y * ny for x, y in poly]
    return min(values), max(values)

def polygon_polygon(poly_a, poly_b):
    axes = []
    for poly in (poly_a, poly_b):
        for i in range(len(poly)):
            ax, ay = poly[i]
            bx, by = poly[(i + 1) % len(poly)]
            nx, ny = -(by - ay), bx - ax
            length = math.hypot(nx, ny)
            if length:
                axes.append((nx / length, ny / length))
    best_overlap, best_axis = float("inf"), None
    for nx, ny in axes:
        amin, amax = project_polygon(poly_a, nx, ny)
        bmin, bmax = project_polygon(poly_b, nx, ny)
        overlap = min(amax, bmax) - max(amin, bmin)
        if overlap <= 0.0:
            return None
        if overlap < best_overlap:
            best_overlap, best_axis = overlap, (nx, ny)
    cax, cay = centroid(poly_a)
    cbx, cby = centroid(poly_b)
    nx, ny = best_axis
    if (cbx - cax) * nx + (cby - cay) * ny < 0:
        nx, ny = -nx, -ny
    return (nx, ny), best_overlap

def collide_shapes(shape_a, shape_b):
    if shape_a[0] == "circle" and shape_b[0] == "circle":
        ax, ay, ar = shape_a[1][0], shape_a[1][1], shape_a[2]
        bx, by, br = shape_b[1][0], shape_b[1][1], shape_b[2]
        dx, dy = bx - ax, by - ay
        dist = math.hypot(dx, dy)
        total = ar + br
        if dist >= total:
            return None
        if dist < 1e-9:
            return (0.0, -1.0), total
        return (dx / dist, dy / dist), total - dist
    if shape_a[0] == "circle":
        return circle_polygon(shape_a, shape_b[1])
    if shape_b[0] == "circle":
        hit = circle_polygon(shape_b, shape_a[1])
        if hit is None:
            return None
        (nx, ny), penetration = hit
        return (-nx, -ny), penetration
    return polygon_polygon(shape_a[1], shape_b[1])

def resolve_pair(obj_a, obj_b, normal, penetration, cw, ch):
    inv_a, inv_b = inv_mass(obj_a), inv_mass(obj_b)
    total_inv = inv_a + inv_b
    if total_inv == 0.0:
        return
    nx, ny = normal
    correction = max(0.0, penetration - 0.5) * 0.85
    obj_a["x"] -= nx * correction * (inv_a / total_inv) / cw
    obj_a["y"] -= ny * correction * (inv_a / total_inv) / ch
    obj_b["x"] += nx * correction * (inv_b / total_inv) / cw
    obj_b["y"] += ny * correction * (inv_b / total_inv) / ch

    rvx = obj_b["vx"] - obj_a["vx"]
    rvy = obj_b["vy"] - obj_a["vy"]
    vn = rvx * nx + rvy * ny
    if vn >= 0.0:
        return
    bounce = max(body_restitution(obj_a), body_restitution(obj_b))
    impulse = -(1.0 + bounce) * vn / total_inv
    obj_a["vx"] -= impulse * nx * inv_a
    obj_a["vy"] -= impulse * ny * inv_a
    obj_b["vx"] += impulse * nx * inv_b
    obj_b["vy"] += impulse * ny * inv_b

    tx, ty = rvx - vn * nx, rvy - vn * ny
    tangent = math.hypot(tx, ty)
    if tangent > 1e-6:
        tx, ty = tx / tangent, ty / tangent
        friction_impulse = -(rvx * tx + rvy * ty) / total_inv
        limit = 0.15 * abs(impulse)
        friction_impulse = max(-limit, min(limit, friction_impulse))
        obj_a["vx"] -= friction_impulse * tx * inv_a
        obj_a["vy"] -= friction_impulse * ty * inv_a
        obj_b["vx"] += friction_impulse * tx * inv_b
        obj_b["vy"] += friction_impulse * ty * inv_b

def apply_environment(obj, dt):
    kind = obj["kind"]
    if kind not in ("Balls", "Cube"):
        return
    mass = body_mass(obj)
    if kind == "Balls":
        radius = max(0.01, S["ball_radius"])
        area = math.pi * radius * radius
    else:
        hw, hh = SIZE["Cube"]
        area = (2 * hw / PX_PER_M) * (2 * hh / PX_PER_M)
    speed = math.hypot(obj["vx"], obj["vy"]) / PX_PER_M
    if speed < 1e-6:
        return
    factor = 0.5 * S["air_density"] * DRAG_CD[kind] * area * speed / mass
    obj["vx"] -= factor * obj["vx"] * dt
    obj["vy"] -= factor * obj["vy"] * dt

def collide_arena(obj, cw, ch, dt):
    if obj.get("static"):
        return
    ax1, ay1, ax2, ay2 = ARENA
    hw, hh = body_half_extents(obj)
    x, y = obj["x"] * cw, obj["y"] * ch
    left, right = ax1 * cw + hw, ax2 * cw - hw
    top, bottom = ay1 * ch + hh, ay2 * ch - hh
    bounce = S["restitution"]
    if x < left:
        x = left
        if obj["vx"] < 0:
            obj["vx"] = -obj["vx"] * bounce
            obj["vy"] *= max(0.0, 1.0 - S["wall_friction"])
    elif x > right:
        x = right
        if obj["vx"] > 0:
            obj["vx"] = -obj["vx"] * bounce
            obj["vy"] *= max(0.0, 1.0 - S["wall_friction"])
    if y < top:
        y = top
        if obj["vy"] < 0:
            obj["vy"] = -obj["vy"] * bounce
            obj["vx"] *= max(0.0, 1.0 - S["wall_friction"])
    elif y > bottom:
        y = bottom
        if obj["vy"] > 0:
            obj["vy"] = -obj["vy"] * bounce
            if abs(obj["vy"]) < SLEEP_SPEED:
                obj["vy"] = 0.0
        obj["vx"] *= max(0.0, 1.0 - S["ground_friction"] * 5.0 * dt)
    obj["x"], obj["y"] = x / cw, y / ch

def physics(dt):
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    gravity = S["gravity"] * PX_PER_M
    angle = math.radians(S["gravity_angle"])
    gravity_x, gravity_y = gravity * math.sin(angle), gravity * math.cos(angle)
    steps = max(1, min(20, int(math.ceil(dt / 0.003))))
    step = dt / steps
    for _ in range(steps):
        for obj in objects:
            if obj.get("static") or obj["drag"] or obj["rest"]:
                continue
            obj["vx"] += gravity_x * step
            obj["vy"] += gravity_y * step
            apply_environment(obj, step)
            obj["x"] += obj["vx"] * step / cw
            obj["y"] += obj["vy"] * step / ch
        for obj in objects:
            if obj["drag"] or obj["rest"]:
                continue
            collide_arena(obj, cw, ch, step)
        solids = [(obj, object_collider(obj, cw, ch)) for obj in objects if not obj["drag"]]
        for i, (obj_a, shape_a) in enumerate(solids):
            moving_a = not obj_a.get("static") and not obj_a["rest"]
            for j in range(i + 1, len(solids)):
                obj_b, shape_b = solids[j]
                if obj_a.get("static") and obj_b.get("static"):
                    continue
                moving_b = not obj_b.get("static") and not obj_b["rest"]
                if not moving_a and not moving_b:
                    continue
                if obj_a["rest"] and moving_b:
                    wake(obj_a)
                if obj_b["rest"] and moving_a:
                    wake(obj_b)
                hit = collide_shapes(shape_a, shape_b)
                if hit is not None:
                    resolve_pair(obj_a, obj_b, hit[0], hit[1], cw, ch)
        for obj in objects:
            if obj["drag"] or obj["rest"]:
                continue
            collide_arena(obj, cw, ch, 0.0)
        for obj in objects:
            if obj.get("static") or obj["drag"] or obj["rest"]:
                continue
            if math.hypot(obj["vx"], obj["vy"]) < SLEEP_SPEED:
                obj["sleep_timer"] += step
                if obj["sleep_timer"] >= SLEEP_TIME:
                    obj["vx"] = obj["vy"] = 0.0
                    obj["rest"] = True
            else:
                obj["sleep_timer"] = 0.0

def sync_positions():
    for obj in objects:
        place_obj(obj)

def update_drag_state():
    obj = drag_obj
    if obj is None or obj.get("static") or obj.get("aiming"):
        return
    now = time.perf_counter()
    if now - obj["grab_time"] < HOLD_DELAY:
        return
    px, py = pointer()
    gx, gy = obj["grab_px"]
    if math.hypot(px - gx, py - gy) <= 12:
        obj["aiming"] = True
        obj["charge_start"] = now
        obj["charge"] = 0.0
        set_status("Power throw: aim with the mouse, release to throw")

def update_aim():
    canvas.delete("aim")
    obj = drag_obj
    if obj is None or not obj.get("aiming"):
        return
    now = time.perf_counter()
    charge = min(1.0, max(0.0, (now - obj["charge_start"]) / CHARGE_TIME))
    obj["charge"] = charge
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    cx, cy = obj["x"] * cw, obj["y"] * ch
    px, py = pointer()
    dx, dy = px - cx, py - cy
    distance = math.hypot(dx, dy)
    if distance > 10:
        obj["aim_dir"] = (dx / distance, dy / distance)
    ax, ay = obj["aim_dir"]
    length = 50 + 220 * charge
    tip_x, tip_y = cx + ax * length, cy + ay * length
    force = MIN_FORCE + (MAX_FORCE - MIN_FORCE) * charge
    canvas.create_line(cx, cy, tip_x, tip_y, arrow="last", arrowshape=(14, 18, 7),
                       fill=GOLD, width=4, tags="aim")
    canvas.create_text(tip_x + ax * 26, tip_y + ay * 26,
                       text=f"{force:.0f} N", fill=GOLD, font=FB, tags="aim")

def update_telemetry():
    obj = active_obj
    if obj not in objects:
        obj = None
    if obj is None:
        values = ["—"] * len(INFO)
    else:
        speed = math.hypot(obj["vx"], obj["vy"]) / PX_PER_M
        mass = body_mass(obj)
        energy = 0.5 * mass * speed * speed if mass != float("inf") else 0.0
        values = [
            f"{speed:.1f} m/s",
            f"{obj.get('last_force', 0.0):.1f} N",
            f"{obj.get('spin', 0.0):.1f} rad/s",
            f"{energy:.1f} J",
            f"{obj['vx'] / PX_PER_M:+.1f} / {obj['vy'] / PX_PER_M:+.1f} m/s",
        ]
    for label, value in zip(info_values, values):
        label.config(text=value)

def begin_drag(obj):
    global drag_obj, active_obj, drag_samples
    obj["drag"], obj["rest"] = True, False
    obj["sleep_timer"] = 0.0
    obj["vx"] = obj["vy"] = 0.0
    obj["aiming"] = False
    obj["charge"] = 0.0
    obj["grab_time"] = time.perf_counter()
    obj["grab_px"] = pointer()
    obj["aim_dir"] = (0.0, -1.0)
    obj.setdefault("static", obj["kind"] in STATIC_KINDS)
    obj.setdefault("last_force", 0.0)
    obj.setdefault("spin", 0.0)
    drag_obj = obj
    active_obj = obj
    drag_samples = [(obj["grab_time"],) + obj["grab_px"]]
    canvas.tag_raise(obj["id"])

def spawn_at_cursor(kind):
    px, py = pointer()
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    obj = {"kind": kind, "x": px / cw, "y": py / ch, "vx": 0.0, "vy": 0.0,
           "drag": True, "rest": False, "new": True,
           "static": kind in STATIC_KINDS, "sleep_timer": 0.0,
           "last_force": 0.0, "spin": 0.0}
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
    global drag_samples
    if drag_obj is None:
        return
    px, py = pointer()
    now = time.perf_counter()
    drag_samples.append((now, px, py))
    del drag_samples[:-25]
    if drag_obj.get("aiming"):
        return
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    drag_obj["x"], drag_obj["y"] = px / cw, py / ch
    place_obj(drag_obj)

def drop(event=None):
    global drag_obj, active_obj, drag_samples
    obj = drag_obj
    if obj is None:
        return
    now = time.perf_counter()
    px, py = pointer()
    aiming = obj.get("aiming", False)
    drag_obj = None
    obj["drag"] = False
    obj["aiming"] = False
    status = f"Placed {obj['kind']}"
    if obj.get("static"):
        obj["vx"] = obj["vy"] = 0.0
    elif aiming:
        charge = obj.get("charge", 0.0)
        force = MIN_FORCE + (MAX_FORCE - MIN_FORCE) * charge
        dx, dy = obj.get("aim_dir", (0.0, -1.0))
        speed = min(MAX_THROW_SPEED, force * STRIKE_TIME / body_mass(obj) * PX_PER_M)
        obj["vx"], obj["vy"] = dx * speed, dy * speed
        obj["last_force"] = force
        obj["spin"] = S["ball_spin"] if obj["kind"] == "Balls" else 0.0
        status = f"Power throw {force:.0f} N"
    else:
        drag_samples.append((now, px, py))
        cutoff = now - 0.12
        recent = [sample for sample in drag_samples if sample[0] >= cutoff]
        vx = vy = 0.0
        if len(recent) >= 2:
            t0, x0, y0 = recent[0]
            t1, x1, y1 = recent[-1]
            elapsed = t1 - t0
            if elapsed > 1e-4:
                vx, vy = (x1 - x0) / elapsed, (y1 - y0) / elapsed
        speed = math.hypot(vx, vy)
        flick = speed > FLICK_SPEED
        if flick:
            vx, vy, speed = vx * FLICK_BOOST, vy * FLICK_BOOST, speed * FLICK_BOOST
        if speed > MAX_THROW_SPEED:
            scale = MAX_THROW_SPEED / speed
            vx, vy, speed = vx * scale, vy * scale, MAX_THROW_SPEED
        obj["vx"], obj["vy"] = vx, vy
        obj["last_force"] = body_mass(obj) * speed / PX_PER_M / STRIKE_TIME if speed else 0.0
        if flick:
            obj["spin"] = S["ball_spin"] if obj["kind"] == "Balls" else 0.0
            status = f"Flick kick {speed / PX_PER_M:.1f} m/s"
        elif speed > 0:
            status = f"Threw {obj['kind']} at {speed / PX_PER_M:.1f} m/s"
    obj["rest"] = False
    obj["sleep_timer"] = 0.0
    ax1, ay1, ax2, ay2 = ARENA
    inside = ax1 <= obj["x"] <= ax2 and ay1 <= obj["y"] <= ay2
    if not inside:
        if obj["new"]:
            canvas.delete(obj["id"])
            objects.remove(obj)
            return
    hw, hh = body_half_extents(obj)
    cw, ch = canvas.winfo_width(), canvas.winfo_height()
    obj["x"] = min(max(obj["x"], ax1 + hw / cw), ax2 - hw / cw)
    obj["y"] = min(max(obj["y"], ay1 + hh / ch), ay2 - hh / ch)
    obj["new"] = False
    active_obj = obj
    place_obj(obj)
    set_status(status)

def tick():
    global last_time
    now = time.perf_counter()
    dt = min(now - last_time, 0.05)
    last_time = now
    update_drag_state()
    if not paused and any(not o.get("static") and not o["drag"] and not o["rest"] for o in objects):
        physics(dt)
        sync_positions()
    update_aim()
    update_telemetry()
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
    global paused, drag_obj, active_obj, drag_samples
    objects.clear()
    drag_obj = active_obj = None
    drag_samples = []
    paused = False
    pause_btn.config(text="PAUSE")
    badge_lbl.config(text="")
    canvas.delete("aim")
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
mk_button("LOAD", load_state, 0.26, 0.80, 0.07)
mk_button("EXIT", root.destroy, 0.34, 0.80, 0.07)
mk_button("World Physics", open_world, 0.52, 0.80, 0.14)
mk_button("Surfaces & Environment", open_surfaces, 0.71, 0.80, 0.21)
mk_spawn_button("Balls", 0.16, 0.945, 0.08)
mk_spawn_button("Cube", 0.32, 0.945, 0.08)
mk_spawn_button("Ramp", 0.48, 0.945, 0.08)
mk_spawn_button("Bumper", 0.64, 0.945, 0.08)
mk_spawn_button("Wall Barrier", 0.80, 0.945, 0.13)

for i, text in enumerate(INFO):
    tk.Label(root, text=text, bg=PANEL, fg=MUTED, font=FB, anchor="w").place(relx=0.02 + i * 0.19, rely=0.87, anchor="w")
    value_lbl = tk.Label(root, text="—", bg=PANEL, fg=FG, font=FB, anchor="w")
    value_lbl.place(relx=0.02 + i * 0.19, rely=0.905, anchor="w")
    info_values.append(value_lbl)
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
root.bind("<Control-s>", lambda _e: save_state())
root.bind("<Control-o>", lambda _e: load_state())

if __name__ == "__main__":
    last_time = time.perf_counter()
    root.after(16, tick)
    root.mainloop()
