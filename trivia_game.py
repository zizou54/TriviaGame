"""Simple trivia game built with Tkinter.

Each question has four options. Pick one to see whether it was right,
then move on. A restart button starts the game over at any time.
"""

import tkinter as tk

try:  # Crisp rendering on high-DPI Windows displays.
    import ctypes

    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Each question: (prompt, four options, index of the correct option)
QUESTIONS = [
    ("What is the capital of Turkey?", ["Istanbul", "Ankara", "Izmir", "Bursa"], 1),
    ("Which planet is known as the Red Planet?", ["Venus", "Jupiter", "Mars", "Saturn"], 2),
    ("How many continents are there on Earth?", ["5", "6", "7", "8"], 2),
    ("Who painted the Mona Lisa?", ["Leonardo da Vinci", "Picasso", "Van Gogh", "Michelangelo"], 0),
    ("What is the largest ocean on Earth?", ["Atlantic", "Indian", "Arctic", "Pacific"], 3),
]

CORRECT_MESSAGE = "Correct! Well done!"
WRONG_MESSAGE = "Oops, that's not right. The answer was: {answer}"

# Palette
BG = "#F4F1EC"
TEXT = "#2F3437"
MUTED = "#8E929A"
CARD = "#FFFFFF"
CARD_HOVER = "#ECE7DF"
ACCENT = "#7C9CBF"
ACCENT_HOVER = "#6A8BB0"
CORRECT = "#7FB685"
WRONG = "#D98880"

FONT = "Segoe UI"


class TriviaGame:
    def __init__(self, root):
        self.root = root
        root.title("Trivia")
        root.configure(bg=BG)
        root.minsize(520, 460)

        frame = tk.Frame(root, bg=BG, padx=28, pady=24)
        frame.pack(fill="both", expand=True)

        self.progress_label = tk.Label(frame, bg=BG, fg=MUTED, font=(FONT, 10))
        self.progress_label.pack(anchor="w")

        self.question_label = tk.Label(
            frame, bg=BG, fg=TEXT, font=(FONT, 15, "bold"), wraplength=460, justify="left"
        )
        self.question_label.pack(anchor="w", pady=(6, 16))

        self.option_buttons = []
        for i in range(4):
            button = self._make_button(frame, CARD, CARD_HOVER, TEXT, lambda i=i: self.choose(i))
            button.configure(anchor="w", padx=14)
            self.option_buttons.append(button)

        self.feedback_label = tk.Label(
            frame, bg=BG, fg=TEXT, font=(FONT, 11, "bold"), wraplength=460, justify="left"
        )
        self.feedback_label.pack(anchor="w", pady=(14, 10))

        controls = tk.Frame(frame, bg=BG)
        controls.pack(fill="x", side="bottom")
        self.next_button = self._make_button(controls, ACCENT, ACCENT_HOVER, "white", self.next_question)
        self.next_button.configure(text="Next", width=10)
        self.restart_button = self._make_button(controls, CARD, CARD_HOVER, TEXT, self.restart)
        self.restart_button.configure(text="Restart", width=10)
        self.restart_button.pack(side="left")

        self.restart()

    def _make_button(self, parent, bg, hover, fg, command):
        button = tk.Button(
            parent, bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
            relief="flat", bd=0, font=(FONT, 11), pady=8, cursor="hand2", command=command,
        )
        button.bind("<Enter>", lambda e: button["state"] == "normal" and button.configure(bg=hover))
        button.bind("<Leave>", lambda e: button["state"] == "normal" and button.configure(bg=bg))
        return button

    def restart(self):
        self.index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        prompt, options, _ = QUESTIONS[self.index]
        self.progress_label.configure(
            text=f"Question {self.index + 1} of {len(QUESTIONS)}   ·   Score: {self.score}"
        )
        self.question_label.configure(text=prompt)
        for button, option in zip(self.option_buttons, options):
            button.configure(text=option, state="normal", bg=CARD, disabledforeground=TEXT)
            button.pack(fill="x", pady=4, before=self.feedback_label)
        self.feedback_label.configure(text="")
        self.next_button.pack_forget()

    def choose(self, choice):
        _, options, answer = QUESTIONS[self.index]
        for button in self.option_buttons:
            button.configure(state="disabled")
        self.option_buttons[answer].configure(bg=CORRECT, disabledforeground="white")

        if choice == answer:
            self.score += 1
            self.feedback_label.configure(text=CORRECT_MESSAGE, fg=CORRECT)
        else:
            self.option_buttons[choice].configure(bg=WRONG, disabledforeground="white")
            self.feedback_label.configure(text=WRONG_MESSAGE.format(answer=options[answer]), fg=WRONG)

        self.progress_label.configure(
            text=f"Question {self.index + 1} of {len(QUESTIONS)}   ·   Score: {self.score}"
        )
        is_last = self.index == len(QUESTIONS) - 1
        self.next_button.configure(text="See score" if is_last else "Next")
        self.next_button.pack(side="right")

    def next_question(self):
        self.index += 1
        if self.index < len(QUESTIONS):
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        total = len(QUESTIONS)
        self.progress_label.configure(text="Game over")
        self.question_label.configure(text=f"You scored {self.score} out of {total}!")
        for button in self.option_buttons:
            button.pack_forget()
        if self.score == total:
            message = "Perfect score — you're a trivia master!"
        elif self.score >= total / 2:
            message = "Nice job! Press Restart to try for a perfect score."
        else:
            message = "Keep practicing! Press Restart to play again."
        self.feedback_label.configure(text=message, fg=TEXT)
        self.next_button.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    TriviaGame(root)
    root.mainloop()
