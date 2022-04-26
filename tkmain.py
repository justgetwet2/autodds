
import tkinter as tk
# from tkinter import ttk

root = tk.Tk()

root.title("test")
root.geometry("400x200+100+50")

CheckBox = tk.Checkbutton(text=u"test")
CheckBox.pack()

root.mainloop()