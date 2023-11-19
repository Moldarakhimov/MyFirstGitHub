# Программа анализа  .csv файла
import tkinter as tk
from tkinter.scrolledtext import ScrolledText as st
from tkinter import filedialog as fd
import pandas as pd

# Создание главного окна
window = tk.Tk()
window.geometry("550x550")
window.title("Программа анализа .csv файлов")

# Создание меток вывода
label_00 = tk.Label(text = "Файл:")
label_00.grid(row=0, column=0, padx=10, pady=10, sticky="e")

label_01 = tk.Label(text = "")
label_01.grid(row=0, column=1, sticky="w")

label_08 = tk.Label(text = "Столбцов:")
label_08.grid(row=1, column=0, padx=10, pady=10, sticky="e")
label_09 = tk.Label(text = "")
label_09.grid(row=1, column=1, sticky="w")

label_10 = tk.Label(text = "Email:")
label_10.grid(row=2, column=0, padx=10, pady=10, sticky="e")
label_11 = tk.Label(text = "")
label_11.grid(row=2, column=1, sticky="w")

label_20 = tk.Label(text = "Телефон:")
label_20.grid(row=2, column=1, padx=10, pady=10, sticky="W"+"E")
label_21 = tk.Label(text = "")
label_21.grid(row=2, column=2, sticky="w")

# Создание текстового вывода с прокруткой
output_text = st(height = 22, width = 50)
output_text.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Диалог открытия файла
def do_dialog():
    name= fd.askopenfilename()
    return name
    
# Обработка csv файла при помощи pandas
def pandas_read_csv(file_name):
    df = pd.read_csv(file_name, header=None, sep=';')
    cnt_columns = df.shape[1]
    label_09['text'] = cnt_columns
    return df  
  
# Обработчик нажатия кнопки
def process_button():
    file_name = do_dialog()
    label_01['text'] = file_name
    pandas_read_csv(file_name)

# Создание кнопки
button=tk.Button(window, text="Прочитать файл", font=("Arial", 10, "bold"), bg='#ff0000', command=process_button)
button.grid(row=4, column=1)

# Запуск цикла mainloop
window.mainloop()
