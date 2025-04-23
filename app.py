import tkinter as tk
from tkinter import messagebox

# --------- Minimax Algorithm for AI ---------
def minimax(sticks, is_ai):
    if sticks == 0:
        return -1 if is_ai else 1

    if is_ai:
        best = -float('inf')
        for i in range(1, 4):
            if sticks - i >= 0:
                best = max(best, minimax(sticks - i, False))
        return best
    else:
        best = float('inf')
        for i in range(1, 4):
            if sticks - i >= 0:
                best = min(best, minimax(sticks - i, True))
        return best

def find_best_move(sticks):
    best_val = -float('inf')
    best_move = 1
    for i in range(1, 4):
        if sticks - i >= 0:
            value = minimax(sticks - i, False)
            if value > best_val:
                best_val = value
                best_move = i
    return best_move

# --------- Game Logic ---------
matchsticks = 21

def update_display():
    match_label.config(text=f"Matchsticks remaining: {matchsticks}")

def show_result(winner):
    messagebox.showinfo("Game Over", f"{winner} took the last matchstick.\n{winner} loses!")
    root.quit()

def player_move(pick):
    global matchsticks
    if pick > matchsticks:
        status_label.config(text="Invalid move!")
        return
    matchsticks -= pick
    update_display()

    if matchsticks == 0:
        show_result("You")
    else:
        root.after(500, ai_move)

def ai_move():
    global matchsticks
    ai_pick = find_best_move(matchsticks)
    status_label.config(text=f"AI picks: {ai_pick}")
    matchsticks -= ai_pick
    update_display()

    if matchsticks == 0:
        show_result("AI")

# --------- GUI ---------
root = tk.Tk()
root.title("Matchstick Game with AI")
root.geometry("400x300")

match_label = tk.Label(root, text=f"Matchsticks remaining: {matchsticks}", font=("Arial", 16))
match_label.pack(pady=20)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

for i in range(1, 4):
    tk.Button(btn_frame, text=f"Take {i}", command=lambda i=i: player_move(i), width=10).pack(side=tk.LEFT, padx=5)

status_label = tk.Label(root, text="Your Turn", font=("Arial", 14))
status_label.pack(pady=20)

root.mainloop()
