# LoptoLand — poznámky k prezentácii a technická dokumentácia

**Projekt:** LoptoLand — interaktívna 2D fyzikálna simulácia
**Autor:** Tomáš Molnár
**Súbory:** `loptoland.py` (program), `LoptoLand_prezentacia.pptx` (18 slidov), `poznamky.md` (tento dokument), `prezentacia_obrazky/` (screenshoty)

Prezentácia má 18 slidov. Speaker notes sú vložené aj priamo v PPTX (záložka *Poznámky* / *Notes*).
Screenshoty v prezentácii sú reálne výstupy aplikácie pri rozlíšení 1900 × 1200 px, nie mockupy.

---

## 1. Časový plán (cca 13–15 minút + otázky)

| Čas | Slidy | Obsah | Body |
|---|---|---|---|
| 0:00 – 0:50 | 1 | Predstavenie projektu | úvod |
| 0:50 – 2:30 | 2–4 | Čo program robí, ako sa používa, rozhranie | 8 b |
| 2:30 – 4:15 | 5–7 | 5W, hodnota, versioning a testovacie skupiny | 8 b |
| 4:15 – 7:30 | 8 | Live demo (alebo screenshoty) | 8 b |
| 7:30 – 9:00 | 9–10 | Architektúra a použitá syntax | 10 b |
| 9:00 – 11:00 | 11–12 | Fyzika a kolízie | 10 b |
| 11:00 – 13:00 | 13 | Drag & drop, flick, power throw | 10 b |
| 13:00 – 14:30 | 14–16 | Telemetria, save/load, robustnosť | 10 b |
| 14:30 – 15:00 | 17–18 | Zhrnutie a otázky | 2 b |

**Bodovanie podľa zadania:**
- Úvod a „biznis“ časť (8 b): prezentácia programu, ukážka, 5W, versioning a testovacie skupiny, live demo → slidy 2–8.
- Technická časť (10 b): použité funkcie, fungovanie programu, checklist (premenné, podmienky, cykly, Tkinter, reťazec/zoznam/súbor), vysvetlenie funkcií → slidy 9–16.
- Prezentácia a ďalšie otázky (2 b): zhrnutie, vystupovanie, Q&A → slidy 17–18.

---

## 2. Poznámky k jednotlivým slidom

### Slide 1 — Titulná strana
- Predstav sa, povedz názov a tému.
- Jednou vetou: „LoptoLand je pieskovisko, v ktorom si postavíš malé ihrisko a experimentuješ s fyzikou v reálnom čase.“
- Zdôrazni: jeden súbor `loptoland.py`, žiadne externé knižnice.

### Slide 2 — Čo je LoptoLand
- 2D simulácia v uzavretej aréne (podlaha, strop, steny).
- Používateľ vkladá objekty, chytá ich myšou a hádže.
- Fyzika: gravitácia, odpor vzduchu, trenie, odrazy, rotácia.
- Telemetria: rýchlosť, sila úderu, rotácia, kinetická energia, vektor rýchlosti.
- 5 typov objektov, 9 fyzikálnych parametrov, ~60 FPS.
- Spustenie: `python loptoland.py` (Python 3 + Tkinter, súčasť štandardnej inštalácie).

### Slide 3 — Ako sa to používa
1. **Vyber objekt** — tlačidlá v spodnej lište (Balls, Cube, Ramp, Bumper, Wall Barrier).
2. **Uchop a presuň** — objekt vznikne pod kurzorom a drží sa, kým pustíš tlačidlo.
3. **Hoď** — rýchly švih = flick; podržanie 0,4 s a potiahnutie = nabíjaný power throw (50–500 N).
4. **Sleduj fyziku** — simulácia pokračuje, telemetria sa obnovuje každú snímku.

### Slide 4 — Rozhranie
- Hore: aréna. Stred: ovládanie. Dole: telemetria + spawn.
- Tlačidlá: PAUSE/RESUME, RESET, SAVE, LOAD, EXIT.
- Panely: **World Physics** (gravitácia, smer, hustota vzduchu), **Surfaces & Environment** (odrazivosť, trenie podlahy, trenie stien).
- Skratky: `Ctrl+S` uložiť, `Ctrl+O` načítať, `Esc` zavrieť panely.
- Stavové hlásenie vpravo hore zmizne po 4 s (`root.after`).

### Slide 5 — 5W
- **What:** interaktívna 2D fyzikálna simulácia / sandbox.
- **Why:** abstraktnú fyziku robí viditeľnou; študent vidí vzorec aj dôsledok.
- **Who:** študenti SŠ/VŠ, učitelia fyziky a informatiky, prototypisti.
- **Where:** školská učebňa, domov, workshop — všade, kde je Python.
- **When:** hodiny fyziky/informatiky, samoštúdium, demo, základ pre väčší projekt.
- **How:** Python + Tkinter, jeden súbor, JSON save, bez inštalácie.

### Slide 6 — Hodnota projektu
- Študent: bezpečné experimentovanie, okamžitá odozva, čísla namiesto dohadov.
- Učiteľ: názorná pomôcka offline, bez licencie, spustenie jedným príkazom.
- Vývojár: malý referenčný model kolízií, impulzov a drag & drop v Tkinteri.
- Distribúcia: GitHub / školský server. Model: open-source jadro + workshopy.
- Riziko: desktopové Tkinter UI; ďalší krok je webový port alebo export scén.
- Konkurencia: PhET, Algodoo — väčšie a krajšie, ale LoptoLand je čitateľný a upraviteľný.

### Slide 7 — Versioning a testovacie skupiny
- **v1.0 (interná alpha):** objekty, gravitácia, základný drag & drop.
- **v1.5 (beta):** flick, power throw, telemetria, ladenie kolízií.
- **v2.0 (release):** 3 ms substeps, sleep režim, odpor vzduchu, save/load, robustný load.
- Testovanie:
  - interné (autor): manuálne scenáre, extrémne hodnoty, stabilita;
  - alpha (5 spolužiakov): drag & drop, power throw, zrozumiteľnosť UI;
  - beta (20 študentov + učiteľ): reálna hodina, save/load, zmena gravitácie.
- Save formát má vlastnú verziu (`format`, `version`), aby sa dal bezpečne meniť.
- Feedback sa triedia podľa frekvencie a dopadu; opravy idú do bugfix vydania.

### Slide 8 — Live demo
Poradie (drž sa ho, aby si stihol všetko):
1. Reťazová reakcia: Ramp + Balls nad ňou + kocky pod ňou.
2. Power throw: chyť loptu, podrž 0,5 s, potiahni na Bumper, pusť.
3. Zmena sveta: World Physics → gravitácia 2 m/s², smer 90°, Apply; potom Defaults.
4. Save (Ctrl+S) → RESET → LOAD (Ctrl+O).
5. Otvor `loptoland_save.json` a ukáž štruktúru.
- Fallback: screenshoty v prezentácii + pripravený save súbor.
- Počas dema komentuj každý krok; ak niečo zlyhá, neopravuj naživo.

### Slide 9 — Architektúra
- Jedna slučka `root.after(16, tick)` ≈ 60× za sekundu.
- `tick()`: `update_drag_state()` → `update_aim()` → ak nie je pauza `physics(dt)` + `sync_positions()` → `update_telemetry()`.
- `dt` je reálny čas od posledného ticku, orezaný na 0,05 s.
- `physics(dt)` delí krok na substeps ≤ 3 ms (max 20), aby sa kolízie nestrácali.
- Sekcie súboru: konfigurácia, stav a UI, fyzika, interakcia, perzistencia, slučka.

### Slide 10 — Použité programovacie prvky
Povinný checklist — viď tabuľka nižšie v časti 4.

### Slide 11 — Fyzika
- Jednotky: 100 px = 1 m (`PX_PER_M`), rýchlosť v m/s = `hypot(vx, vy) / 100`.
- Gravitácia: `g = S["gravity"] * 100` px/s²; smer `gx = g·sin θ`, `gy = g·cos θ`.
- Odpor vzduchu: `F = ½·ρ·Cd·A·v²`, v kóde faktor `0.5·ρ·Cd·A·v/m`, potom `v -= faktor·v·dt`.
- `Cd`: lopta 0,47, kocka 1,05; plocha lopty `πr²` (r v metroch), kocka z pixel rozmerov.
- Substepy: `steps = min(20, ceil(dt / 0.003))`, `step = dt / steps`.
- Statické objekty (Ramp, Bumper, Wall Barrier) nemajú gravitáciu: `inv_mass = 0`.

### Slide 12 — Kolízie
- `collide_shapes()` podľa typov: circle–circle, circle–poly, poly–poly.
- Kruh–kruh: vzdialenosť stredov vs. súčet polomerov.
- Kruh–polygón: najbližší bod na hrane; ak je stred vnútri, hľadá sa najbližšia hrana a normála von.
- Polygón–polygón: SAT — projekcia na osi hrán, najmenší prekryv = normála.
- `resolve_pair()`: pozičná korekcia (85 % penetrácie) + normálový impulz `j = −(1+e)·vn / (1/mA + 1/mB)` + trenie limitované `0,15·|j|`.
- Bumper má `e = 1`, ostatné objekty globálne `e`.
- Každý pár sa rieši raz (`i < j`); po párových kolíziách sa ešte raz kontroluje aréna.

### Slide 13 — Drag & drop
- `grab` → `begin_drag` (vynuluje rýchlosť, spustí vzorkovanie) → `drag` (presun) → `update_drag_state` (podržanie) → `update_aim` (nabíjanie) → `drop` (flick / power throw / položenie).
- Flick: rýchlosť z posledných 0,12 s; nad 900 px/s sa násobí 1,45; strop 5200 px/s.
- Power throw: nabitie 1,10 s = 500 N; rýchlosť = `force · 0,02 / mass · 100`.
- Statické objekty sa pri pustení len položia (`vx = vy = 0`).
- Nový objekt pustený mimo arény sa zmaže; existujúci sa vráti do arény.

### Slide 14 — Telemetria
- `active_obj` = posledný chytený alebo hodený objekt; ak nie je v `objects`, hodnoty sú „—“.
- Speed `hypot(vx, vy)/100`; force `last_force`; spin `spin`; KE `½mv²`; vektor `vx/100, vy/100`.
- Aktualizácia každú snímku v `tick()`.

### Slide 15 — Save / Load
- JSON s hlavičkou `format`, `version`, `saved_at`, tromi skupinami parametrov a zoznamom objektov.
- Ukladá sa vedľa skriptu ako `loptoland_save.json`, `indent=2`, `ensure_ascii=False`.
- Load: validácia formátu, `safe_float`, clamp rozsahov, preskočenie neznámeho typu, strop rýchlosti, obnova runtime príznakov, `redraw()`.
- Skratky `Ctrl+S` / `Ctrl+O`.

### Slide 16 — Robustnosť a výkon
- Substepy 3 ms proti tunelovaniu.
- Sleep: pod 7 px/s po 0,55 s → `rest`, prebudenie kolíziou.
- `safe_float` (NaN/inf), validácia popupov, clamp pri load.
- Limity: `dt ≤ 0,05 s`, 20 substeps, 25 vzoriek kurzora, 5200 px/s.

### Slide 17 — Zhrnutie
- Tri odkazy: reálne jednotky, interakcia ktorá učí, kód bez závislostí.
- Ďalšie kroky: viac objektov, CSV export, web port, efekty, výučbové scenáre.

### Slide 18 — Otázky
- Poďakuj, nechaj slide na obrazovke, ponúkni ukážku kódu alebo zmenu gravitácie.

---

## 3. Ako program funguje — funkcia po funkcii

### 3.1 Spustenie a globálny stav

```python
SAVE = .../loptoland_save.json
DEF = {"gravity": 9.81, ..., "ball_spin": 0.0}
S = dict(DEF)              # aktuálne nastavenia
objects = []               # všetky objekty scény (dict)
paused = False
drag_obj = active_obj = None
drag_samples = []          # (čas, x, y) pohyby kurzora
popups = {}                # kľúč -> (Frame, canvas window id)
```

Každý objekt je slovník:

```python
{"kind": "Balls", "x": 0.36, "y": 0.40,      # relatívne súradnice 0..1
 "vx": -480.0, "vy": -380.0,                 # px/s
 "spin": 12.0, "last_force": 205.0,
 "drag": False, "rest": False, "new": False,
 "static": False, "sleep_timer": 0.0,
 "aiming": False, "charge": 0.0, "id": 42}
```

Relatívne súradnice znamenajú, že scéna sa pri zmene veľkosti okna automaticky prepočíta
(`x * canvas_width`). Kolízie sa však robia v absolútnych pixeloch.

### 3.2 Rozhranie (Tkinter)

| Funkcia | Čo robí |
|---|---|
| `set_status(text)` | Zobrazí hlásenie a po 4 s ho zmaže (`root.after`). |
| `popup(key, title, rows, note)` | Vytvorí panel s poliami, Apply/Defaults/Close, validáciou a vloží ho do canvasu cez `create_window`. |
| `close(key)`, `close_all()` | Odstráni panel z canvasu a zničí Frame. |
| `open_world()`, `open_surfaces()` | Otvoria konkrétne panely s definíciou parametrov. |
| `mk_button`, `mk_spawn_button` | Vytvoria tlačidlá; spawn tlačidlá reagujú na `ButtonPress`. |
| `redraw(event)` | Znovu vykreslí arénu a objekty (pri zmene veľkosti okna). |
| `toggle_pause()` | Prepne pauzu a text tlačidla, zobrazí badge PAUSED. |
| `reset()` | Vyčistí scénu, panely, pauzu a prekreslí. |
| `draw_obj(kind, x, y)` | Vytvorí tvar na plátne (oval, obdĺžnik, polygón). |
| `place_obj(obj)` | Nastaví súradnice existujúceho tvaru podľa relatívnych súradníc. |

Panel `popup` pri „Apply“:
1. prevedie všetky polia na `float` (umožní aj desatinnú čiarku),
2. overí rozsah `low..high`,
3. zapíše do `S`,
4. zavolá `wake_all()`, aby sa zmena prejavila aj na spiacich objektoch.

### 3.3 Drag & drop

**`grab(event)`** — `ButtonPress-1` na plátne.
Prechádza objekty od najvrchnejšieho (`reversed(objects)`) a testuje, či kurzor padol do
bounding boxu (`SIZE[kind] + 4 px`). Ak áno, volá `begin_drag(obj)`.

**`begin_drag(obj)`**
- `drag = True`, `rest = False`, `sleep_timer = 0`, `vx = vy = 0`,
- `aiming = False`, `charge = 0`,
- zapamätá `grab_time` a `grab_px` (pozícia kurzora pri chytení),
- inicializuje `drag_samples` prvým bodom,
- nastaví `active_obj` (pre telemetriu) a zdvihne objekt navrch (`tag_raise`).

**`drag(event)`** — `B1-Motion`.
- Pridá `(time, px, py)` do `drag_samples` a nechá len posledných 25 vzoriek.
- Ak objekt nie je v režime nabíjania, presunie ho na pozíciu kurzora.

**`update_drag_state()`**
- Ak držíš objekt na mieste dlhšie ako `HOLD_DELAY = 0,40 s` a kurzor sa od `grab_px`
  nevzdialil viac ako 12 px, zapne `aiming = True` a spustí nabíjanie.
- Vtedy sa objekt prestane hýbať — používateľ mieri.

**`update_aim()`**
- `charge = min(1, (now − charge_start) / CHARGE_TIME)`, `CHARGE_TIME = 1,10 s`.
- Smer `aim_dir` je jednotkový vektor od objektu k kurzoru (ak je vzdialenosť > 10 px).
- Vykreslí šípku dĺžky `50 + 220·charge` a silu `50 + 450·charge` N.
- Všetko je v tagu `"aim"`, takže sa dá jednoducho zmazať.

**`drop(event)`** — pustenie tlačidla. Tri vetvy:
1. **Statický objekt** (Ramp, Bumper, Wall Barrier): `vx = vy = 0`, len sa položí.
2. **Power throw** (`aiming`):
   `force = 50 + 450·charge`;
   `speed = min(5200, force · STRIKE_TIME / mass · PX_PER_M)`, kde `STRIKE_TIME = 0,02 s`.
   Sila sa uloží do `last_force`, lopta dostane `spin` z nastavení.
3. **Flick**: zoberie vzorky za posledných **0,12 s**, vypočíta `vx, vy` z prvého a posledného bodu.
   Ak je rýchlosť > `FLICK_SPEED = 900 px/s`, vynásobí ju `FLICK_BOOST = 1,45`.
   Rýchlosť sa oreže na `MAX_THROW_SPEED = 5200 px/s`.
   `last_force` sa dopočíta ako `m · v / 100 / 0,02`.

Na konci `drop`:
- nový objekt mimo arény sa zmaže,
- existujúci objekt sa clampne do arény,
- `new = False`, `active_obj = obj`, `place_obj(obj)` a status.

**`spawn_at_cursor(kind)`**
Vytvorí objekt presne pod kurzorom, nastaví `drag = True`, `new = True`, vykreslí ho,
pridá do `objects` a zavolá `begin_drag`.

**`wake(obj)` / `wake_all()`**
Zruší spánok (`rest`), aby sa objekt znovu integroval. Statické objekty sa neprebúdzajú.

### 3.4 Fyzika

**`tick()`** — srdce simulácie, `root.after(16, tick)`:
```python
dt = min(now - last_time, 0.05)
update_drag_state()
if not paused and any(not o.static and not o.drag and not o.rest for o in objects):
    physics(dt)
    sync_positions()
update_aim()
update_telemetry()
root.after(16, tick)
```

**`physics(dt)`**
- `steps = max(1, min(20, ceil(dt / 0.003)))`, `step = dt / steps`.
- V každom substep:
  1. pre každý dynamický objekt: gravitácia → odpor vzduchu → integrácia `x += vx·step/cw`.
  2. `collide_arena()` pre všetky objekty.
  3. párové kolízie (`i < j`), staticko-statické páry sa preskakujú.
  4. `collide_arena()` ešte raz (po odtlačení objektov).
  5. sleep timer.

**Gravitácia**
```python
gravity = S["gravity"] * PX_PER_M          # px/s²
gx = gravity * sin(radians(angle))
gy = gravity * cos(radians(angle))
```
Uhol 0° = dole, 90° = doprava, 180° = hore.

**`apply_environment(obj, dt)`** — odpor vzduchu
- Iba Balls a Cube.
- `A` lopty = `π · ball_radius²`, `A` kocky = `(2·hw/100) · (2·hh/100)`.
- `v = hypot(vx, vy) / 100`.
- `factor = 0.5 · ρ · Cd · A · v / m`.
- `vx -= factor · vx · dt`, to isté pre `vy`.
- `Cd`: lopta 0,47, kocka 1,05.

**`collide_arena(obj, cw, ch, dt)`**
- Clampne objekt do arény podľa `body_half_extents`.
- Pri náraze do steny: `vx = -vx · e` (alebo `vy`), tangenciálna zložka sa zníži o `wall_friction`.
- Pri podlahe: `vy = -vy · e`; ak je `|vy| < 7 px/s`, nastaví 0; `vx *= (1 − μ_podlahy · 5 · dt)`.

**`body_mass`, `inv_mass`, `body_restitution`, `body_half_extents`**
- Lopta: `S["ball_mass"]`, kocka: 1,0, statické: ∞ → `inv_mass = 0`.
- Bumper má `e = 1`, inak `S["restitution"]`.
- Rozmery pre clamp: Balls/Bumper = polomer, ostatné `SIZE`.

**`object_collider(obj, cw, ch)`**
Vráti geometrický tvar v absolútnych pixeloch:
- Balls, Bumper → `("circle", (cx, cy), r)`,
- Ramp → trojuholník (polygón),
- Cube / Wall Barrier → obdĺžnik (polygón).

**`collide_shapes(a, b)`**
- circle–circle: `d < r1 + r2`, normála medzi stredmi.
- circle–poly: `circle_polygon()` (vnútri / najbližší bod na hrane).
- poly–poly: `polygon_polygon()` cez SAT.

**`circle_polygon(circle, poly)`**
- Ak je stred kruhu vnútri polygónu: nájde najbližšiu hranu a normálu smerom von.
- Inak: `closest_on_segment()` pre každú hranu, vyberie najbližší bod; ak `d ≤ r`, vráti normálu a penetráciu.

**`polygon_polygon(a, b)`** — SAT
- Pre každú hranu oboch polygónov vytvorí os (normálu).
- Projekcia oboch tvarov na os; ak je prekryv ≤ 0, tvary sa nepretínajú.
- Inak si zapamätá os s najmenším prekryvom — to je normála kolízie.

**`resolve_pair(a, b, normal, penetration, cw, ch)`**
1. **Pozičná korekcia:** `corr = max(0, penetration − 0,5) · 0,85`; posunie `a` a `b` proti sebe podľa `inv_mass`.
2. **Normálový impulz:** `vn = (vB − vA)·n`; ak `vn ≥ 0`, nič (vzďaľujú sa). Inak
   `j = −(1 + e) · vn / (invA + invB)` a upraví rýchlosti.
3. **Trenie:** tangenciálna zložka, impulz limitovaný `0,15 · |j|`.

**Spánok**
- Ak je `hypot(vx, vy) < SLEEP_SPEED (7 px/s)` dlhšie ako `SLEEP_TIME (0,55 s)`,
  objekt dostane `rest = True`, `vx = vy = 0`.
- Spiace objekty sa neintegrujú, ale zostávajú v kolíziách (dá sa na ne položiť iný objekt).
- Prebudí ich kolízia s pohybujúcim sa objektom alebo interakcia používateľa.

### 3.5 Metriky (telemetria)

**`update_telemetry()`**
- `obj = active_obj`; ak už nie je v `objects`, hodnoty sú „—“.
- `speed = hypot(vx, vy) / PX_PER_M`.
- `mass = body_mass(obj)`; `energy = 0,5·mass·speed²` (statické = 0).
- Formát: `8.5 m/s`, `245.0 N`, `15.2 rad/s`, `15.5 J`, `-6.8 / -5.1 m/s`.
- Volá sa každý tick, takže čísla sa menia plynule.

`active_obj` sa nastaví pri `grab`/`begin_drag` a pri `drop`. Po resete alebo vymazaní
objektu sa telemetria vyčistí.

### 3.6 Save / Load

**`safe_float(value, default=0.0)`**
- Skúsi `float()`, pri `TypeError`/`ValueError` vráti default.
- Ak výsledok nie je konečný (`NaN`, `inf`), vráti default.

**`snapshot_object(obj)`**
- Vyberie len serializovateľné polia: `kind, x, y, vx, vy, spin, last_force, static, rest, sleep_timer`.

**`save_state()`**
- Vytvorí:
```python
{
  "format": "loptoland-save",
  "version": 2,
  "saved_at": "2026-11-23T20:12:44+01:00",
  "world_physics": {...},
  "surfaces_environment": {...},
  "ball_defaults": {...},
  "objects": [ {...}, ... ]
}
```
- Zapíše `json.dump(..., indent=2, ensure_ascii=False)`.
- Chyba `OSError` sa zobrazí v statuse, aplikácia nespadne.
- Status: `Saved 4 object(s) to loptoland_save.json`.

**`load_state()`**
1. Otvorí súbor; `FileNotFoundError`, `OSError`, `ValueError` majú vlastné hlásenie.
2. Overí `data["format"] == "loptoland-save"`.
3. Parametre po skupinách: `safe_float`, clamp do rozsahov z `WORLD + SURF`;
   hmotnosť a polomer majú minimum 0,01.
4. Objekty: neznámy `kind` sa preskočí; pozícia sa clampne do arény;
   rýchlosť sa oreže na `MAX_THROW_SPEED`; obnovia sa runtime príznaky
   (`drag=False`, `new=False`, `aiming=False`, `charge=0`).
5. Vyčistí `objects`, drag stav, pauzu, panely a aim; `redraw()`;
   `last_time = time.perf_counter()`, aby prvý `dt` nebol obrovský.

### 3.7 Ostatné pomocné funkcie

| Funkcia | Význam |
|---|---|
| `shape(kind, x, y)` | Vráti súradnice tvaru pre kreslenie. |
| `pointer()` | Pozícia kurzora voči canvasu. |
| `centroid(poly)` | Ťažisko polygónu (pre smer normály). |
| `point_in_polygon(x, y, poly)` | Ray-casting test bodu v polygóne. |
| `closest_on_segment(...)` | Najbližší bod na úsečke. |
| `project_polygon(poly, nx, ny)` | Min/max projekcia pre SAT. |
| `sync_positions()` | Premietne fyzikálne súradnice do canvasu. |

---

## 4. Checklist programovacích prvkov (mapovanie na kód)

| Prvok | Kde | Konkrétny príklad |
|---|---|---|
| **Premenné a konštanty** | všade | `S = dict(DEF)`, `PX_PER_M = 100.0`, `ARENA = (0.03, 0.05, 0.97, 0.72)` |
| **Podmienky** | `drop`, `collide_arena`, `popup.apply` | `if obj.get("static"): ... elif aiming: ... else: ...` |
| **Cykly** | `physics`, `collide_shapes`, `redraw` | `for obj in objects:`, `for i, (obj_a, shape_a) in enumerate(solids):` |
| **Tkinter** | celé UI | `tk.Canvas`, `tk.Button`, `tk.Label`, `root.after(16, tick)`, `bind` |
| **Reťazce** | statusy, JSON, f-stringy | `f"Saved {len(objects)} object(s) to ..."` |
| **Zoznamy** | `objects`, `drag_samples`, `INFO` | `del drag_samples[:-25]`, `reversed(objects)` |
| **Slovník** | `S`, `GROUPS`, `popups`, objekty | `S.update(values)`, `popups[key] = (frame, window_id)` |
| **Súbory** | `save_state`, `load_state` | `with open(SAVE, "w", encoding="utf-8") as f: json.dump(...)` |

---

## 5. Fyzikálne parametre a konštanty

| Konštanta | Hodnota | Význam |
|---|---|---|
| `PX_PER_M` | 100 | 100 px = 1 m |
| `gravity` | 9,81 m/s² | gravitačné zrýchlenie |
| `gravity_angle` | 0–360° | smer gravitácie |
| `air_density` | 1,225 kg/m³ | hustota vzduchu |
| `restitution` | 0,75 | koeficient odrazu |
| `ground_friction` | 0,35 | trenie podlahy |
| `wall_friction` | 0,20 | trenie stien |
| `ball_mass` | 0,43 kg | hmotnosť lopty |
| `ball_radius` | 0,30 m | polomer lopty (pre odpor) |
| `HOLD_DELAY` | 0,40 s | podržanie pred nabíjaním |
| `CHARGE_TIME` | 1,10 s | plné nabitie |
| `MIN_FORCE` / `MAX_FORCE` | 50 / 500 N | rozsah power throw |
| `STRIKE_TIME` | 0,02 s | doba kontaktu pri hode |
| `FLICK_SPEED` | 900 px/s | hranica flicku |
| `FLICK_BOOST` | 1,45× | zosilnenie flicku |
| `MAX_THROW_SPEED` | 5200 px/s | strop rýchlosti |
| `SLEEP_SPEED` | 7 px/s | hranica spánku |
| `SLEEP_TIME` | 0,55 s | čas pod hranicou na uspanie |
| `DRAG_CD` | 0,47 / 1,05 | koeficient odporu lopty / kocky |

Typy a rozmery (`SIZE`): Balls 18×18, Cube 18×18, Ramp 28×18, Bumper 22×22, Wall Barrier 40×7.

---

## 6. Testovacie scenáre (manuálny checklist)

1. **Pád a odraz:** lopta z hora na podlahu → odrazí sa, postupne sa utlmí a uspí.
2. **Rampa:** lopta sa skotúľa po šikmej hrane; over, že neprepadne.
3. **Kocky:** postav 3 kocky na seba → nesmú sa prekrývať ani vibrovať.
4. **Bumper:** hod loptu do bumpera → výrazný odraz (`e = 1`).
5. **Flick:** rýchly švih myšou → lopta letí; pomalý švih → len sa položí.
6. **Power throw:** podrž 0,4 s, potiahni → šípka a sila; pusť → letí správnym smerom.
7. **Hranice:** hoď loptu mimo arény → nová sa zmaže, existujúca sa vráti do arény.
8. **Gravitácia:** nastav 0 → objekty sa vznášajú; 90° → padajú doprava; Defaults vráti 9,81.
9. **Pauza:** počas letu PAUSE → všetko sa zastaví; RESUME pokračuje.
10. **Save/Load:** ulož scénu, RESET, LOAD → rovnaké pozície, rýchlosti aj spánok.
11. **Poškodený save:** zmeň `format` alebo vymaž súbor → jasná chybová hláška, žiadny pád.
12. **Krajné hodnoty:** gravitácia 100, trenie 1, odpor 20 → stabilné, bez NaN.

---

## 7. Odpovede na časté otázky

**Prečo Tkinter a nie pygame?**
Tkinter je v štandardnej knižnici, funguje na Windows/Linux/macOS a na učebný projekt stačí.
Grafika nie je cieľom — cieľom je fyzika a čitateľný kód.

**Prečo 3 ms substeps?**
Pri rýchlosti 5000 px/s objekt prejde 15 px za 3 ms. Bez substepov by mohol preskočiť stenu.
3 ms je kompromis medzi presnosťou a výkonom (max 20 krokov na snímku).

**Ako presne funguje power throw?**
Podržanie 0,40 s na mieste prepne do nabíjania. Po 1,10 s je plná sila 500 N.
Rýchlosť = `force · 0,02 / hmotnosť · 100`. Silnejšia lopta alebo ľahší objekt letí rýchlejšie.

**Prečo je save verzovaný?**
Formát sa môže meniť. `format` a `version` umožnia starý súbor bezpečne odmietnuť alebo migrovať,
namiesto tichého načítania nezmyslov.

**Čo bolo najťažšie?**
Stabilita kolízií pri veľkom `dt` a prechod medzi relatívnymi a absolútnymi súradnicami.
Vyriešili to substeps, pozičná korekcia a dôsledné prepočítavanie `x·cw`, `y·ch`.

**Ako by si projekt rozšíril?**
Viac objektov (pružina, kĺb, magnet), CSV export telemetrie, webový port, zvuky a výučbové scenáre.

**Je to fyzikálne presné?**
Je to herná aproximácia: Eulerova integrácia, impulzové kolízie, kvadratický odpor.
Na výučbu stačí; nie je to inžiniersky simulátor.

---

## 8. Rýchla príprava pred prezentáciou

1. `python loptoland.py` — over, že sa okno otvorí v rozlíšení aspoň 1900×1200 (alebo uprav `geometry`).
2. Priprav si `loptoland_save.json` s ukážkovou scénou.
3. Otvor terminál v priečinku projektu (na demo JSONu).
4. Skontroluj zvuk/prezentér a poznámky v PPTX.
5. Prejdi si live demo raz bez publika — hlavne power throw a reset/load.
