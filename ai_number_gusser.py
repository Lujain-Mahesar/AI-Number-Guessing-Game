import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("960x640")
root.resizable(False, False)

first_guess_done = False
ai_attempts = 0
selected_difficulty = "Medium"  # Default difficulty
difficulty_ranges = {
    "Easy": (1, 50),
    "Medium": (1, 100),
    "Hard": (1, 500)
}
current_range = difficulty_ranges["Medium"]  # Default range
guess_history = []  # Track all guesses
player_attempts = 0  # Track player attempts

# Setup ttkbootstrap style
style = Style(theme="minty")
style.configure("Big.TButton", font=("Segoe UI", 14), padding=10)
style.configure("Difficulty.TButton", font=("Segoe UI", 12), padding=8)
style.configure("Small.TButton", font=("Segoe UI", 10), padding=4)

# Background Canvas
canvas = tk.Canvas(root, width=960, height=640, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_rectangle(0, 0, 960, 640, fill="#6C63FF", outline="")

def create_rounded_rect(canvas, x1, y1, x2, y2, r=40, **kwargs):
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

create_rounded_rect(canvas, 180, 120, 780, 520, r=40, fill="white", outline="")

# Main Menu Frame
frame = tk.Frame(root, bg="white")
frame.place(x=170, y=90, width=620, height=460)

title_font = ("Segoe UI", 28, "bold")
subtitle_font = ("Segoe UI", 13)

title = tk.Label(frame, text="🎮 Number Guessing Game", font=title_font, bg="white", fg="#222")
title.pack(pady=(40, 10))

subtitle = tk.Label(frame, text="Challenge your brain – Pick a mode", font=subtitle_font, bg="white", fg="#666")
subtitle.pack()

tk.Label(frame, bg="white").pack(pady=20)

# ========== DIFFICULTY SELECTION FRAME ==========
difficulty_frame = tk.Frame(root, bg="white")

difficulty_title = tk.Label(difficulty_frame, text="🎯 Select Difficulty Level", font=("Segoe UI", 24, "bold"), bg="white", fg="#222")
difficulty_title.pack(pady=(30, 20))

difficulty_subtitle = tk.Label(difficulty_frame, text="Choose your number range", font=subtitle_font, bg="white", fg="#666")
difficulty_subtitle.pack(pady=(0, 30))

selected_mode = ""  # Will store which mode was selected

def select_difficulty(difficulty, mode):
    global selected_difficulty, current_range, selected_mode
    selected_difficulty = difficulty
    current_range = difficulty_ranges[difficulty]
    selected_mode = mode
    
    # Hide difficulty frame and start the selected game mode
    difficulty_frame.place_forget()
    
    if mode == "ai_guesses":
        start_ai_guesses_mode()
    else:
        start_you_guess_mode()

# Easy difficulty button
easy_btn = Button(
    difficulty_frame,
    text="🟢 Easy (1-50)\nPerfect for beginners",
    bootstyle="success",
    style="Difficulty.TButton",
    width=22,
    command=lambda: select_difficulty("Easy", selected_mode)
)
easy_btn.pack(pady=6)

# Medium difficulty button
medium_btn = Button(
    difficulty_frame,
    text="🟡 Medium (1-100)\nStandard challenge",
    bootstyle="warning",
    style="Difficulty.TButton",
    width=22,
    command=lambda: select_difficulty("Medium", selected_mode)
)
medium_btn.pack(pady=6)

# Hard difficulty button
hard_btn = Button(
    difficulty_frame,
    text="🔴 Hard (1-500)\nFor experts only",
    bootstyle="danger",
    style="Difficulty.TButton",
    width=22,
    command=lambda: select_difficulty("Hard", selected_mode)
)
hard_btn.pack(pady=6)

def back_to_main_from_difficulty():
    difficulty_frame.place_forget()
    frame.place(x=170, y=90, width=620, height=460)

back_btn_difficulty = Button(difficulty_frame, text="⬅ Back to Menu", bootstyle="secondary", style="Big.TButton", width=20, command=back_to_main_from_difficulty)
back_btn_difficulty.pack(pady=15)

# ========== YOU GUESS AI'S NUMBER ==========
guess_frame = tk.Frame(root, bg="white")

guess_title = tk.Label(guess_frame, text="", font=("Segoe UI", 16), bg="white", fg="#222")
guess_title.pack(pady=20)

entry_var = tk.StringVar()
guess_entry = tk.Entry(guess_frame, textvariable=entry_var, font=("Segoe UI", 14), width=20, justify="center")
guess_entry.pack(pady=10)

feedback_label = tk.Label(guess_frame, text="", font=("Segoe UI", 13), bg="white", fg="#444")
feedback_label.pack(pady=10)

# Guess History Frame
history_frame = tk.Frame(guess_frame, bg="white")
history_frame.pack(pady=10)

history_title = tk.Label(history_frame, text="📝 Your Guesses:", font=("Segoe UI", 12, "bold"), bg="white", fg="#444")
history_title.pack()

history_text = tk.Text(history_frame, height=4, width=50, font=("Segoe UI", 10), bg="#f8f9fa", fg="#444", state="disabled", wrap="word")
history_text.pack(pady=5)

last_hint = ""

def check_guess():
    global last_hint, player_attempts
    try:
        guess = int(entry_var.get())
        if guess < current_range[0] or guess > current_range[1]:
            feedback_label.config(text=f"❗ Please enter a number between {current_range[0]} and {current_range[1]}.")
            return
        
        player_attempts += 1
        guess_history.append(guess)
        update_guess_history()
        feedback_label.config(text="")
        entry_var.set("")  # Clear the entry
        root.after(300, lambda: show_feedback(guess))
    except ValueError:
        feedback_label.config(text="❗ Please enter a valid number.")

def show_feedback(guess):
    global last_hint
    if guess < ai_number:
        if last_hint == "low":
            feedback_label.config(text="🔻 Still too low!")
        else:
            feedback_label.config(text="🔻 Too low!")
        last_hint = "low"
    elif guess > ai_number:
        if last_hint == "high":
            feedback_label.config(text="🔺 Still too high!")
        else:
            feedback_label.config(text="🔺 Too high!")
        last_hint = "high"
    else:
        feedback_label.config(text=f"✅ Correct! You guessed it in {player_attempts} attempts! ({selected_difficulty} mode)")
        last_hint = ""

def update_guess_history():
    history_text.config(state="normal")
    history_text.delete(1.0, tk.END)
    
    # Show recent guesses (last 10)
    recent_guesses = guess_history[-10:]
    history_line = f"Attempts: {player_attempts} | Recent guesses: "
    history_line += " → ".join(map(str, recent_guesses))
    
    if len(guess_history) > 10:
        history_line = f"... {history_line}"
    
    history_text.insert(tk.END, history_line)
    history_text.config(state="disabled")

submit_btn = Button(guess_frame, text="Submit Guess", bootstyle="success", style="Big.TButton", width=24, command=check_guess)
submit_btn.pack(pady=6)

def back_to_main():
    guess_frame.place_forget()
    ai_frame.place_forget()
    frame.place(x=170, y=90, width=620, height=460)

back_btn = Button(guess_frame, text="⬅ Back to Menu", bootstyle="secondary", style="Big.TButton", width=24, command=back_to_main)
back_btn.pack(pady=6)

# ========== AI GUESSES YOUR NUMBER ==========
ai_frame = tk.Frame(root, bg="white")

ai_label = tk.Label(ai_frame, text="", font=("Segoe UI", 16), bg="white", fg="#222")
ai_label.pack(pady=20)

ai_guess_label = tk.Label(ai_frame, text="", font=("Segoe UI", 22, "bold"), bg="white", fg="#222")
ai_guess_label.pack(pady=20)

attempts_label = tk.Label(ai_frame, text="Attempts: 0", font=("Segoe UI", 14), bg="white", fg="#555")
attempts_label.pack(pady=5)

ai_feedback = tk.Label(ai_frame, text="", font=subtitle_font, bg="white", fg="#555")
ai_feedback.pack(pady=10)

def ai_make_guess():
    global ai_low, ai_high, ai_guess, first_guess_done, ai_attempts
    if ai_low > ai_high:
        ai_feedback.config(text="🤖 Are you tricking me?")
        return

    if not first_guess_done:
        ai_guess = random.randint(ai_low, ai_high)
        first_guess_done = True
    else:
        ai_guess = (ai_low + ai_high) // 2

    ai_attempts += 1
    ai_guess_label.config(text=f"My guess is: {ai_guess}")
    attempts_label.config(text=f"Attempts: {ai_attempts}")
    ai_feedback.config(text="")

def higher():
    global ai_high
    ai_feedback.config(text="")
    ai_high = ai_guess - 1
    root.after(500, ai_make_guess)

def lower():
    global ai_low
    ai_feedback.config(text="")
    ai_low = ai_guess + 1
    root.after(500, ai_make_guess)

def correct():
    ai_feedback.config(text=f"🎉 Yay! I guessed it in {ai_attempts} attempts! ({selected_difficulty} mode)")

def set_ai_feedback(msg, direction):
    ai_feedback.config(text=msg)

btns = tk.Frame(ai_frame, bg="white")
btns.pack(pady=10)

Button(btns, text="🔼 Too High", bootstyle="info", style="Big.TButton", width=14, command=higher).grid(row=0, column=0, padx=5)
Button(btns, text="✅ Correct", bootstyle="success", style="Big.TButton", width=14, command=correct).grid(row=0, column=1, padx=5)
Button(btns, text="🔽 Too Low", bootstyle="warning", style="Big.TButton", width=14, command=lower).grid(row=0, column=2, padx=5)


back_btn2 = Button(ai_frame, text="⬅ Back to Menu", bootstyle="secondary", style="Big.TButton", width=20, command=back_to_main)
back_btn2.pack(pady=12)

# Game mode starting functions
def start_ai_guesses_mode():
    global ai_low, ai_high, first_guess_done, ai_attempts
    ai_low, ai_high = current_range
    first_guess_done = False
    ai_attempts = 0
    ai_label.config(text=f"🤖 Think of a number between {current_range[0]} and {current_range[1]}! ({selected_difficulty})")
    ai_frame.place(x=170, y=90, width=620, height=460)
    ai_make_guess()

def start_you_guess_mode():
    global ai_number, last_hint, guess_history, player_attempts
    ai_number = random.randint(current_range[0], current_range[1])
    entry_var.set("")
    feedback_label.config(text="")
    last_hint = ""
    guess_history = []  # Reset guess history
    player_attempts = 0  # Reset attempts
    
    # Clear and reset history display
    history_text.config(state="normal")
    history_text.delete(1.0, tk.END)
    history_text.insert(tk.END, "No guesses yet...")
    history_text.config(state="disabled")
    
    guess_title.config(text=f"🎯 I'm thinking of a number between {current_range[0]} and {current_range[1]} ({selected_difficulty})")
    guess_frame.place(x=170, y=90, width=620, height=460)

# Main menu actions - now show difficulty selection first
def ai_guesses_mode():
    global selected_mode
    selected_mode = "ai_guesses"
    frame.place_forget()
    difficulty_frame.place(x=170, y=90, width=620, height=460)

def you_guess_mode():
    global selected_mode
    selected_mode = "you_guess"
    frame.place_forget()
    difficulty_frame.place(x=170, y=90, width=620, height=460)

# Main menu buttons
ai_btn = Button(
    frame,
    text="🧠 AI Guesses Your Number",
    bootstyle="primary",
    style="Big.TButton",
    width=32,
    command=ai_guesses_mode
)
ai_btn.pack(pady=(8, 8))

you_btn = Button(
    frame,
    text="🤖 You Guess AI's Number",
    bootstyle="info",
    style="Big.TButton",
    width=32,
    command=you_guess_mode
)
you_btn.pack(pady=(0, 8))

root.mainloop()