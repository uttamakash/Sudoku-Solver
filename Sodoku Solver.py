import tkinter as tk
from tkinter import messagebox
import random
import copy
import time
import winsound

BLOCK_COLORS = [
    "#ffadad", "#ffd6a5", "#fdffb6",
    "#caffbf", "#9bf6ff", "#a0c4ff",
    "#bdb2ff", "#ffc6ff", "#fffffc"
]
sudoku_puzzles = {
    "easy": [
        [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    ]
}
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Colorful Sudoku Solver")
        self.root.geometry("660x720")
        self.root.configure(bg="#2c3e50")

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.current_puzzle = []
        self.solved_puzzle = []
        self.start_time = None

        self.create_widgets()
        self.load_new_puzzle("easy")

    def create_widgets(self):
        title = tk.Label(self.root, text="Colorful Sudoku Solver", font=("Helvetica", 24, "bold"),
                         bg="#2c3e50", fg="white")
        title.pack(pady=10)

        self.frame = tk.Frame(self.root, bg="#2c3e50", pady=5)
        self.frame.pack()

        for i in range(9):
            for j in range(9):
                block_index = (i // 3) * 3 + (j // 3)
                bg_color = BLOCK_COLORS[block_index]

                entry = tk.Entry(self.frame, width=4, font=("Consolas", 20, "bold"), justify="center",
                                 bg=bg_color, fg="#1B1B2F", relief="flat", bd=2)
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

        btn_frame = tk.Frame(self.root, bg="#2c3e50")
        btn_frame.pack(pady=15)

        btn_style = {"font": ("Arial", 12, "bold"), "width": 15, "bg": "#34495e", "fg": "white", "bd": 0}

        tk.Button(btn_frame, text="🎯 Submit & Solve", command=self.solve_and_fill, **btn_style).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="🧩 New Puzzle", command=self.load_new_puzzle, **btn_style).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="✅ Check Answer", command=self.check_answer, **btn_style).grid(row=0, column=2, padx=10)

    def load_new_puzzle(self, difficulty="easy"):
        self.current_puzzle = copy.deepcopy(random.choice(sudoku_puzzles[difficulty]))
        self.solved_puzzle = copy.deepcopy(self.current_puzzle)
        self.solve(self.solved_puzzle)

        for i in range(9):
            for j in range(9):
                block_index = (i // 3) * 3 + (j // 3)
                bg_color = BLOCK_COLORS[block_index]
                val = self.current_puzzle[i][j]
                entry = self.entries[i][j]
                entry.config(bg=bg_color)
                entry.delete(0, tk.END)
                if val != 0:
                    entry.insert(0, str(val))
                    entry.config(state="disabled", disabledbackground=bg_color, disabledforeground="#000000")
                else:
                    entry.config(state="normal", bg=bg_color, fg="#000000")

        self.start_time = time.time()

    def solve_and_fill(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                board[i][j] = int(val) if val.isdigit() else 0

        if self.solve(board):
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(board[i][j]))
                    self.entries[i][j].config(state="disabled", disabledbackground="#B9FBC0", disabledforeground="#000000")
            self.play_sound(True)
            messagebox.showinfo("Solved", f"Solved in {int(time.time() - self.start_time)} seconds!")
        else:
            self.play_sound(False)
            messagebox.showerror("Error", "Puzzle could not be solved!")

    def check_answer(self):
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if not val.isdigit() or int(val) != self.solved_puzzle[i][j]:
                    self.entries[i][j].config(bg="#ffcccc")
                    self.play_sound(False)
                    messagebox.showwarning("Oops!", "Incorrect Answer!")
                    return
        self.play_sound(True)
        messagebox.showinfo("Perfect!", "All answers are correct!")

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.solve(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def play_sound(self, correct):
        try:
            if correct:
                winsound.Beep(800, 200)
            else:
                winsound.Beep(400, 400)
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
