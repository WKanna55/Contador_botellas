import tkinter as tk
from tkinter import font

# Create the main window
root = tk.Tk()
root.title("Available Fonts")

# Create a frame to hold the font list
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Get all available fonts
available_fonts = list(font.families())

# Create a scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox to display the fonts
listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=50, height=20)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Configure the scrollbar
scrollbar.config(command=listbox.yview)

# Insert fonts into the listbox
for f in available_fonts:
    listbox.insert(tk.END, f)

# Run the Tkinter main loop
root.mainloop()
