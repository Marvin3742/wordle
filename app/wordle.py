import tkinter as tk
import random

SEED = 42
WORD_LIST = "../data/words.txt"
random.seed(SEED)

def grade_guess(start, end):
    winning_word_freq = {}

    for char in winning_word:
        winning_word_freq[char] = winning_word_freq.get(char, 0) + 1

    for i, char in zip(range(start, end), winning_word):
        if word_slots[i]["text"] == char:
            word_slots[i].config(bg="green", fg="white")
            winning_word_freq[char] -= 1

    for i in range(start, end):
        guess_char = word_slots[i]["text"]

        if guess_char == winning_word[i - start]:
            continue  
        elif winning_word_freq.get(guess_char, 0) > 0:
            word_slots[i].config(bg="orange", fg="white")
            winning_word_freq[guess_char] -= 1

        else:
            word_slots[i].config(bg="black", fg="white")

def handle_enter_button():
    global current_row, current_col, game_won, game_over
    if game_won or game_over:
        return

    if current_col != 4 or word_slots[(current_row*5) + 4]["text"] == "":
        status_label.config(text="Not enough letters.")
        root.after(2000, lambda: status_label.config(text="Guess the word!"))
        return
    else:
        start = current_row * 5
        end = (current_row*5) + 5
        user_guess = ""
        for j in range(start, end):
            user_guess += word_slots[j]["text"]

        if user_guess == winning_word:
            grade_guess(start, end)
            status_label.config(text=f"Correct!")
            game_won = True
            game_over = True
            return
        if current_row+1 == 6:
            grade_guess(start, end)
            status_label.config(text=f"Game over! Word was {winning_word}.")
        else:
            grade_guess(start, end)
            status_label.config(text=f"Incorrect.")   
            root.after(2000, lambda: status_label.config(text="Guess the word!")) 
            current_row += 1
            current_col = 0
        return
    
def handle_keyboard_button(i):
    global current_row, current_col, game_won, game_over
    if game_won or game_over:
        return

    word_slots[(current_row*5) + current_col].config(text=keys[i])
    current_col = min(4, current_col+1)

def handle_back_button():
    global game_over, game_won, current_row, current_col
    if game_won or game_over:
        return
    if current_col == 4 and word_slots[(current_row*5) + current_col]["text"] != "":
        word_slots[(current_row*5) + current_col].config(text="")
    else:
        current_col = max(0, current_col-1)
        word_slots[(current_row*5) + current_col].config(text="")


def handle_restart_button():
    global game_won, game_over, current_row, current_col, winning_word
    for slot in word_slots:
        slot.config(text="", bg="white", fg="black")
    status_label.config(text=f"Guess the word!")
    current_row, current_col = 0, 0
    game_won = False
    game_over = False
    winning_word = random.choice(word_list).upper().strip()

with open(WORD_LIST, "r") as f:
    word_list = f.readlines()

winning_word = random.choice(word_list).upper().strip()

keys = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", 
        "S", "D", "F", "G", "H", "J", "K", "L", "ENTER", "Z", 
        "X", "C", "V", "B", "N", "M", "BACK",]

current_row, current_col = 0, 0
game_won = False
game_over = False

root = tk.Tk()
root.configure(bg="darkgrey")
root.title("Wordle")

status_label = tk.Label(
    root,
    text="Guess the word!",
    font=("Arial", 25, "bold"),
    padx=10,
    pady=10
)

status_label.grid(row=0, column=0, columnspan=3, pady=10)

word_frame = tk.Frame(root, bg="darkgrey")
keyboard_frame = tk.Frame(root, bg="darkgrey")

word_frame.grid(row=1, column=0, padx=25, pady=25)
keyboard_frame.grid(row=2, column=0, padx=25, pady=25)

word_slots = []
for i in range(30):
    word_slot = tk.Label(
        word_frame,
        text="",
        font=("Arial", 24, "bold"),
        width=6,
        height=3,
    )

    word_slot.grid(
        row=(i // 5),
        column=i%5,
        padx=3,
        pady=3
    )
    word_slots.append(word_slot)

keyboard_buttons = []
for i in range(28):
    keyboard_button = tk.Button(
        keyboard_frame,
        text=keys[i],
        font=("Arial", 14, "bold"),
        width=5,
        height=2,
        command=lambda i=i: (handle_enter_button() if keys[i] == "ENTER" 
                             else handle_back_button() if keys[i] == "BACK" 
                             else handle_keyboard_button(i))
    )

    keyboard_button.grid(
        row=(i // 10),
        column=i%10,
    )
    keyboard_buttons.append(keyboard_button)

restart_button = tk.Button(
    root,
    text="Restart",
    font=("Arial", 12),
    width=7,
    height=3,
    command=handle_restart_button
)

restart_button.grid(
    row=4,
    column=0
)
root.mainloop()