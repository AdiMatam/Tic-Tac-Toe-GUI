import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from widgets import Board, Watch

import numpy as np
from random import randint


class Game(tk.Tk):
    def __init__(self, first=0, alternate="n"):
        super().__init__()
        self.resizable(False, False)
        self.watch = Watch(self)

        self.board = Board(self)
        self.boxes = self.board.boxes
        abox = list(self.boxes.values())[0]
        self.boxwidth = abox["width"]
        self.boxheight = abox["height"]

        self.first = first
        self.alternate = alternate
        self.symbols = ["ticx.png", "ticcircle.png"]
        self.playerdict = {0: "USER", 1: "BOT"}

        self.array = np.full((3, 3), 2, dtype="uint8")

        self.switch(player=first)

    def switch(self, player):
        if 2 not in self.array:
            self.retry_message("tie")

        elif self.wincheck(who=player ^ 1):
            self.retry_message("vic")

        else:
            if player == 0:
                for key in self.boxes:
                    self.boxes[key].bind("<Button-1>", self.userplay)
                    self.boxes[key].bind("<Enter>", self.hover)
                    self.boxes[key].bind("<Leave>", self.hover)
            elif player == 1:
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

    def get_image(self, who):
        if who == "user":
            symbol = self.symbols[0]
        elif who == "bot":
            symbol = self.symbols[1]

        imgopen = Image.open(symbol)
        resized = imgopen.resize(
            (self.boxwidth - 20, self.boxheight - 20), Image.ANTIALIAS
        )

        return ImageTk.PhotoImage(resized)

    def userplay(self, event):
        img = self.get_image("user")

        frame = event.widget
        label = tk.Label(frame, image=img, bg="white")
        label.image = img
        label.place(x=self.boxwidth // 2, y=self.boxheight // 2, anchor="center")

        self.array_update(frame)
        self.switch(player=1)

    def array_update(self, frame):
        gridx, gridy = (
            round(frame.winfo_x() / self.boxwidth),
            round(frame.winfo_y() / self.boxheight),
        )

        self.array[gridy, gridx] = 0
        print(self.array)

    def botplay(self):
        img = self.get_image("bot")

        if self.array[1, 1] == 2:  # if center is empty
            row = 1
            col = 1

        elif self.present2() is not None:  # possible victory in next turn?
            print("BLOCK/ATTACK")
            row, col = self.present2()

        else:  # random move
            print("RANDOM")
            locs = np.where(self.array == 2)
            coords = list(zip(locs[0], locs[1]))
            toplay = randint(0, len(coords))
            row, col = coords[toplay]

        leframe = self.boxes[f"{row},{col}"]
        label = tk.Label(leframe, image=img, bg="white")
        label.image = img
        label.place(x=self.boxwidth // 2, y=self.boxheight // 2, anchor="center")

        self.array[row, col] = 1
        print(self.array)
        self.switch(player=0)

    def present2(self):
        for i in range(3):
            subarr = self.array[i]
            if 2 in subarr:
                if (subarr == 0).sum() == 2 or (subarr == 1).sum() == 2:
                    return [i, subarr.tolist().index(2)]
            subarr = self.array[:, i]
            if 2 in subarr:
                if (subarr == 0).sum() == 2 or (subarr == 1).sum() == 2:
                    return [subarr.tolist().index(2), i]

        subarr = [self.array[i, i] for i in range(3)]
        if 2 in subarr:
            if subarr.count(0) == 2 or subarr.count(1) == 2:
                return [subarr.index(2)] * 2

        subarr = [self.array[i, abs(i - 2)] for i in range(3)]
        if 2 in subarr:
            if subarr.count(0) == 2 or subarr.count(1) == 2:
                row = subarr.index(2)
                return [row, abs(row - 2)]

        return None

    def wincheck(self, who):
        subarrs = []
        for i in range(3):
            subarrs.append(self.array[i].tolist())
            subarrs.append(self.array[:, i].tolist())
        subarrs.append([self.array[i, i] for i in range(3)])
        subarrs.append([self.array[i, abs(i - 2)] for i in range(3)])

        for trio in subarrs:
            if trio.count(0) == 3 or trio.count(1) == 3:
                self.winner = self.playerdict[who]
                return True

        return None

    def retry_message(self, endtype):
        if endtype == "tie":
            mes = "Its a tie!\n\nWould you like to play again?"
        elif endtype == "vic":
            mes = f"{self.winner} won the game!\n\nWould you like to play again?"

        response = messagebox.askyesno(title="Game Over!", message=mes)

        if response is True:
            self.reset()
        elif response is False:
            self.destroy()
            print("DONE")

    def reset(self):
        for box in self.boxes:
            frm = self.boxes[box]
            for child in frm.winfo_children():
                child.destroy()
        self.array = np.full((3, 3), 2, dtype="uint8")
        if "y" in self.alternate:
            self.switch(player=self.first ^ 1)
        else:
            self.switch(player=self.first)


g = Game(first=0)
g.mainloop()
