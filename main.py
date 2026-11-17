import tkinter as tk
from tkinter import messagebox
import time
import random

PASSAGES = [
    "Programming in Python is simple, fun, and powerful. Practice typing daily to improve your speed and accuracy.",
    "The quick brown fox jumps over the lazy dog. Consistent practice helps develop strong keyboard muscle memory.",
    "Computer science is the study of computation and information. Touch typing makes coding effortless and fast.",
    "Artificial intelligence and data science are transforming the world through smart algorithms and automation.",
    "Practice makes perfect. Focus on typing accurately first, and your typing speed will naturally increase over time."
]


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("SpeedType - Typing Speed Test")
        self.root.geometry("820x480")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.time_limit = 60
        self.time_left = self.time_limit
        self.running = False
        self.start_time = None
        self.timer_id = None
        self.target_text = ""
        self.typed_chars = 0
        self.correct_chars = 0
        self.errors = 0

        self.setup_ui()
        self.new_test()

    def setup_ui(self):
        title = tk.Label(
            self.root, text="⚡ TYPING SPEED TEST",
            font=("Segoe UI", 18, "bold"),
            fg="black", bg="white"
        )
        title.pack(pady=(18, 10))

        stats_frame = tk.Frame(self.root, bg="white")
        stats_frame.pack(fill="x", padx=40, pady=(0, 15))

        self.card_wpm = self.make_card(
            stats_frame, "SPEED", "0 WPM", "#008000"
        )
        self.card_acc = self.make_card(
            stats_frame, "ACCURACY", "100%", "#b8860b"
        )
        self.card_time = self.make_card(
            stats_frame, "TIME LEFT", f"{self.time_limit}s", "#0077aa"
        )
        self.card_err = self.make_card(
            stats_frame, "ERRORS", "0", "#cc0000"
        )

        self.text_display = tk.Text(
            self.root, font=("Consolas", 14), wrap="word", height=4,
            bg="white", fg="black", padx=15, pady=12,
            relief="solid", bd=1
        )
        self.text_display.pack(
            fill="x", padx=40, pady=(0, 15)
        )

        self.text_display.tag_configure(
            "correct", foreground="#008000"
        )
        self.text_display.tag_configure(
            "wrong", foreground="#cc0000", background="#ffe6e6"
        )
        self.text_display.tag_configure(
            "current", underline=True, foreground="black"
        )
        self.text_display.configure(state="disabled")

        self.entry = tk.Entry(
            self.root, font=("Consolas", 14),
            bg="white", fg="black",
            insertbackground="black",
            relief="solid", bd=1
        )
        self.entry.pack(
            fill="x", padx=40, ipady=8, pady=(0, 18)
        )
        self.entry.bind("<KeyRelease>", self.on_key)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=5)

        self.btn_time = tk.Button(
            btn_frame, text="⏱️ Mode: 60s",
            font=("Segoe UI", 10, "bold"),
            bg="white", fg="black",
            relief="solid", bd=1, padx=14, pady=5,
            command=self.toggle_time
        )
        self.btn_time.pack(side="left", padx=8)

        btn_new = tk.Button(
            btn_frame, text="🔀 New Passage",
            font=("Segoe UI", 10, "bold"),
            bg="white", fg="black",
            relief="solid", bd=1, padx=14, pady=5,
            command=self.new_test
        )
        btn_new.pack(side="left", padx=8)

        btn_restart = tk.Button(
            btn_frame, text="🔄 Restart",
            font=("Segoe UI", 10, "bold"),
            bg="white", fg="black",
            relief="solid", bd=1, padx=18, pady=5,
            command=self.restart_test
        )
        btn_restart.pack(side="left", padx=8)

    def make_card(self, parent, title, val, color):
        box = tk.Frame(
            parent, bg="white", padx=15, pady=8,
            highlightbackground="#cccccc", highlightthickness=1
        )
        box.pack(side="left", expand=True, fill="x", padx=6)

        tk.Label(
            box, text=title,
            font=("Segoe UI", 8, "bold"),
            fg="black", bg="white"
        ).pack()

        lbl_val = tk.Label(
            box, text=val,
            font=("Segoe UI", 15, "bold"),
            fg=color, bg="white"
        )
        lbl_val.pack()
        return lbl_val

    def toggle_time(self):
        self.time_limit = 30 if self.time_limit == 60 else 60
        self.btn_time.config(text=f"⏱️ Mode: {self.time_limit}s")
        self.restart_test()

    def new_test(self):
        self.target_text = random.choice(PASSAGES)
        self.restart_test()

    def restart_test(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.running = False
        self.start_time = None
        self.time_left = self.time_limit
        self.typed_chars = self.correct_chars = self.errors = 0

        self.card_wpm.config(text="0 WPM")
        self.card_acc.config(text="100%")
        self.card_time.config(text=f"{self.time_left}s")
        self.card_err.config(text="0")

        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.update_text_display("")
        self.entry.focus_set()

    def update_text_display(self, typed):
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", self.target_text)

        for i, char in enumerate(typed):
            if i < len(self.target_text):
                tag = (
                    "correct"
                    if char == self.target_text[i]
                    else "wrong"
                )
                self.text_display.tag_add(
                    tag, f"1.0+{i}c", f"1.0+{i+1}c"
                )

        if len(typed) < len(self.target_text):
            self.text_display.tag_add(
                "current",
                f"1.0+{len(typed)}c",
                f"1.0+{len(typed)+1}c"
            )

        self.text_display.config(state="disabled")

    def on_key(self, event):
        if not self.running and self.entry.get():
            self.running = True
            self.start_time = time.time()
            self.tick_timer()

        typed = self.entry.get()
        self.update_text_display(typed)

        self.typed_chars = len(typed)
        self.correct_chars = sum(
            1 for i, c in enumerate(typed)
            if i < len(self.target_text)
            and c == self.target_text[i]
        )
        self.errors = self.typed_chars - self.correct_chars

        elapsed_mins = (
            max(0.001, (time.time() - self.start_time) / 60)
            if self.start_time else 0.001
        )

        wpm = int((self.correct_chars / 5) / elapsed_mins)
        acc = (
            int((self.correct_chars / self.typed_chars) * 100)
            if self.typed_chars > 0 else 100
        )

        self.card_wpm.config(text=f"{wpm} WPM")
        self.card_acc.config(text=f"{acc}%")
        self.card_err.config(text=str(self.errors))

        if len(typed) >= len(self.target_text):
            self.finish_test()

    def tick_timer(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.card_time.config(text=f"{self.time_left}s")
            self.timer_id = self.root.after(1000, self.tick_timer)
        elif self.time_left <= 0:
            self.finish_test()

    def finish_test(self):
        if not self.running:
            return

        self.running = False

        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.entry.config(state="disabled")

        wpm_val = int(self.card_wpm.cget("text").split()[0])
        acc_val = self.card_acc.cget("text")

        rating = (
            "Master Typer! 🏆" if wpm_val >= 60
            else "Good Job! 🚀" if wpm_val >= 40
            else "Keep Practicing! 👍"
        )

        messagebox.showinfo(
            "Test Results",
            f"🎉 Test Completed!\n\n"
            f"Speed: {wpm_val} WPM\n"
            f"Accuracy: {acc_val}\n"
            f"Errors: {self.errors}\n\n"
            f"Rating: {rating}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()