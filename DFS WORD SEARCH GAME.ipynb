import random, time, tkinter as tk
# random -> مكتبة بتخليك تختار عشوائي سواء كانت من ليستاية او رقم واستعملناها في اللابات
# time -> بتحسب الوقت اللي بيعدي هنحتاجها في الواجهة 
# tkinter -> دي مكتبة بتاعت بايثون استخدمناها عشان نعمل الواجهة الاساسية لو محدش غيرها
N, TIME_LIMIT, NUM_WORDS, MAX_EFFORT = 8, 300, 10, 1000
# N -> grid size aka 8*8 , TIME_LIMIT -> literally time limit in seconds
# NUM_WORDS ->  عدد الكلام المستعمل في اللعبة انا شايف انو 10 احسن حاجة عشان هتوضح ليه بنفضل ستايلات على ستايلات تانية 
# MAX_EFFORT -> اعلى عدد من محاولات انك تحط كلمة في اماكن مختلفة 
HINT_COST = 5   # points taken off for each hint
POOL = ["HOUSE", "WATER", "APPLE", "TABLE", "CHAIR", "MUSIC", "LIGHT", "PHONE", "BREAD",
        "GREEN", "SMILE", "RIVER", "CLOUD", "PLANT", "TRAIN", "SUGAR", "MONEY", "HAPPY",
        "SUMMER", "WINTER", "GARDEN", "FRIEND", "FAMILY", "SCHOOL", "WINDOW", "DOCTOR",
        "ORANGE", "KITCHEN", "MORNING", "COUNTRY", "BIRTHDAY", "MOUNTAIN", "ANIMAL"]
# هنا زود كلام براحتك في الليستاية دي اهم حاجة الكلمة متعديش ال 8 حروف
DIRS = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]
# دي الاتجهات هنحتاجها في المعادلة تحت على طول

# Finds all valid grid positions for a word.
def placements(grid, word):
# هنا الفنكشن دي بتتاكد من كل الاماكن اللي كل حرف من الكلمة ينفع يتحط فيها لو المكان فيه نفس الحرف او فاضي هيعدي غير كدا هنروح للي بعدها
    out = []
    for r in range(N):
        for c in range(N):
            for dr, dc in DIRS:
# السطر اللي تحت ده من الاخر بيعمل ليستاية جواها كل الاماكن اللي الكلمة ينفع تتحط فيها بيجرب كل الاتجاهات وكل عمود في كل صف 
# CAT مثال على كلمة 
# cat is 3 letters so index 0 1 2 , cells is a list which will have three tuples of placements for each letter of the word cat 
#let's say the index row in the loop is 3 and column is 2 and the direction is (1,-1) the loop underneath will make the cells = [(3,2),(4,1),(5,0)]
#which if you look at the grid is a diagonal from right to left      
                cells = [(r + dr * i, c + dc * i) for i in range(len(word))]
                if all(0 <= y < N and 0 <= x < N and grid[y * N + x] in ".%s" % ch
                       for (y, x), ch in zip(cells, word)):
# all makes sure that every condition is true
# first zip(cells,word) makes it so that every placement is with it's character in the word like this ((3, 2), 'C'), ((4, 1), 'A'), ((5, 0), 'T') 
# so the if condition only makes sure that everything is true as in y "row index" is bigger or equal to 0 and smaller than the number of grid which is 8 so maximum index is 7
# column is same as row and that the cell number since our grid is literally a big string of N*N we calculate the index number using y * N + x we make sure that it's either a . which is empty or the character that we are iterating through and if allat is True we append the cells to out
                    out.append(cells)
    return out

# Puts a word's letters onto the grid.
# هنا الفنكشن دي حرفيا بتحط الحروف في مكانها في الجريد
def place(grid, word, cells):
#  بتاخد كوبي من الجريد وبتحطها في ليست عشان تعدل عليها  
    g = list(grid)
    for (y, x), ch in zip(cells, word):
        g[y * N + x] = ch
# هنا ال ريتيرن بترجع الليستاية كا سترينج تاني بعد ما اتعدل عليها
    return "".join(g)


# دي التلت ستايلات اللي عندنا كل واحدة بتاخد الجريد والسيلز وبتشتغل عليهم 
STYLES = {
    # overlap 
    # sort كل مكان في السيلز عبارة عن مكان على الجريد الفنكشن بترجع مجموع الاماكن اللي لقيتها مش فاضية وبتحط في الاخر سالب عشان فنشن ال 
    # تعتبرها اختيار افضل
    "overlap": lambda grid, cells: -sum(grid[y * N + x] != "." for y, x in cells),
    # بالنسبة لل edge
    #   هنا بتفضل لما تبقى اماكن السيلز بعيدة عن النص بتاع الجريد مثال لو حسبت مجموع السيلز دي
    # (0,0) , (0,1) , (0,2)
    # outcome : 18 and with the outside negative it becomes -18 وزي ما قولت السالب بيخليها افضل لما نستعمل عليها فنكشن السورت
    "edge":    lambda grid, cells: -sum(abs(y - (N - 1) / 2) + abs(x - (N - 1) / 2) for y, x in cells),
    # هنا حرفيا عشوائية وكل ما كان الرقم اصغر كل ما فنكشن السورت اعتمدته الاول
    "random":  lambda grid, cells: random.random(),
}
# هنا حرفيا ديكشنري لكل ستايل جواه ليست فاضية هتتملي بعدين بعدد المحاولات الستايل احتاجها عشان يعمل لعبة لما نستعملهم عشان نعرف اني واحدة اسهل واحسن 
history = {s: [] for s in STYLES} 


# Picks the best or random AI placement style.
def pick_style():
#هنا هيشوفهم واحد واحد قبل اي حاجة هيشوف لو الستايل في الديكشنري عبارة عن ليستاية فاضية هيجربه عشان مجربهوش قبل كدا
    for s in STYLES:
        if not history[s]:
            return s
#    فيه نسبة انو يجرب ستايل عشوائي لو الرقم العشوائي طلع اقل من 0.2 او نسبة 20% يعني
    if random.random() < 0.2:                      
        return random.choice(list(STYLES))
#  لو عدا من كل حاجة من دي في العادي بيختار احسن ستايل بانه بيروح لكل واحد ويحسب عدد محاولاته على اشتغل كام مرة واقل رقم هيطلع احسن واحد فا هيختاره
# example : history = {
#    "overlap": [100, 200, 300],
#    "edge": [50, 60, 70],
#    "random": [400, 500, 600]
#}     
# (100 + 200 + 300) / 3 = 200 , (50 + 60 + 70) / 3 = 60 , (400 + 500 + 600) / 3 = 500
# edge اقل رقم ال
    return min(STYLES, key=lambda s: sum(history[s]) / len(history[s]))

# exception هنحتاج ال   
# عشان احنا في ال فنكشن اللي بعدها باكتراك هنقعد ننادي الفنكشن جوا نفسها كتير فا لما عدد المحاولات يعدي الماكس بتاعنا اللي هو كان 1000 عايزين نطلع من كل الفنكشنز اللي جوا بعض دي على طول
class TooHard(Exception):
    pass

# دي زي وكانك عملت كل واحدة لوحدها عادي هي هي
effort = backtracks = 0
chosen = []          # NEW: cells of every word placed so far, in order (same order as words)

# Recursively places all words onto the grid.
# هنا بقى واحدة واحدة انا هشرحها كاملة من فوق هنا عشان مينفعش ادخل جواها هيبقى شكلها معقد
# grid -> N*N string of "." , words -> list of randomly selected words , i which is index which is 0 , style -> chosen style
# uses the same global variables that are outside the function
# if i == len(words) that means the function recurred till the end with no issues 
# we get this possible placements for the current grid and the current word inside a variable named options and we shuffle them so it lowers the chance of getting the same puzzle twice
# and then we sort them using the selected style and yes even if we sort them we still need the shuffle since if two placements have the same value the sort is gonna leave them as their original order
# again options are like this options = [  [(0, 0), (0, 1), (0, 2)], [(2, 1), (2, 2), (2, 3)], [(4, 3), (4, 4), (4, 5)]  ] so cells in options are a list of tuples 
# now for every time we try a cell the effort += 1 so we can measure if it's taking too many attempts and it's not worth it and if we go over the max effort we raise the exception toohard which interrupts every function in the recursion and stops them
# now for the bigger picture now let's say the first word is DOG the second is OWL now we go through every cell in options for DOG now let's say we go through the first one now the result awaits for another call of the function backtrack 
# but this time it's a new grid which is a copy of the original modified with the placement that we used for DOG and i + 1 so it goes to the next word which is OWL now again we see all the possible options for this word with the new grid which DOG is placed in already
# now we try the same thing with OWL we go through all of it's possible cells now let's say we go through the first one the same cycle repeats with the next words but if the next word doesn't have a valid placement we go back one cycle now let's say we chose a placement for OWL and then the next cycle was FOX but FOX doesn't have any valid placement 
# then it returns None for the previous cycle which was OWL now owl's loop tries another placement and i think you get the idea by now now let's say it all worked out and the final word found a valid placement the new word placement is placed in the new copied grid it made and the first condition becomes True which then returns the final grid of all placed words the final grid keeps returning to the previous cycles till it returns to the very first one and returns the final grid
# now again if the effort exceeds max effort we raise the too hard exception and all of this recursion is interrupted and it doesn't make any problems since every cycle edits it's own copied grid
# also everytime a cycle returns None to it's previous cycle and it makes it's loop try another placement (cells in options) we add + 1 to the backtracks 
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
        chosen.append(cells)                       # NEW: try this placement
        result = backtrack(place(grid, words[i], cells), words, i + 1, style)
        if result:
            return result
        chosen.pop()                               # NEW: it failed, undo it
        backtracks += 1
    return None


# Generates a new complete word search puzzle.
def make_puzzle():
    # uses the same global effort , backtracks variables
    global effort, backtracks
    while True:
    # using the pick_style function to pick a style
        style = pick_style()
    # picking random different words from the pool of words how many is indicated by the NUM_WORDS variable
        words = random.sample(POOL, NUM_WORDS)
    # long words first = fewer dead ends   
        words.sort(key=len, reverse=True)  
    # zeroing everything every loop
        effort = backtracks = 0
        chosen.clear()                              # NEW
        try:
    # here we try the backtrack function to make the grid of our game
            grid = backtrack("." * (N * N), words, 0, style)
        except TooHard:
    # and if we ever raise the toohard exception we catch it here and append to the list of the of the style key in the dictionary and we continue another round of the loop so in summary we try again
            history[style].append(MAX_EFFORT)       # punish the style, then try again
            continue
    # here if we actually succeed and get our final grid with all the valid placements 
        if grid:
    # we append the number of efforts it took to the list of the of the style key in the dictionary so that we can check if this is the most efficient when making another puzzle by it taking fewer attempts on average
            history[style].append(effort)   
            # here we just take the final grid and if there is an empty position which is indicated by "." we replace it with a random character and if not we leave the original character
            grid = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") if ch == "." else ch
                           for ch in grid)
            # NEW: also return where every word was placed {word: cells}
            return words, grid, style, effort, backtracks, dict(zip(words, chosen))


# ---------------- GAME / GUI PART (CREAM EDITION) ----------------
import tkinter.font as tkfont
import math

# ---- الألوان: كلها هنا وتقدر تغيّر أي واحد ----
BG          = "#faf7f1"   # خلفية الشاشة (كريمي)
TILE        = "#ebe3d2"   # الخانة العادية
TILE_EDGE   = "#d6cbb3"
TILE_HOVER  = "#e2d8c3"   # لما الماوس يعدي على خانة
INK         = "#2a2118"   # لون الكلام
MUTED       = "#8a7f6f"
GREEN       = "#6cbb8a"   # الكلمة اللي اتلقت
GREEN_DARK  = "#4f9b6d"
ORANGE      = "#f0a35e"   # السحب
BTN         = "#d96a1f"   # زرار New Game
BTN_HOVER   = "#c25a14"
HINT_FILL   = "#fbe3c4"   # الحرف الأول بتاع التلميح
HINT_EDGE   = "#e8944a"
MISS_FILL   = "#f9d6d6"   # الكلمات اللي متلقتش بعد ما الوقت يخلص
MISS_EDGE   = "#d64545"
PANEL       = "#e6e9ef"   # بانل الكلمات
PANEL_EDGE  = "#c8cfdb"
TRACK       = "#e8e0d4"
NAVY        = "#1f2937"
RED         = "#d64545"
WHITE       = "#ffffff"

# ألوان مختلفة لكل كلمة تتلقي
WORD_COLORS = [
    "#57b880",  #green
    "#4c9be8",  #blue
    "#e06c75",  #red
    "#9b72cf",  #purple
    "#3aa89e",  #teal
    "#d97b38",  #orange
    "#d4609c",  #pink
    "#6d8ce8",  #sky blue
    "#82ad49",  #lime
    "#c98a2c",  #yellow
]

# ---- الفونت ----
FONT = "Segoe UI"         # بدائل: "Bahnschrift", "Trebuchet MS"

# ---- المقاسات ----
T, G, PAD = 56, 6, 4      # حجم الخانة، المسافة بين الخانات، الهامش
BOARD_W = N * T + (N - 1) * G + 2 * PAD
CONTENT_W = 620           # عرض بانل الكلمات
COLS = 5                  # عدد الكلمات في الصف

root = tk.Tk()
root.title("AI Word Search")
root.configure(bg=BG)
root.resizable(False, False)

F_CELL  = tkfont.Font(family=FONT, size=18, weight="bold")
F_WORD  = tkfont.Font(family=FONT, size=13)
F_DONE  = tkfont.Font(family=FONT, size=13, overstrike=True)
F_TITLE = tkfont.Font(family=FONT, size=10, weight="bold")
F_WIN   = tkfont.Font(family=FONT, size=40, weight="bold")

state = dict(words=[], grid="", found=set(), found_lines=[], done={}, first=None,
             preview=[], left=0, score=0, running=False, job=None, hover=None,
             positions={}, hint=None, reveal=set(), bjob=None)


# Draws a rounded rectangle on a canvas.
def rrect(cv, x1, y1, x2, y2, r, **kw):
    """مستطيل بحواف مدورة على Canvas."""
    pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
           x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
    return cv.create_polygon(pts, smooth=True, **kw)


# Creates a custom rounded clickable button.
def rbutton(parent, text, command, bg, hover_bg, fg, w=130, h=40, r=10):
    """زرار بحواف مدورة."""
    cv = tk.Canvas(parent, width=w, height=h, bg=BG, highlightthickness=0, cursor="hand2")
    shape = rrect(cv, 1, 1, w - 1, h - 1, r, fill=bg, outline=bg)
    cv.create_text(w / 2, h / 2, text=text, font=(FONT, 11, "bold"), fill=fg)
    cv.bind("<Enter>", lambda e: cv.itemconfig(shape, fill=hover_bg, outline=hover_bg))
    cv.bind("<Leave>", lambda e: cv.itemconfig(shape, fill=bg, outline=bg))
    cv.bind("<Button-1>", lambda e: command())
    return cv


# ---- الهيدر ----
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=24, pady=(18, 6))
tk.Label(header, text="AI WORD SEARCH", font=(FONT, 20, "bold"), bg=BG, fg=INK).pack(side="left")
tk.Label(header, text="●", font=(FONT, 10), bg=BG, fg=INK).pack(side="left", padx=8)
rbutton(header, "NEW GAME", lambda: new_game(), BTN, BTN_HOVER, WHITE).pack(side="right")
hint_btn = tk.Label(header, text="HINT (-%d pts)" % HINT_COST, font=(FONT, 11, "bold"), bg=BG, fg=MUTED,
                    cursor="hand2")
hint_btn.pack(side="right", padx=(0, 18))
hint_btn.bind("<Button-1>", lambda e: hint())

# ---- الإحصائيات ----
stats = tk.Frame(root, bg=BG)
stats.pack(fill="x", padx=24)
timer_lbl = tk.Label(stats, font=(FONT, 16, "bold"), bg=BG, fg=INK)
timer_lbl.pack(side="left")
score_lbl = tk.Label(stats, font=(FONT, 16, "bold"), bg=BG, fg=INK)
score_lbl.pack(side="right")
wordlabel = tk.Label(stats, font=(FONT, 12), bg=BG, fg=MUTED)
wordlabel.pack(expand=True)

bar = tk.Canvas(root, height=5, bg=TRACK, highlightthickness=0)
bar.pack(fill="x", padx=24, pady=(8, 0))

msg = tk.Label(root, font=(FONT, 10, "bold"), bg=BG, fg=INK)
msg.pack(pady=(10, 0))

# ---- اللوحة ----
board = tk.Canvas(root, width=BOARD_W, height=BOARD_W, bg=BG, highlightthickness=0)
board.pack(pady=10)


# Calculates the height needed for the word panel.
def panel_h(n):
    return 46 + ((n + COLS - 1) // COLS) * 30 + 10


# ---- بانل الكلمات (تحت اللوحة) ----
words_cv = tk.Canvas(root, width=CONTENT_W, height=panel_h(NUM_WORDS), bg=BG,
                     highlightthickness=0)
words_cv.pack(padx=24, pady=(0, 8))

note = tk.Label(root, font=(FONT, 10), bg=BG, fg=RED)
note.pack()
statlabel = tk.Label(root, font=(FONT, 9), bg=BG, fg="#5c5245")
statlabel.pack(pady=(0, 14))


# Gets the center screen coordinates of a cell.
def center(r, c):
    return PAD + c * (T + G) + T / 2, PAD + r * (T + G) + T / 2


# Draws a colored highlight bar over a word.
def draw_pill(cells, color):
    """شريط مدور بيغطي الكلمة من أول خانة لآخر خانة (في أي اتجاه)."""
    (r0, c0), (r1, c1) = cells[0], cells[-1]
    x0, y0 = center(r0, c0)
    x1, y1 = center(r1, c1)
    board.create_line(x0, y0, x1, y1, width=T - 4, fill=color, capstyle="round", tags="b")


# Redraws all tiles, highlights, and letters on board.
def draw_board(hint_cell):
    board.delete("b")
    for r in range(N):
        for c in range(N):
            pos = (r, c)
            x, y = PAD + c * (T + G), PAD + r * (T + G)
            fill, edge = TILE, TILE_EDGE
            if state["hover"] == pos and state["running"]: fill = TILE_HOVER
            if pos in state["reveal"]: fill, edge = MISS_FILL, MISS_EDGE   # NEW: missed words after time's up
            if pos == hint_cell: fill, edge = HINT_FILL, HINT_EDGE         # NEW: hint
            if state["first"] == pos: fill, edge = ORANGE, ORANGE
            rrect(board, x, y, x + T, y + T, 10, fill=fill, outline=edge, tags="b")
    for cells, color in state["found_lines"]:
        draw_pill(cells, color)
    if len(state["preview"]) > 1:                      # live drag highlight
        draw_pill(state["preview"], ORANGE)
    for k, ch in enumerate(state["grid"]):
        pos = (k // N, k % N)
        covered = pos in state["found"] or pos in state["preview"] or state["first"] == pos
        x, y = center(*pos)
        board.create_text(x, y, text=ch, font=F_CELL, fill=WHITE if covered else INK, tags="b")
    board.tag_raise("win")                             # شاشة الفوز دايما فوق


# Displays the target words list with their statuses.
def draw_words():
    n = len(state["words"]) or NUM_WORDS
    W, H = CONTENT_W, panel_h(n)
    words_cv.config(height=H)
    words_cv.delete("all")
    rrect(words_cv, 2, 2, W - 2, H - 2, 14, fill=PANEL, outline=PANEL_EDGE)
    words_cv.create_text(W / 2, 24, text="WORDS", font=F_TITLE, fill=MUTED)
    ptxt = "".join(state["grid"][y * N + x] for y, x in state["preview"])
    for i, w in enumerate(sorted(state["words"])):
        x, y = W * ((i % COLS) + 0.5) / COLS, 56 + (i // COLS) * 30
        if w in state["done"]:
            fnt, col = F_DONE, state["done"][w]
        elif ptxt and ptxt in (w, w[::-1]):            # الكلمة اللي بتسحبها دلوقتي
            fnt, col = F_WORD, HINT_EDGE
        else:
            fnt, col = F_WORD, INK
        words_cv.create_text(x, y, text=w, font=fnt, fill=col)


# Updates the board, word list, timer, and score.
def refresh():
    # NEW: the hint is only shown while its word is still not found
    hint_cell = None
    if state["hint"] and state["hint"][0] not in state["done"]:
        hint_cell = state["hint"][1]
    draw_board(hint_cell)
    draw_words()
    low = state["left"] <= 30
    can_hint = state["running"] and state["score"] >= HINT_COST
    wordlabel.config(text="%d / %d found" % (len(state["done"]), len(state["words"])))
    timer_lbl.config(text="%d:%02d" % divmod(state["left"], 60), fg=RED if low else INK)
    score_lbl.config(text="%d pts" % state["score"])
    hint_btn.config(text="HINT (-%d pts)" % HINT_COST,
                    fg=MUTED if can_hint else "#c9c0b0")
    bar.delete("all")                                  # الوقت اللي عدّى بيكبر من اليمين
    w = bar.winfo_width()
    used = (TIME_LIMIT - state["left"]) / TIME_LIMIT
    bar.create_rectangle(w * (1 - used), 0, w, 5, fill=RED if low else NAVY, width=0)


# Resets everything and starts a fresh game.
def new_game():
    if state["job"]:
        root.after_cancel(state["job"])
    if state["bjob"]:
        root.after_cancel(state["bjob"])
        state["bjob"] = None
    board.delete("win")
    note.config(text="")
    t = time.time()
    words, grid, style, tries, undone, positions = make_puzzle()
    state.update(words=words, grid=grid, found=set(), found_lines=[], done={},
                 first=None, preview=[], left=TIME_LIMIT, running=True,
                 positions=positions, hint=None, reveal=set(), score=0)
    msg.config(text="AI used '%s': %d attempts, %d backtracks, %.2fs"
               % (style, tries, undone, time.time() - t), fg=INK)
    statlabel.config(text="AI's avg attempts (lower = better):  " + "   ".join(
        "%s %.0f" % (s, sum(v) / len(v)) for s, v in history.items() if v))
    refresh()
    tick()


# Counts down the timer and ends game at zero.
def tick():
    if not state["running"]:
        return
    if state["left"] <= 0:
        state["running"] = False
        # NEW: reveal every word the player didn't find
        for w in state["words"]:
            if w not in state["done"]:
                state["reveal"].update(state["positions"][w])
        state["hint"] = None
        msg.config(text="TIME'S UP - YOU LOSE", fg=RED)
        note.config(text="The words you missed are shown in red")
        refresh()
        return
    state["left"] -= 1
    refresh()
    state["job"] = root.after(1000, tick)


# Highlights the first letter of an unfound word.
def hint():
    # NEW: highlights the first letter of a random unfound word
    if not state["running"]:
        return
    if state["score"] < HINT_COST:
        note.config(text="Not enough points for a hint (need %d pts)" % HINT_COST)
        root.after(1500, lambda: note.config(text=""))
        return
    left = [w for w in state["words"] if w not in state["done"]]
    if not left:
        return
    w = random.choice(left)
    state["hint"] = (w, state["positions"][w][0])
    state["score"] -= HINT_COST
    note.config(text="Hint: a %d-letter word starts at the highlighted cell" % len(w))
    refresh()


# Gets the grid row and column under the mouse.
def cell_at(e):
    """Row, col of the cell under the mouse (or None if outside the board)."""
    c, r = (e.x - PAD) // (T + G), (e.y - PAD) // (T + G)
    return (int(r), int(c)) if 0 <= r < N and 0 <= c < N else None


# Returns all cells along a straight drag line.
def line(start, end):
    """Cells on the straight line from start to end ([] if it isn't straight)."""
    (r0, c0), (r, c) = start, end
    dy, dx = r - r0, c - c0
    if dy != 0 and dx != 0 and abs(dy) != abs(dx):
        return []
    n = max(abs(dy), abs(dx)) + 1
    sy, sx = (dy > 0) - (dy < 0), (dx > 0) - (dx < 0)
    return [(r0 + sy * i, c0 + sx * i) for i in range(n)]


# Starts word selection when the mouse is pressed.
def press(r, c):
    if state["running"]:
        state["first"] = (r, c)          # drag starts here
        refresh()


# Updates the live highlight path while dragging.
def motion(e):
    if state["running"] and state["first"] is not None:
        end = cell_at(e)
        state["preview"] = line(state["first"], end) if end else []
        refresh()                        # highlights the path while you drag


# Checks the selected line when mouse is released.
def release(e):
    if state["running"] and state["first"] is not None:
        end = cell_at(e)
        if end and end != state["first"]:                 # a real drag, not a single click
            before = len(state["done"])
            cells = line(state["first"], end)
            check_line(cells)
            if len(state["done"]) == before:              # nothing new was found
                text = "".join(state["grid"][y * N + x] for y, x in cells)
                if cells and any(text in (w, w[::-1]) for w in state["done"]):
                    note.config(text="Already found")     # كلمة اتلقت قبل كده: من غير خصم
                else:
                    note.config(text="Not one of the hidden words")
                root.after(1500, lambda: note.config(text=""))
    state["first"], state["preview"] = None, []
    refresh()


# Checks if selected letters match a hidden word.
def check_line(cells):
    text = "".join(state["grid"][y * N + x] for y, x in cells)
    for w in state["words"]:
        if w not in state["done"] and text in (w, w[::-1]):
            color = WORD_COLORS[len(state["done"]) % len(WORD_COLORS)]
            state["done"][w] = color
            state["found"].update(cells)
            state["found_lines"].append((cells, color))
            state["score"] += 10 * len(w)
    if len(state["done"]) == len(state["words"]):
        state["running"] = False
        state["score"] += state["left"]            # time bonus
        msg.config(text="YOU WIN!", fg=GREEN_DARK)
        show_win()


BALLOON_COLORS = ["#f0a35e", "#6cbb8a", "#e86a6a", "#6ab0f0", "#f2d45c", "#b48be8"]
balloons = []


# Shows the win banner and spawns floating balloons.
def show_win():
    """كلمة YOU WIN كبيرة في نص اللوحة + بلالين بتطلع لفوق."""
    board.delete("win")
    balloons.clear()
    for i in range(14):
        x = random.randint(30, BOARD_W - 30)
        y = random.randint(BOARD_W + 10, BOARD_W + 260)
        tag, col = "bal%d" % i, random.choice(BALLOON_COLORS)
        board.create_line(x, y + 22, x, y + 75, fill=MUTED, tags=("win", tag))           # الخيط
        board.create_polygon(x - 4, y + 28, x + 4, y + 28, x, y + 21, fill=col,
                             outline=col, tags=("win", tag))                              # العقدة
        board.create_oval(x - 17, y - 22, x + 17, y + 22, fill=col, outline=col,
                          tags=("win", tag))                                              # البالونة
        board.create_oval(x - 10, y - 15, x - 5, y - 7, fill=WHITE, outline=WHITE,
                          tags=("win", tag))                                              # لمعة
        balloons.append([tag, random.uniform(1.5, 3.5), random.uniform(0, 6.28), y])
    mid = BOARD_W / 2
    rrect(board, 50, mid - 85, BOARD_W - 50, mid + 85, 24, fill=BG, outline=GREEN,
          width=3, tags="win")
    board.create_text(mid, mid - 25, text="YOU WIN!", font=F_WIN, fill=GREEN_DARK, tags="win")
    board.create_text(mid, mid + 45, text="Score: %d" % state["score"],
                      font=(FONT, 16, "bold"), fill=INK, tags="win")
    animate_balloons()


# Moves the celebration balloons upward across the screen.
def animate_balloons():
    for b in balloons:
        b[2] += 0.08
        board.move(b[0], math.sin(b[2]) * 1.2, -b[1])
        b[3] -= b[1]
        if b[3] < -85:                                 # طلعت برا: ترجع من تحت
            board.move(b[0], 0, BOARD_W + 200)
            b[3] += BOARD_W + 200
    state["bjob"] = root.after(30, animate_balloons)


# Handles mouse click events on the game board.
def on_press(e):
    cell = cell_at(e)
    if cell:
        press(*cell)


# Highlights the tile currently under the mouse cursor.
def on_hover(e):
    cell = cell_at(e)
    if cell != state["hover"]:
        state["hover"] = cell
        refresh()


# Clears tile hover highlight when mouse leaves board.
def on_leave(e):
    state["hover"] = None
    refresh()


board.bind("<ButtonPress-1>", on_press)
board.bind("<B1-Motion>", motion)
board.bind("<ButtonRelease-1>", release)
board.bind("<Motion>", on_hover)
board.bind("<Leave>", on_leave)

root.update_idletasks()
new_game()
root.mainloop()
