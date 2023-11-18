# Python калькулятор

import tkinter as tk

window=tk.Tk()
window.geometry("300x200")
window.title("Python калькулятор")

first = tk.Label(text = "Первое число")
first.grid(column=0, row=0, padx=10, pady=10)
second = tk.Label(text = "Второе число")
second.grid(column=0, row=1)

firstEntry = tk.Entry()
firstEntry.grid(column=1, row=0)
secondEntry = tk.Entry()
secondEntry.grid(column=1, row=1)

window.mainloop()

