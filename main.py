import tkinter as tk
from game import WordSearchGame
from gui import WordSearchGUI
from logic import PuzzleGenerator


def main():
    root = tk.Tk()
    generator = PuzzleGenerator()
    game = WordSearchGame(generator=generator)
    app = WordSearchGUI(root, game)
    root.update_idletasks()
    app.new_game()
    root.mainloop()


if __name__ == "__main__":
    main()
