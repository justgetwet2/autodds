
import pickle
import sys
import tkinter as tk
# from tkinter import ttk

args = sys.argv 

filepath = args[1]
with open(filepath, mode="rb") as f:
    races = pickle.load(f)

root = tk.Tk()

root.title("test")
root.geometry("800x400+50+50")

CheckBox = tk.Checkbutton(text=u"test")
# CheckBox.pack()

def tes(r):
    print(r)

for r in range(1, len(races)+1):
    Button = tk.Button(text=f"{r}", command=lambda: tes(r))
    Button.pack(side="left", anchor=tk.NW)

root.mainloop()