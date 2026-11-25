# ---------------- GAME / GUI PART (CREAM EDITION) ----------------
import tkinter as tk
import tkinter.font as tkfont
import math
import random

from config import (
    BALLOON_COLORS, BG, BOARD_W, BTN, BTN_HOVER, COLS, CONTENT_W, FONT, G,
    GREEN, GREEN_DARK, HINT_COST, HINT_EDGE, HINT_FILL, INK, MISS_EDGE,
    MISS_FILL, MUTED, N, NAVY, NUM_WORDS, ORANGE, PAD, PANEL, PANEL_EDGE,
    RED, T, TILE, TILE_EDGE, TILE_HOVER, TIME_LIMIT, TRACK, WHITE,
)


class CanvasHelpers:
    # Draws a rounded rectangle on a canvas.
    @staticmethod
    def rrect(cv, x1, y1, x2, y2, r, **kw):
        """مستطيل بحواف مدورة على Canvas."""
        pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
               x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return cv.create_polygon(pts, smooth=True, **kw)

    # Creates a custom rounded clickable button.
    @classmethod
    def rbutton(cls, parent, text, command, bg, hover_bg, fg, w=130, h=40, r=10):
        """زرار بحواف مدورة."""
        cv = tk.Canvas(parent, width=w, height=h, bg=BG, highlightthickness=0, cursor="hand2")
        shape = cls.rrect(cv, 1, 1, w - 1, h - 1, r, fill=bg, outline=bg)
        cv.create_text(w / 2, h / 2, text=text, font=(FONT, 11, "bold"), fill=fg)
        cv.bind("<Enter>", lambda e: cv.itemconfig(shape, fill=hover_bg, outline=hover_bg))
        cv.bind("<Leave>", lambda e: cv.itemconfig(shape, fill=bg, outline=bg))
        cv.bind("<Button-1>", lambda e: command())
        return cv


class WordSearchGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.job = None
        self.bjob = None
        self.note_job = None
        self.balloons = []

        self.root.title("AI Word Search")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.F_CELL  = tkfont.Font(family=FONT, size=18, weight="bold")
        self.F_WORD  = tkfont.Font(family=FONT, size=13)
        self.F_DONE  = tkfont.Font(family=FONT, size=13, overstrike=True)
        self.F_TITLE = tkfont.Font(family=FONT, size=10, weight="bold")
        self.F_WIN   = tkfont.Font(family=FONT, size=40, weight="bold")

        self._build_widgets()
        self._bind_events()

    # Calculates the height needed for the word panel.
    @staticmethod
    def panel_h(n):
        return 46 + ((n + COLS - 1) // COLS) * 30 + 10

    # Gets the center screen coordinates of a cell.
    @staticmethod
    def center(r, c):
        return PAD + c * (T + G) + T / 2, PAD + r * (T + G) + T / 2

    def _build_widgets(self):
        # ---- الهيدر ----
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=24, pady=(18, 6))
        tk.Label(header, text="AI WORD SEARCH", font=(FONT, 20, "bold"), bg=BG, fg=INK).pack(side="left")
        tk.Label(header, text="●", font=(FONT, 10), bg=BG, fg=INK).pack(side="left", padx=8)
        CanvasHelpers.rbutton(header, "NEW GAME", self.new_game, BTN, BTN_HOVER, WHITE).pack(side="right")
        self.hint_btn = tk.Label(header, text="HINT (-%d pts)" % HINT_COST, font=(FONT, 11, "bold"), bg=BG, fg=MUTED,
                                 cursor="hand2")
        self.hint_btn.pack(side="right", padx=(0, 18))
        self.hint_btn.bind("<Button-1>", lambda e: self.hint())

        # ---- الإحصائيات ----
        stats = tk.Frame(self.root, bg=BG)
        stats.pack(fill="x", padx=24)
        self.timer_lbl = tk.Label(stats, font=(FONT, 16, "bold"), bg=BG, fg=INK)
        self.timer_lbl.pack(side="left")
        self.score_lbl = tk.Label(stats, font=(FONT, 16, "bold"), bg=BG, fg=INK)
        self.score_lbl.pack(side="right")
        self.wordlabel = tk.Label(stats, font=(FONT, 12), bg=BG, fg=MUTED)
        self.wordlabel.pack(expand=True)

        self.bar = tk.Canvas(self.root, height=5, bg=TRACK, highlightthickness=0)
        self.bar.pack(fill="x", padx=24, pady=(8, 0))

        self.msg = tk.Label(self.root, font=(FONT, 10, "bold"), bg=BG, fg=INK)
        self.msg.pack(pady=(10, 0))

        # ---- اللوحة ----
        self.board = tk.Canvas(self.root, width=BOARD_W, height=BOARD_W, bg=BG, highlightthickness=0)
        self.board.pack(pady=10)

        # ---- بانل الكلمات (تحت اللوحة) ----
        self.words_cv = tk.Canvas(self.root, width=CONTENT_W, height=self.panel_h(NUM_WORDS), bg=BG,
                                  highlightthickness=0)
        self.words_cv.pack(padx=24, pady=(0, 8))

        self.note = tk.Label(self.root, font=(FONT, 10), bg=BG, fg=RED)
        self.note.pack()
        self.statlabel = tk.Label(self.root, font=(FONT, 9), bg=BG, fg="#5c5245")
        self.statlabel.pack(pady=(0, 8))

        # ---- جدول الـ Score Tracker ----
        tk.Label(self.root, text="SCORE TRACKER", font=(FONT, 10, "bold"), bg=BG, fg=MUTED).pack()
        tf = tk.Frame(self.root, bg=BG)
        tf.pack(padx=24, pady=(4, 0))
        self.tracklist = tk.Listbox(tf, width=60, height=6, font=("Courier", 10), bg=PANEL, fg=INK,
                                    highlightthickness=0, bd=0, activestyle="none",
                                    selectbackground=PANEL, selectforeground=INK)
        tsb = tk.Scrollbar(tf, command=self.tracklist.yview)
        self.tracklist.config(yscrollcommand=tsb.set)
        self.tracklist.pack(side="left")
        tsb.pack(side="left", fill="y")
        self.tracksummary = tk.Label(self.root, font=(FONT, 10), bg=BG, fg=NAVY)
        self.tracksummary.pack(pady=(4, 14))
        self._shown_runs = -1

    def _bind_events(self):
        self.board.bind("<ButtonPress-1>", self.on_press)
        self.board.bind("<B1-Motion>", self.motion)
        self.board.bind("<ButtonRelease-1>", self.release)
        self.board.bind("<Motion>", self.on_hover)
        self.board.bind("<Leave>", self.on_leave)

    def _clear_note_later(self, ms=1500):
        if self.note_job:
            self.root.after_cancel(self.note_job)
        self.note_job = self.root.after(ms, self._clear_note)

    def _clear_note(self):
        self.note_job = None
        self.game.note_text = ""
        self.note.config(text="")

    # Gets the grid row and column under the mouse.
    def cell_at(self, e):
        """Row, col of the cell under the mouse (or None if outside the board)."""
        c, r = (e.x - PAD) // (T + G), (e.y - PAD) // (T + G)
        return (int(r), int(c)) if 0 <= r < N and 0 <= c < N else None

    # Draws a colored highlight bar over a word.
    def draw_pill(self, cells, color):
        """شريط مدور بيغطي الكلمة من أول خانة لآخر خانة (في أي اتجاه)."""
        (r0, c0), (r1, c1) = cells[0], cells[-1]
        x0, y0 = self.center(r0, c0)
        x1, y1 = self.center(r1, c1)
        self.board.create_line(x0, y0, x1, y1, width=T - 4, fill=color, capstyle="round", tags="b")

    # Redraws all tiles, highlights, and letters on board.
    def draw_board(self, hint_cell):
        self.board.delete("b")
        g = self.game
        for r in range(N):
            for c in range(N):
                pos = (r, c)
                x, y = PAD + c * (T + G), PAD + r * (T + G)
                fill, edge = TILE, TILE_EDGE
                if g.hover == pos and g.running: fill = TILE_HOVER
                if pos in g.reveal: fill, edge = MISS_FILL, MISS_EDGE   # NEW: missed words after time's up
                if pos == hint_cell: fill, edge = HINT_FILL, HINT_EDGE         # NEW: hint
                if g.first == pos: fill, edge = ORANGE, ORANGE
                CanvasHelpers.rrect(self.board, x, y, x + T, y + T, 10, fill=fill, outline=edge, tags="b")
        for cells, color in g.found_lines:
            self.draw_pill(cells, color)
        if len(g.preview) > 1:                      # live drag highlight
            self.draw_pill(g.preview, ORANGE)
        for k, ch in enumerate(g.grid):
            pos = (k // N, k % N)
            covered = pos in g.found or pos in g.preview or g.first == pos
            x, y = self.center(*pos)
            self.board.create_text(x, y, text=ch, font=self.F_CELL, fill=WHITE if covered else INK, tags="b")
        self.board.tag_raise("win")                             # شاشة الفوز دايما فوق

    # Displays the target words list with their statuses.
    def draw_words(self):
        g = self.game
        n = len(g.words) or NUM_WORDS
        W, H = CONTENT_W, self.panel_h(n)
        self.words_cv.config(height=H)
        self.words_cv.delete("all")
        CanvasHelpers.rrect(self.words_cv, 2, 2, W - 2, H - 2, 14, fill=PANEL, outline=PANEL_EDGE)
        self.words_cv.create_text(W / 2, 24, text="WORDS", font=self.F_TITLE, fill=MUTED)
        ptxt = g.cell_text(g.preview)
        for i, w in enumerate(sorted(g.words)):
            x, y = W * ((i % COLS) + 0.5) / COLS, 56 + (i // COLS) * 30
            if w in g.done:
                fnt, col = self.F_DONE, g.done[w]
            elif ptxt and ptxt in (w, w[::-1]):            # الكلمة اللي بتسحبها دلوقتي
                fnt, col = self.F_WORD, HINT_EDGE
            else:
                fnt, col = self.F_WORD, INK
            self.words_cv.create_text(x, y, text=w, font=fnt, fill=col)

    # Updates the board, word list, timer, and score.
    def refresh(self):
        g = self.game
        self.draw_board(g.active_hint_cell())
        self.draw_words()
        low = g.left <= 30
        can_hint = g.can_afford_hint()
        self.wordlabel.config(text="%d / %d found" % (len(g.done), len(g.words)))
        self.timer_lbl.config(text="%d:%02d" % divmod(g.left, 60), fg=RED if low else INK)
        self.score_lbl.config(text="%d pts" % g.score)
        self.hint_btn.config(text="HINT (-%d pts)" % HINT_COST,
                             fg=MUTED if can_hint else "#c9c0b0")
        self.note.config(text=g.note_text)
        kind_colors = {"win": GREEN_DARK, "lose": RED, "info": INK}
        self.msg.config(text=g.status_text, fg=kind_colors.get(g.status_kind, INK))
        self.statlabel.config(text=g.stats_text)
        self.refresh_tracker()
        self.bar.delete("all")                                  # الوقت اللي عدّى بيكبر من اليمين
        w = self.bar.winfo_width()
        used = (TIME_LIMIT - g.left) / TIME_LIMIT
        self.bar.create_rectangle(w * (1 - used), 0, w, 5, fill=RED if low else NAVY, width=0)

    # Redraws the score tracker table, only when a new run was saved.
    def refresh_tracker(self):
        runs = self.game.runs
        if len(runs) == self._shown_runs:
            return
        self._shown_runs = len(runs)
        self.tracklist.delete(0, tk.END)
        self.tracklist.insert(tk.END, "%-4s %-7s %-7s %-7s %s" % ("Run", "Result", "Found", "Score", "Style"))
        for n, run in enumerate(runs, 1):
            found = "%d/%d" % (run["found"], run["total"])
            self.tracklist.insert(tk.END, "%-4d %-7s %-7s %-7d %s" % (n, run["result"], found, run["score"], run["style"]))
        self.tracklist.yview_moveto(1)
        self.tracksummary.config(text=self.game.tracker_summary())

    # Resets everything and starts a fresh game.
    def new_game(self):
        if self.job:
            self.root.after_cancel(self.job)
        if self.bjob:
            self.root.after_cancel(self.bjob)
            self.bjob = None
        if self.note_job:
            self.root.after_cancel(self.note_job)
            self.note_job = None
        self.board.delete("win")
        self.game.start_new()
        self.refresh()
        self.tick()

    # Counts down the timer and ends game at zero.
    def tick(self):
        state = self.game.tick()
        self.refresh()
        if state == "running":
            self.job = self.root.after(1000, self.tick)

    # Highlights the first letter of an unfound word.
    def hint(self):
        granted = self.game.request_hint()
        self.refresh()
        if not granted and self.game.note_text:
            self._clear_note_later()

    # Starts word selection when the mouse is pressed.
    def press(self, r, c):
        self.game.begin_drag((r, c))
        self.refresh()

    # Updates the live highlight path while dragging.
    def motion(self, e):
        if self.game.running and self.game.first is not None:
            self.game.update_drag(self.cell_at(e))
            self.refresh()                        # highlights the path while you drag

    # Checks the selected line when mouse is released.
    def release(self, e):
        if self.game.running and self.game.first is not None:
            outcome = self.game.finish_drag(self.cell_at(e))
            self.refresh()
            if outcome == "win":
                self.show_win()
            elif self.game.note_text:
                self._clear_note_later()

    # Shows the win banner and spawns floating balloons.
    def show_win(self):
        """كلمة YOU WIN كبيرة في نص اللوحة + بلالين بتطلع لفوق."""
        self.board.delete("win")
        self.balloons.clear()
        for i in range(14):
            x = random.randint(30, BOARD_W - 30)
            y = random.randint(BOARD_W + 10, BOARD_W + 260)
            tag, col = "bal%d" % i, random.choice(BALLOON_COLORS)
            self.board.create_line(x, y + 22, x, y + 75, fill=MUTED, tags=("win", tag))           # الخيط
            self.board.create_polygon(x - 4, y + 28, x + 4, y + 28, x, y + 21, fill=col,
                                      outline=col, tags=("win", tag))                              # العقدة
            self.board.create_oval(x - 17, y - 22, x + 17, y + 22, fill=col, outline=col,
                                   tags=("win", tag))                                              # البالونة
            self.board.create_oval(x - 10, y - 15, x - 5, y - 7, fill=WHITE, outline=WHITE,
                                   tags=("win", tag))                                              # لمعة
            self.balloons.append([tag, random.uniform(1.5, 3.5), random.uniform(0, 6.28), y])
        mid = BOARD_W / 2
        CanvasHelpers.rrect(self.board, 50, mid - 85, BOARD_W - 50, mid + 85, 24, fill=BG, outline=GREEN,
                            width=3, tags="win")
        self.board.create_text(mid, mid - 25, text="YOU WIN!", font=self.F_WIN, fill=GREEN_DARK, tags="win")
        self.board.create_text(mid, mid + 45, text="Score: %d" % self.game.score,
                               font=(FONT, 16, "bold"), fill=INK, tags="win")
        self.animate_balloons()

    # Moves the celebration balloons upward across the screen.
    def animate_balloons(self):
        for b in self.balloons:
            b[2] += 0.08
            self.board.move(b[0], math.sin(b[2]) * 1.2, -b[1])
            b[3] -= b[1]
            if b[3] < -85:                                 # طلعت برا: ترجع من تحت
                self.board.move(b[0], 0, BOARD_W + 200)
                b[3] += BOARD_W + 200
        self.bjob = self.root.after(30, self.animate_balloons)

    # Handles mouse click events on the game board.
    def on_press(self, e):
        cell = self.cell_at(e)
        if cell:
            self.press(*cell)

    # Highlights the tile currently under the mouse cursor.
    def on_hover(self, e):
        cell = self.cell_at(e)
        if cell != self.game.hover:
            self.game.hover = cell
            self.refresh()

    # Clears tile hover highlight when mouse leaves board.
    def on_leave(self, e):
        self.game.hover = None
        self.refresh()
