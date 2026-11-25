import random, time
from config import HINT_COST, N, TIME_LIMIT, WORD_COLORS
from logic import PuzzleGenerator


class WordSearchGame:
    def __init__(self, generator=None, size=N, time_limit=TIME_LIMIT, hint_cost=HINT_COST):
        self.generator = generator if generator is not None else PuzzleGenerator(size=size)
        self.size = size
        self.time_limit = time_limit
        self.hint_cost = hint_cost

        self.words = []
        self.grid = ""
        self.found = set()
        self.found_lines = []
        self.done = {}
        self.first = None
        self.preview = []
        self.left = 0
        self.score = 0
        self.running = False
        self.hover = None
        self.positions = {}
        self.hint = None
        self.reveal = set()
        self.runs = []                 # finished runs for the score tracker
        self.recorded = True           # True = no live run waiting to be saved
        self.style = ""

        self.status_text = ""
        self.status_kind = "info"
        self.note_text = ""
        self.stats_text = ""

    # Returns all cells along a straight drag line.
    @staticmethod
    def line_cells(start, end):
        """Cells on the straight line from start to end ([] if it isn't straight)."""
        (r0, c0), (r, c) = start, end
        dy, dx = r - r0, c - c0
        if dy != 0 and dx != 0 and abs(dy) != abs(dx):
            return []
        n = max(abs(dy), abs(dx)) + 1
        sy, sx = (dy > 0) - (dy < 0), (dx > 0) - (dx < 0)
        return [(r0 + sy * i, c0 + sx * i) for i in range(n)]

    def cell_text(self, cells):
        return "".join(self.grid[y * self.size + x] for y, x in cells)

    def active_hint_cell(self):
        # NEW: the hint is only shown while its word is still not found
        if self.hint and self.hint[0] not in self.done:
            return self.hint[1]
        return None

    def can_afford_hint(self):
        return self.running and self.score >= self.hint_cost

    # Saves the current run once (QUIT, LOSE or WIN) so the tracker can show it.
    def _record(self, result):
        if self.recorded:
            return
        self.recorded = True
        self.runs.append(dict(result=result, found=len(self.done), total=len(self.words),
                              score=self.score, style=self.style))

    # Text shown under the score tracker table.
    def tracker_summary(self):
        if not self.runs:
            return "No runs yet"
        scores = [r["score"] for r in self.runs]
        wins = sum(r["result"] == "WIN" for r in self.runs)
        return "Runs: %d   Wins: %d   Best: %d   Average: %.1f" % (
            len(self.runs), wins, max(scores), sum(scores) / len(scores))

    # Resets everything and starts a fresh game.
    def start_new(self):
        if self.running:
            self._record("QUIT")                 # new game pressed mid-game
        t = time.time()
        words, grid, style, tries, undone, positions = self.generator.generate()
        self.words = words
        self.grid = grid
        self.found = set()
        self.found_lines = []
        self.done = {}
        self.first = None
        self.preview = []
        self.left = self.time_limit
        self.running = True
        self.positions = positions
        self.hint = None
        self.reveal = set()
        self.score = 0
        self.note_text = ""
        self.status_kind = "info"
        self.status_text = (
            "AI used '%s': %d attempts, %d backtracks, %.2fs"
            % (style, tries, undone, time.time() - t)
        )
        self.stats_text = self.generator.format_stats()
        self.style = style
        self.recorded = False

    # Counts down the timer and ends game at zero.
    def tick(self):
        if not self.running:
            return "stopped"
        if self.left <= 0:
            self.running = False
            # NEW: reveal every word the player didn't find
            for w in self.words:
                if w not in self.done:
                    self.reveal.update(self.positions[w])
            self.hint = None
            self.status_kind = "lose"
            self.status_text = "TIME'S UP - YOU LOSE"
            self.note_text = "The words you missed are shown in red"
            self._record("LOSE")
            return "lose"
        self.left -= 1
        return "running"

    # Highlights the first letter of an unfound word.
    def request_hint(self):
        # NEW: highlights the first letter of a random unfound word
        if not self.running:
            return False
        if self.score < self.hint_cost:
            self.note_text = "Not enough points for a hint (need %d pts)" % self.hint_cost
            return False
        left = [w for w in self.words if w not in self.done]
        if not left:
            return False
        w = random.choice(left)
        self.hint = (w, self.positions[w][0])
        self.score -= self.hint_cost
        self.note_text = "Hint: a %d-letter word starts at the highlighted cell" % len(w)
        return True

    # Starts word selection when the mouse is pressed.
    def begin_drag(self, pos):
        if self.running:
            self.first = pos          # drag starts here

    # Updates the live highlight path while dragging.
    def update_drag(self, end_pos):
        if self.running and self.first is not None:
            self.preview = self.line_cells(self.first, end_pos) if end_pos else []

    # Checks the selected line when mouse is released.
    def finish_drag(self, end_pos):
        outcome = None
        if self.running and self.first is not None:
            if end_pos and end_pos != self.first:                 # a real drag, not a single click
                before = len(self.done)
                cells = self.line_cells(self.first, end_pos)
                outcome = self.check_line(cells)
                if len(self.done) == before:              # nothing new was found
                    text = self.cell_text(cells)
                    if cells and any(text in (w, w[::-1]) for w in self.done):
                        self.note_text = "Already found"     # كلمة اتلقت قبل كده: من غير خصم
                    else:
                        self.note_text = "Not one of the hidden words"
        self.first, self.preview = None, []
        return outcome

    # Checks if selected letters match a hidden word.
    def check_line(self, cells):
        text = self.cell_text(cells)
        for w in self.words:
            if w not in self.done and text in (w, w[::-1]):
                color = WORD_COLORS[len(self.done) % len(WORD_COLORS)]
                self.done[w] = color
                self.found.update(cells)
                self.found_lines.append((cells, color))
                self.score += 10 * len(w)
        if len(self.done) == len(self.words):
            self.running = False
            self.score += self.left            # time bonus
            self._record("WIN")
            self.status_kind = "win"
            self.status_text = "YOU WIN!"
            return "win"
        return None
