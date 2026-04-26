from tkinter import *
from tkinter import messagebox
import json
import math


class GomokuWindow:
    def __init__(self, my_name, peer_name, send_func, i_go_first):
        self.root = Toplevel()
        self.root.title(f"Gomoku Battle: {my_name} vs {peer_name}")
        self.root.resizable(False, False)

        self.my_name = my_name
        self.peer_name = peer_name
        self.send_func = send_func
        self.my_turn = i_go_first

        self.my_color_id = 1 if i_go_first else 2
        self.peer_color_id = 2 if i_go_first else 1

        self.rows = 15
        self.cell_size = 30
        self.offset = 30
        self.board_size = self.cell_size * (self.rows - 1) + 2 * self.offset

        self.board_data = [[0 for _ in range(self.rows)] for _ in range(self.rows)]

        self.setup_ui()

        self.canvas.bind("<Button-1>", self.on_click)
        self.update_status()

    def setup_ui(self):
        self.lbl_status = Label(self.root, text="Initializing...", font=("Arial", 12, "bold"))
        self.lbl_status.pack(pady=5)

        self.canvas = Canvas(self.root, width=self.board_size, height=self.board_size, bg="#E3C087")  # 木纹色
        self.canvas.pack(padx=10, pady=10)

        for i in range(self.rows):
            start = (self.offset, self.offset + i * self.cell_size)
            end = (self.board_size - self.offset, self.offset + i * self.cell_size)
            self.canvas.create_line(start, end, width=2)
            start = (self.offset + i * self.cell_size, self.offset)
            end = (self.offset + i * self.cell_size, self.board_size - self.offset)
            self.canvas.create_line(start, end, width=2)

        self.draw_star_point(7, 7)
        self.draw_star_point(3, 3)
        self.draw_star_point(3, 11)
        self.draw_star_point(11, 3)
        self.draw_star_point(11, 11)

    def draw_star_point(self, r, c):
        x = self.offset + c * self.cell_size
        y = self.offset + r * self.cell_size
        r = 3
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")

    def update_status(self):
        if self.my_turn:
            self.lbl_status.config(text="YOUR TURN (Black)" if self.my_color_id == 1 else "YOUR TURN (White)",
                                   fg="green")
            self.canvas.config(cursor="hand2")
        else:
            self.lbl_status.config(text=f"Waiting for {self.peer_name}...", fg="red")
            self.canvas.config(cursor="arrow")

    def get_coord(self, event):
        x, y = event.x, event.y
        col = round((x - self.offset) / self.cell_size)
        row = round((y - self.offset) / self.cell_size)
        return row, col

    def on_click(self, event):
        if not self.my_turn:
            return

        row, col = self.get_coord(event)

        if 0 <= row < self.rows and 0 <= col < self.rows:
            if self.board_data[row][col] == 0:
                self.place_piece(row, col, self.my_color_id)
                self.my_turn = False
                self.update_status()

                msg = json.dumps({
                    "action": "game",
                    "from": self.my_name,
                    "to": self.peer_name,
                    "data": f"{row},{col}"
                })
                self.send_func(msg)                   #################

                if self.check_winner(row, col, self.my_color_id):
                    messagebox.showinfo("Game Over", "YOU WIN! 🏆")
                    self.root.destroy()

    def on_peer_move(self, data_str):
        try:
            row, col = map(int, data_str.split(','))

            self.place_piece(row, col, self.peer_color_id)
            self.my_turn = True
            self.update_status()

            if self.check_winner(row, col, self.peer_color_id):
                messagebox.showinfo("Game Over", "YOU LOSE! 💀")
                self.root.destroy()

        except ValueError:
            print("Invalid move data received")

    def place_piece(self, row, col, color_id):
        self.board_data[row][col] = color_id

        x = self.offset + col * self.cell_size
        y = self.offset + row * self.cell_size
        radius = 12
        color = "black" if color_id == 1 else "white"

        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="gray")

        if hasattr(self, 'last_move_marker'):
            self.canvas.delete(self.last_move_marker)
        self.last_move_marker = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red", outline="red")

    def check_winner(self, row, col, color_id):
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dr, dc in directions:
            count = 1
            for i in range(1, 5):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < self.rows and 0 <= c < self.rows and self.board_data[r][c] == color_id:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                r, c = row - dr * i, col - dc * i
                if 0 <= r < self.rows and 0 <= c < self.rows and self.board_data[r][c] == color_id:
                    count += 1
                else:
                    break

            if count >= 5:
                return True
        return False