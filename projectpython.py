import tkinter as tk
import random
from functools import partial

# Step 1: Create main window
root = tk.Tk()
root.title("Memory Puzzle Game")
root.configure(bg='#2C3E50')
root.resizable(False, False)

# Step 2: Define symbols with their natural colors
symbols = [
    ('🍎', '#FF6B6B'),  # Red Apple
    ('🍌', '#FFD93D'),  # Yellow Banana
    ('🍓', '#FF6B9D'),  # Pink Strawberry
    ('🍇', '#9B59B6'),  # Purple Grapes
    ('🍉', '#FF6B6B'),  # Red Watermelon
    ('🍒', '#E74C3C'),  # Red Cherries
    ('🍊', '#F39C12'),  # Orange Orange
    ('🥝', '#A3CB38')   # Green Kiwi
]
cards = symbols * 2
random.shuffle(cards)

# Step 3: Variables
flipped = []  # stores indexes of flipped cards
buttons = []
matched_pairs = 0
total_pairs = len(symbols)
moves = 0

# Step 4: Create header with score
header_frame = tk.Frame(root, bg='#2C3E50')
header_frame.grid(row=0, column=0, columnspan=4, pady=10)

moves_label = tk.Label(header_frame, text="Moves: 0", font=('Arial', 14, 'bold'), 
                      fg='#ECF0F1', bg='#2C3E50')
moves_label.pack(side=tk.LEFT, padx=20)

pairs_label = tk.Label(header_frame, text="Pairs: 0/8", font=('Arial', 14, 'bold'), 
                      fg='#ECF0F1', bg='#2C3E50')
pairs_label.pack(side=tk.RIGHT, padx=20)

# Step 5: Function to handle click
def on_click(index):
    global moves
    
    # Prevent clicking already flipped or matched cards
    button = buttons[index]
    if button['state'] == 'disabled' and button['bg'] != '#27AE60':
        return
    
    # Prevent clicking more than 2 cards
    if len(flipped) >= 2:
        return
    
    # Flip the card with animation effect - show fruit with its natural color
    fruit, color = cards[index]
    button.config(text=fruit, fg=color, bg='#FFFFFF', 
                  state='disabled', relief='sunken')
    flipped.append(index)
    
    if len(flipped) == 2:
        moves += 1
        moves_label.config(text=f"Moves: {moves}")
        root.after(800, check_match)

# Step 6: Check for match
def check_match():
    global matched_pairs
    first, second = flipped
    
    # Compare the fruit emojis (first element of the tuple)
    if cards[first][0] == cards[second][0]:
        # Match found - change to green background but keep fruit color
        fruit1, color1 = cards[first]
        fruit2, color2 = cards[second]
        buttons[first].config(bg='#27AE60', fg=color1, state='disabled')
        buttons[second].config(bg='#27AE60', fg=color2, state='disabled')
        matched_pairs += 1
        pairs_label.config(text=f"Pairs: {matched_pairs}/{total_pairs}")
        
        # Check for win
        if matched_pairs == total_pairs:
            show_win_message()
    else:
        # No match - flip back with animation
        root.after(200, lambda: buttons[first].config(bg='#3498DB', text='', state='normal'))
        root.after(200, lambda: buttons[second].config(bg='#3498DB', text='', state='normal'))
    
    flipped.clear()

# Step 7: Enhanced Win Message
def show_win_message():
    # Create a colorful win frame
    win_frame = tk.Frame(root, bg='#27AE60', relief='raised', bd=5)
    win_frame.grid(row=3, column=0, columnspan=4, pady=15, padx=10, sticky='ew')
    
    # Win title with emojis
    win_label = tk.Label(win_frame, text="🎉 Congratulations! You Win! 🎉", 
                        font=('Arial', 20, 'bold'), fg='white', bg='#27AE60')
    win_label.pack(pady=10)
    
    # Score display
    score_label = tk.Label(win_frame, 
                          text=f"Final Score: {moves} moves", 
                          font=('Arial', 16, 'bold'), fg='#F1C40F', bg='#27AE60')
    score_label.pack(pady=5)
    
    # Performance rating
    performance = ""
    if moves <= 16:
        performance = "⭐ Perfect! ⭐"
        color = '#F1C40F'  # Gold
    elif moves <= 24:
        performance = "Great Job!"
        color = '#2ECC71'  # Green
    else:
        performance = "Good Game!"
        color = '#E74C3C'  # Red
    
    performance_label = tk.Label(win_frame, text=performance,
                               font=('Arial', 14, 'bold'), fg=color, bg='#27AE60')
    performance_label.pack(pady=5)
    
    # Display all matched fruits in a row with their colors
    fruits_frame = tk.Frame(win_frame, bg='#27AE60')
    fruits_frame.pack(pady=10)
    
    for fruit, color in symbols:
        fruit_label = tk.Label(fruits_frame, text=fruit, font=('Arial', 16),
                              fg=color, bg='#27AE60')
        fruit_label.pack(side=tk.LEFT, padx=3)
    
    # Add restart button with nice styling
    restart_btn = tk.Button(win_frame, text="🔄 Play Again", font=('Arial', 14, 'bold'),
                           bg='#E74C3C', fg='white', activebackground='#C0392B',
                           relief='raised', bd=3, padx=20, pady=10,
                           command=restart_game)
    restart_btn.pack(pady=15)
    
    # Add some celebration effects
    celebrate_label = tk.Label(win_frame, text="★" * 20, 
                             font=('Arial', 12), fg='#F1C40F', bg='#27AE60')
    celebrate_label.pack(pady=5)

# Step 8: Restart game function
def restart_game():
    global flipped, matched_pairs, moves
    flipped.clear()
    matched_pairs = 0
    moves = 0
    
    # Reset labels
    moves_label.config(text="Moves: 0")
    pairs_label.config(text="Pairs: 0/8")
    
    # Remove win frame if exists
    for widget in root.grid_slaves():
        if widget.grid_info()['row'] == 3:
            widget.destroy()
    
    # Reshuffle cards
    random.shuffle(cards)
    
    # Reset all buttons
    for i, button in enumerate(buttons):
        button.config(text='', bg='#3498DB', fg='#3498DB', 
                     state='normal', relief='raised')

# Step 9: Create grid of buttons with better styling
button_frame = tk.Frame(root, bg='#2C3E50')
button_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

for i in range(len(cards)):
    btn = tk.Button(button_frame, text='', width=6, height=3, 
                   font=('Arial', 18, 'bold'),
                   bg='#3498DB',  # Nice blue color for card back
                   fg='#3498DB',  # Same as background to hide text
                   activebackground='#2980B9',
                   relief='raised',
                   bd=3,
                   command=partial(on_click, i))
    btn.grid(row=i // 4, column=i % 4, padx=4, pady=4)
    buttons.append(btn)

# Step 10: Add footer with instructions
footer_label = tk.Label(root, text="Match all colorful fruit pairs with the fewest moves!", 
                       font=('Arial', 10), fg='#BDC3C7', bg='#2C3E50')
footer_label.grid(row=2, column=0, columnspan=4, pady=5)

# Center the window on screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'+{x}+{y}')

root.mainloop()