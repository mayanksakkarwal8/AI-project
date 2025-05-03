import tkinter as tk
from tkinter import messagebox

# --------- Minimax Algorithm for AI ---------
def minimax(sticks, is_ai, depth=0):  # Added depth for debugging
    """
    Calculates the best move using the Minimax algorithm.

    Args:
        sticks: The number of sticks remaining.
        is_ai:  True if it's the AI's turn, False if it's the player's turn.
        depth:  The current depth of the recursion (for debugging).

    Returns:
        The evaluation of the position (1 for AI win, -1 for AI loss, 0 for draw).
    """
    indent = "  " * depth  # Create indentation for output
    print(f"{indent}minimax(sticks={sticks}, is_ai={is_ai}, depth={depth})")

    if sticks == 0:
        result = 1 if is_ai else -1  # Fix: AI wins if player took last stick
        print(f"{indent}Base case: sticks == 0, returning {result}")
        return result

    if is_ai:
        best = -float('inf')
        for i in range(1, 4):
            if sticks - i >= 0:
                val = minimax(sticks - i, False, depth + 1)
                best = max(best, val)
                print(f"{indent}AI:  Trying move {i}, value = {val}, best = {best}")
        print(f"{indent}AI: Returning best = {best}")
        return best
    else:
        best = float('inf')
        for i in range(1, 4):
            if sticks - i >= 0:
                val = minimax(sticks - i, True, depth + 1)
                best = min(best, val)
                print(f"{indent}Player: Trying move {i}, value = {val}, best = {best}")
        print(f"{indent}Player: Returning best = {best}")
        return best

def find_best_move(sticks):
    """
    Finds the best move for the AI to make.

    Args:
        sticks: The number of sticks remaining.

    Returns:
        The number of sticks the AI should take (1, 2, or 3).
    """
    print(f"find_best_move(sticks={sticks})")
    best_val = -float('inf')
    best_move = 1
    for i in range(1, 4):
        if sticks - i >= 0:
            value = minimax(sticks - i, False)
            print(f"  Move {i} has value {value}")
            if value > best_val:
                best_val = value
                best_move = i
    print(f"  Returning best_move = {best_move}")
    return best_move

# --------- Game Logic ---------
initial_sticks = 21  # Changed to a variable for easier modification
matchsticks = initial_sticks  # Initialize the game state

def update_display():
    """Updates the matchstick count display."""
    match_label.config(text=f"Matchsticks remaining: {matchsticks}")

def show_result(winner):
    """Displays the game result in a message box and quits."""
    messagebox.showinfo("Game Over", f"{winner} took the last matchstick.\n{winner} loses!")
    root.quit()  # Use root.quit() to properly close the Tkinter window

def player_move(pick):
    """
    Handles the player's move.

    Args:
        pick: The number of sticks the player takes (1, 2, or 3).
    """
    global matchsticks  # Need to use the global keyword
    if not 1 <= pick <= 3:  # Input validation
        status_label.config(text="Invalid move!  Pick 1, 2, or 3 sticks.")
        return

    if pick > matchsticks:
        status_label.config(text="Invalid move!  Not enough sticks remaining.")
        return

    matchsticks -= pick
    update_display()

    if matchsticks == 0:
        show_result("You")
    else:
        status_label.config(text="AI's turn...")  # Provide feedback to the player
        root.after(500, ai_move)  # Delay the AI's move slightly

def ai_move():
    """Handles the AI's move."""
    global matchsticks  # Need to use the global keyword
    if matchsticks <= 0:
        return  # important: prevent AI from making a move if no sticks left.

    ai_pick = find_best_move(matchsticks)
    status_label.config(text=f"AI picks: {ai_pick}")
    matchsticks -= ai_pick
    update_display()

    if matchsticks == 0:
        show_result("AI")
    else:
        status_label.config(text="Your turn...") # Inform the player
        # No need for root.after here, player moves are directly triggered by button clicks.

# --------- GUI ---------
root = tk.Tk()
root.title("Matchstick Game with AI")
root.geometry("400x300")  # Set a reasonable window size

match_label = tk.Label(root, text=f"Matchsticks remaining: {matchsticks}", font=("Arial", 16))
match_label.pack(pady=20)  # Add some padding for better visual appearance

btn_frame = tk.Frame(root)  # Use a frame to contain the buttons
btn_frame.pack(pady=10)

# Create buttons for taking 1, 2, or 3 sticks
for i in range(1, 4):
    btn = tk.Button(btn_frame, text=f"Take {i}", command=lambda i=i: player_move(i), width=10)
    btn.pack(side=tk.LEFT, padx=5)  # Pack the buttons into the frame

status_label = tk.Label(root, text="Your Turn", font=("Arial", 14))
status_label.pack(pady=20)

root.mainloop()
