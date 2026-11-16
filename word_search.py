import random, time, tkinter as tk
import tkinter.font as tkfont

N, TIME_LIMIT, NUM_WORDS, MAX_EFFORT = 8, 180, 10, 3000
POOL = ["HOUSE", "WATER", "APPLE", "TABLE", "CHAIR", "MUSIC", "LIGHT", "PHONE", "BREAD",
        "GREEN", "SMILE", "RIVER", "CLOUD", "PLANT", "TRAIN", "SUGAR", "MONEY", "HAPPY",
        "SUMMER", "WINTER", "GARDEN", "FRIEND", "FAMILY", "SCHOOL", "WINDOW", "DOCTOR",
        "ORANGE", "KITCHEN", "MORNING", "COUNTRY", "BIRTHDAY", "MOUNTAIN", "ANIMAL",
        "BASKET", "CANDLE", "DRAGON", "ENGINE", "FOREST", "GUITAR", "HOLIDAY", "JACKET",
        "JUNGLE", "LEMON", "MARKET", "NATURE", "PENCIL", "PUZZLE", "ROCKET", "SILVER",
        "TOMATO", "TURTLE", "VALLEY", "BUTTER", "CAMERA", "DESERT", "FLOWER", "PARROT",
        "PICNIC", "PILLOW", "RABBIT", "SPIDER", "SPRING", "STREAM", "TICKET", "BOTTLE",
        "CASTLE", "CIRCLE", "COOKIE", "HAMMER", "ISLAND", "LADDER", "MIRROR", "OCEAN",
        "PEPPER", "PURPLE", "SALAD", "SQUARE", "TEMPLE", "WIZARD", "CLEVER", "BRAVE", "QUICK", "HAPPY", "BRIGHT", "CALM", "EAGER", "FANCY", "GENTLE",
        "JOLLY", "KIND", "LIVELY", "MERRY", "NEAT", "OLD", "NEW", "YOUNG", "BIG", "SMALL", "TALL", "SHORT", "LONG", "ROUND", "SQUARE", "SOFT", "HARD",
        "STRONG", "WEAK", "FAST", "SLOW", "HOT", "COLD", "WARM", "COOL", "DRY",
        "WET", "LIGHT", "DARK", "CLEAN", "DIRTY", "RICH", "POOR", "FULL", "EMPTY", "SWEET", "SOUR",
        "BITTER", "SALTY", "FRESH", "STALE", "SHARP", "DULL", "SMOOTH"]
POOL = [w for w in POOL if len(w) <= N]
DIRS = [(0, 1), (1, 0), (1, 1)]
PALETTE = ["#ff9999", "#99ccff", "#99ff99", "#ffcc66", "#cc99ff", "#66ffff", "#ff99dd",
           "#ffff66", "#ffb366", "#b3ff66", "#d9d9d9", "#e6b3ff", "#b3e6b3", "#ffd9b3"]


def placements(grid, word):
    out = []
    for r in range(N):
        for c in range(N):
            for dr, dc in DIRS:
                cells = [(r + dr * i, c + dc * i) for i in range(len(word))]
                if all(0 <= y < N and 0 <= x < N and grid[y * N + x] in ".%s" % ch
                       for (y, x), ch in zip(cells, word)):
                    out.append(cells)
    return out


def place(grid, word, cells):
    g = list(grid)
    for (y, x), ch in zip(cells, word):
        g[y * N + x] = ch
    return "".join(g)


def neighbour_count(grid, cells):
    return sum(0 <= y + dy < N and 0 <= x + dx < N and grid[(y + dy) * N + x + dx] != "."
               for y, x in cells for dy in (-1, 0, 1) for dx in (-1, 0, 1))


STYLES = {
    "overlap": lambda grid, cells: -sum(grid[y * N + x] != "." for y, x in cells),
    "spread": neighbour_count,
    "random": lambda grid, cells: random.random(),
}
history = {s: [] for s in STYLES}


def pick_style():
    for s in STYLES:
        if not history[s]:
            return s
    if random.random() < 0.2:
        return random.choice(list(STYLES))
    return min(STYLES, key=lambda s: sum(history[s]) / len(history[s]))


class TooHard(Exception): pass


effort = backtracks = 0


def backtrack(grid, words, i, style):
    global effort, backtracks
    if i == len(words):
        return grid
    options = placements(grid, words[i])
    random.shuffle(options)
    options.sort(key=lambda cells: STYLES[style](grid, cells))
    for cells in options:
        effort += 1
        if effort > MAX_EFFORT:
            raise TooHard
        result = backtrack(place(grid, words[i], cells), words, i + 1, style)
        if result:
            return result
        backtracks += 1
    return None


def make_puzzle():
    global effort, backtracks
    while True:
        style = pick_style()
        words = sorted(random.sample(POOL, NUM_WORDS), key=len, reverse=True)
        effort = backtracks = 0
        try:
            grid = backtrack("." * (N * N), words, 0, style)
        except TooHard:
            history[style].append(MAX_EFFORT)
            continue
        if grid:
            history[style].append(effort)
            filler = "".join(words)
            grid = "".join(random.choice(filler) if ch == "." else ch for ch in grid)
            return words, grid, style, effort, backtracks


# ---------------- GAME / GUI ----------------
root = tk.Tk()
root.title("AI Word Search")
state = dict(words=[], grid="", found={}, done=set(), first=None, preview=[],
             left=0, score=0, running=False, job=None, colors={})
normal_font = tkfont.Font(family="Arial", size=12, weight="bold")
strike_font = tkfont.Font(family="Arial", size=12, weight="bold", overstrike=1)

top = tk.Frame(root); top.pack(pady=5)
tk.Button(top, text="New Game", command=lambda: new_game()).pack(side="left", padx=5)
hint_btn = tk.Button(top, text="Hide hints", command=lambda: toggle_hints())
hint_btn.pack(side="left", padx=5)
info = tk.Label(root, font=("Arial", 12)); info.pack()
msg = tk.Label(root, font=("Arial", 12, "bold")); msg.pack()
main = tk.Frame(root); main.pack(padx=10, pady=5)
board = tk.Frame(main); board.pack(side="left")
wordpanel = tk.Frame(main); wordpanel.pack(side="left", padx=20, anchor="n")
tk.Label(wordpanel, text="Find these words:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
wordlabel = tk.Label(root, font=("Arial", 12)); wordlabel.pack()
note = tk.Label(root, font=("Arial", 11), fg="red"); note.pack()
statlabel = tk.Label(root, font=("Arial", 9), fg="gray"); statlabel.pack(pady=5)
labels = []
word_labels = []


def toggle_hints():
    if wordpanel.winfo_ismapped():
        wordpanel.pack_forget()
        hint_btn.config(text="Show hints")
    else:
        wordpanel.pack(side="left", padx=20, anchor="n")
        hint_btn.config(text="Hide hints")


def build_board():
    for l in labels:
        l.destroy()
    labels.clear()
    for r in range(N):
        for c in range(N):
            l = tk.Label(board, width=3, height=1, font=("Arial", 18, "bold"), relief="ridge")
            l.grid(row=r, column=c)
            l.bind("<ButtonPress-1>", lambda e, r=r, c=c: press(r, c))
            l.bind("<B1-Motion>", motion)
            l.bind("<ButtonRelease-1>", release)
            labels.append(l)


def build_word_list(words):
    for w, l in word_labels:
        l.destroy()
    word_labels.clear()
    for w in words:
        l = tk.Label(wordpanel, text=w, font=normal_font, anchor="w", width=12)
        l.pack(anchor="w", pady=2)
        word_labels.append((w, l))


def refresh():
    for k, l in enumerate(labels):
        cell = (k // N, k % N)
        color = state["found"].get(cell, "white")
        if cell in state["preview"]:
            color = "orange"
        if state["first"] == cell:
            color = "yellow"
        l.config(text=state["grid"][k], bg=color)
    for w, l in word_labels:
        if w in state["done"]:
            l.config(font=strike_font, fg="gray", bg=state["colors"][w])
        else:
            l.config(font=normal_font, fg="black", bg="white")
    wordlabel.config(text="Words found: %d / %d" % (len(state["done"]), len(state["words"])))
    info.config(text="Time: %d   Score: %d" % (state["left"], state["score"]))


def new_game():
    if state["job"]:
        root.after_cancel(state["job"])
    note.config(text="")
    t = time.time()
    words, grid, style, tries, undone = make_puzzle()
    colors = {w: PALETTE[i % len(PALETTE)] for i, w in enumerate(words)}
    state.update(words=words, grid=grid, found={}, done=set(), first=None,
                 left=TIME_LIMIT, running=True, colors=colors)
    build_word_list(words)
    msg.config(text="AI used '%s': %d attempts, %d backtracks, %.2fs"
               % (style, tries, undone, time.time() - t), fg="black")
    statlabel.config(text="AI's avg attempts (lower = better):  " + "   ".join(
        "%s %.0f" % (s, sum(v) / len(v)) for s, v in history.items() if v))
    refresh()
    tick()


def tick():
    if not state["running"]:
        return
    if state["left"] <= 0:
        state["running"] = False
        msg.config(text="TIME'S UP - YOU LOSE", fg="red")
        return
    state["left"] -= 1
    refresh()
    state["job"] = root.after(1000, tick)


def cell_at(e):
    for k, l in enumerate(labels):
        x, y = l.winfo_rootx(), l.winfo_rooty()
        if x <= e.x_root < x + l.winfo_width() and y <= e.y_root < y + l.winfo_height():
            return (k // N, k % N)
    return None


def line(start, end):
    (r0, c0), (r, c) = start, end
    dy, dx = r - r0, c - c0
    if dy and dx and abs(dy) != abs(dx):
        return []
    n = max(abs(dy), abs(dx)) + 1
    sy, sx = (dy > 0) - (dy < 0), (dx > 0) - (dx < 0)
    return [(r0 + sy * i, c0 + sx * i) for i in range(n)]


def press(r, c):
    if state["running"]:
        state["first"] = (r, c)
        refresh()


def motion(e):
    if state["running"] and state["first"] is not None:
        end = cell_at(e)
        state["preview"] = line(state["first"], end) if end else []
        refresh()


def release(e):
    if state["running"] and state["first"] is not None:
        end = cell_at(e)
        if end and end != state["first"]:
            before = len(state["done"])
            check_line(line(state["first"], end))
            if len(state["done"]) == before:
                note.config(text="Not one of the hidden words")
                root.after(1500, lambda: note.config(text=""))
    state["first"], state["preview"] = None, []
    refresh()


def check_line(cells):
    text = "".join(state["grid"][y * N + x] for y, x in cells)
    for w in state["words"]:
        if w not in state["done"] and text == w:
            state["done"].add(w)
            for cell in cells:
                state["found"][cell] = state["colors"][w]
            state["score"] += 10 * len(w)
    if len(state["done"]) == len(state["words"]):
        state["running"] = False
        state["score"] += state["left"]
        msg.config(text="YOU WIN!", fg="green")


build_board()
new_game()
root.mainloop()
