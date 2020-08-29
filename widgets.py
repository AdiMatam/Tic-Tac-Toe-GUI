import tkinter as tk


class Board(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.boxes = {}

        self.grid(row=0, column=0, rowspan=2, sticky="ns")

        for col in range(3):
            for row in range(3):
                box = tk.Frame(
                    self,
                    bg="white",
                    highlightbackground="black",
                    highlightthickness=1,
                    width=200,
                    height=200,
                )

                self.boxes[f"{row},{col}"] = box
                box.grid(row=row, column=col, sticky="nsew")


class Watch(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.configure(
            width=300,
            height=300,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
        )
        self.grid(row=0, column=1, sticky="ne")

        self.timecount = 0
        self.setup_watch()
        self.update_watch()

    def setup_watch(self):
        self.elapsed = tk.StringVar()
        self.watch = tk.Label(
            self,
            textvariable=self.elapsed,
            bg="white",
            font=("Lucida Grande", 24, "bold"),
            relief="sunken",
            padx=80,
            pady=5,
            bd=2,
        )
        self.watch.place(relx=0.5, rely=0.333, anchor="center")

        self.resetbut = tk.Button(
            self,
            text="Reset",
            font=("Lucida Grande", 12, "bold"),
            bg="#c6c6c6",
            padx=10,
            command=self.reset_watch,
        )
        self.resetbut.place(in_=self.watch, relx=0.5, rely=1.5, anchor="center")

    def update_watch(self):
        watchval = self.secs_to_str(self.timecount)
        self.elapsed.set(watchval)
        self.timecount += 1
        self.watch.after(1000, self.update_watch)

    def secs_to_str(self, elapSecs):
        secs = elapSecs % 60
        raw_mins = elapSecs // 60
        mins = raw_mins % 60
        hrs = (raw_mins // 60) % 60

        return f"{hrs:02}:{mins:02}:{secs:02}"

    def reset_watch(self):
        self.timecount = 0


class staticLabel(tk.Label):
    def __init__(self, master, text, relPos: tuple):
        super().__init__(master)
        self.config(
            text=text, font=("Lucida Grande", 20, "bold", "underline"), bg="white"
        )
        self.place(relx=relPos[0], rely=relPos[1], anchor="center")


class Tally(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.configure(
            width=300,
            height=300,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
        )
        self.grid(row=1, column=1, sticky="s")

        self.userScore = tk.IntVar(value=0)
        self.botScore = tk.IntVar(value=0)
        self.totalScore = tk.IntVar(value=0)

        self.setup_tally()

    def setup_tally(self):
        staticLabel(self, "Game Status", (0.5, 0.1))

        staticOffset = 0.3
        
        staticLabel(self, "USER", (staticOffset, 0.3))
        staticLabel(self, "BOT", (staticOffset, 0.5))
        staticLabel(self, "TOTAL", (staticOffset, 0.7))

        dynamicOffset = 0.6
        
        tk.Label(
            self,
            textvariable=self.userScore,
            bg="white",
            font=("Lucida Grande", 20, "bold"),
        ).place(relx=dynamicOffset, rely=0.3, anchor="center")

        tk.Label(
            self,
            textvariable=self.botScore,
            bg="white",
            font=("Lucida Grande", 20, "bold"),
        ).place(relx=dynamicOffset, rely=0.5, anchor="center")

        tk.Label(
            self,
            textvariable=self.totalScore,
            bg="white",
            font=("Lucida Grande", 20, "bold"),
        ).place(relx=dynamicOffset, rely=0.7, anchor="center")

    def increment(self, who: str):
        self.totalScore.set(self.totalScore.get() + 1)
        if who.lower == "user":
            self.userScore.set(self.userScore.get() + 1)
        else:
            self.botScore.set(self.botScore.get() + 1)
