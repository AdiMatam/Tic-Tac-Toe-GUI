import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from widgets import Board, Watch, Tally

import numpy as np
from random import randint


class Game(tk.Tk):
    def __init__(self, first="USER"):
        super().__init__()
        self.resizable(False, False)
        self.watch = Watch(self)
        self.tally = Tally(self)

        self.board = Board(self)
        self.boxes = self.board.boxes
        abox = list(self.boxes.values())[0]
        self.boxwidth, self.boxheight = abox["width"], abox["height"]

        self.playerdict = {0: "USER", 1: "BOT", "USER": 0, "BOT": 1}
        self.turn = self.playerdict[first.upper()]

        self.symbols = [r"imgs\ticx.png", r"imgs\ticcircle.png"]

        self.array = np.full((3, 3), 2, dtype="uint8")

        self.switch()

    def switch(self):
        if 2 not in self.array:
            self.retry_message("tie")

        else:
            if self.turn == 0:
                for key in self.boxes:
                    self.boxes[key].bind("<Button-1>", self.userplay)
                    self.boxes[key].bind("<Enter>", self.hover)
                    self.boxes[key].bind("<Leave>", self.hover)
            elif self.turn == 1:
                for key in self.boxes:
                    self.boxes[key].bind("<Button-1>", lambda e: None)
                self.after(1000, self.botplay)

    def hover(self, event):
        frm = event.widget
        if frm.winfo_children() == []:
            if "Enter" in repr(event):
                frm["bg"] = "#87CEEB"
            else:
                frm["bg"] = "white"
        else:
            frm["bg"] = "white"

    def get_image(self):
        symbol = self.symbols[self.turn]
        imgopen = Image.open(symbol)
        resized = imgopen.resize(
            (self.boxwidth - 20, self.boxheight - 20), Image.ANTIALIAS
        )

        return ImageTk.PhotoImage(resized)

    def userplay(self, event):
        img = self.get_image()

        frame = event.widget
        label = tk.Label(frame, image=img, bg="white")
        label.image = img
        label.place(x=self.boxwidth // 2, y=self.boxheight // 2, anchor="center")

        self.array_update(frame)

        self.wincheck()
        self.turn ^= 1
        self.switch()

    def array_update(self, frame):
        gridx, gridy = (
            round(frame.winfo_x() / self.boxwidth),
            round(frame.winfo_y() / self.boxheight),
        )

        self.array[gridy, gridx] = 0
        print(self.array)

    def botplay(self):
        img = self.get_image()

        if self.array[1, 1] == 2:  # if center is empty
            row = 1
            col = 1

        elif coord := self.present2(1):  # possible victory for self?
            print("FINISH")
            row, col = coord

        elif coord := self.present2(0):  # possible victory for user?
            print("BLOCK")
            row, col = coord

        else:  # random move
            print("RANDOM")
            locs = np.where(self.array == 2)
            coords = list(zip(locs[0], locs[1]))
            print(coords)
            row, col = coords[randint(0, len(coords) - 1)]

        leframe = self.boxes[f"{row},{col}"]
        label = tk.Label(leframe, image=img, bg="white")
        label.image = img
        label.place(x=self.boxwidth // 2, y=self.boxheight // 2, anchor="center")

        self.array[row, col] = 1
        print(self.array)

        self.wincheck()
        self.turn ^= 1
        self.switch()

    def present2(self, who):
        for i in range(3):
            subarr = list(self.array[i])
            if 2 in subarr and subarr.count(who) == 2:
                return [i, subarr.index(2)]

            subarr = list(self.array[:, i])
            if 2 in subarr and subarr.count(who) == 2:
                return [subarr.index(2), i]

        subarr = [self.array[i, i] for i in range(3)]
        if 2 in subarr and subarr.count(who) == 2:
            return [subarr.index(2)] * 2

        subarr = [self.array[i, abs(i - 2)] for i in range(3)]
        if 2 in subarr and subarr.count(who) == 2:
            row = subarr.index(2)
            return [row, abs(row - 2)]

        return None

    def wincheck(self):
        subarrs = []
        for i in range(3):
            subarrs.append(self.array[i].tolist())
            subarrs.append(self.array[:, i].tolist())
        subarrs.append([self.array[i, i] for i in range(3)])
        subarrs.append([self.array[i, abs(i - 2)] for i in range(3)])

        for trio in subarrs:
            if trio.count(self.turn) == 3:
                self.retry_message("vic")

        return None

    def retry_message(self, endtype):
        if endtype == "tie":
            mes = "Its a tie!\n\nWould you like to play again?"
        elif endtype == "vic":
            mes = f"{self.playerdict[self.turn]} won the game!\n\nWould you like to play again?"
            self.tally.increment(self.playerdict[self.turn])

        response = messagebox.askyesno(title="Game Over!", message=mes)

        if response:
            self.reset()
        else:
            self.destroy()
            print("DONE")

    def reset(self):
        for box in self.boxes:
            frm = self.boxes[box]
            for child in frm.winfo_children():
                child.destroy()
        self.array = np.full((3, 3), 2, dtype="uint8")

        self.switch()


if __name__ == "__main__":
    g = Game(first="BOT")
    g.mainloop()
