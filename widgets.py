import tkinter as tk


class Board(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.boxes = {}

        self.grid(row=0, column=0, sticky="nsew")

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
        self.grid(row=0, column=1, sticky="n")

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

