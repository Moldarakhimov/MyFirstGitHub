# Программа анализа  .csv файла
import tkinter as tk
from tkinter.scrolledtext import ScrolledText as st
from tkinter import filedialog as fd
import os
import pandas as pd

# Создание главного окна
window = tk.Tk()
window.geometry("550x600")
window.title("Программа анализа .csv файлов")

# Создание меток вывода
label_00 = tk.Label(text = "Файл:")
label_00.grid(row=0, column=0, padx=10, pady=10, sticky="e")
label_01 = tk.Label(text = "")
label_01.grid(row=0, column=1, sticky="w")

label_02 = tk.Label(text = "Столбцов:")
label_02.grid(row=1, column=0, padx=10, pady=10, sticky="e")
label_03 = tk.Label(text = "")
label_03.grid(row=1, column=1, sticky="w")

label_04 = tk.Label(text = "Name column:")
label_04.grid(row=2, column=0, padx=10, pady=10, sticky="e")
label_05 = tk.Label(text = "")
label_05.grid(row=2, column=1, sticky="w")

label_06 = tk.Label(text = "Email:")
label_06.grid(row=3, column=0, padx=10, pady=10, sticky="e")
label_07 = tk.Label(text = "")
label_07.grid(row=3, column=1, sticky="w")

label_08 = tk.Label(text = "Phone:")
label_08.grid(row=4, column=0, padx=10, pady=10, sticky="e")
label_09 = tk.Label(text = "")
label_09.grid(row=4, column=1, sticky="w")

# Создание текстового вывода с прокруткой
output_text = st(height = 20, width = 48)
output_text.grid(row=5, column=1, padx=10, pady=10, sticky="W"+"E")
       
# Функция для определения заголовки столбцов по их содержимому
def detect_headers(column):
    if any('@' in str(value) for value in column):
        return 'email'
    elif any(not any(char in ('.', '/') for char in str(value)) and str(value).count(char) > 6 and char in '0123456789+-' for value in column for char in '0123456789+-'): 
        return 'phone'
    else:
        return ''

# Функция для анализа столбцов
def analyze_columns(df):
    headers = []
    for col_number, column in enumerate(df.columns):
        header = detect_headers(df[column])
        headers.append((col_number, header))
    return headers
    
# Функция для поиска столбцов email по содержимому
def find_email(df):
    # Определить тип заголовка (например, 'phone') на основе данных в первой строке
    header_type = analyze_columns(df)
    email_index = next((header[0] for header in header_type if header[1] == 'email'), None)
    # Если тип заголовка определен, подсчитать количество строк с данным типом
    if email_index is not None:
        header_row = df.iloc[:, email_index]
        return header_row[0:].notna().sum()
    else:
        return 0

# Функция для поиска столбцов phone по содержимому
def find_phone(df):
    # Определить тип заголовка на основе данных
    header_type = analyze_columns(df)
    phone_index = next((header[0] for header in header_type if header[1] == 'phone'), None)
    # Если тип заголовка определен, подсчитать количество строк с данным типом
    if phone_index is not None:
        header_row = df.iloc[:, phone_index]
        return header_row[0:].notna().sum()
    else:
        return 0

#выборка столбца в список
def get_column(df, column_ix):
    cnt_rows = df.shape[0]
    lst = []
    for i in range(cnt_rows):
        lst.append(df.iat[i,column_ix])
    return lst
    
# Если в этом поле имя, пусть вернет True    
def meet_name(field):
    checkfor = ['Вера', 'Анатолий', 'Мария', 'Алексей', 'Валерия', 'Наталья', 'Оксана', 'Галина', 'Марина']
    for s in checkfor:
        if s in str(field): # Нашлось!
            return True
    # Ничего не совпало
    return False

# Если в этом списке многие элементы содержат имя, пусть вернет True    
def list_meet_name(fields_list):
    counter_total = 0
    counter_meet = 0
    for list_item in fields_list:
        counter_total += 1
        if meet_name(list_item):
            counter_meet += 1
    # Конец подсчета
    ratio = counter_meet / counter_total
    if ratio > 0:
        return True, ratio
    # Не набралось нужного количества совпадений
    return False, ratio

# Если в этом поле Фамилия по окончаниям, пусть вернет True    
def meet_last_name(field):
    checkfor = ['ов', 'ова']
    field_str = str(field)
    for s in checkfor:
        if str(field).endswith(s): # Нашлось!
            return True
    # Ничего не совпало
    return False

# Если в этом списке многие элементы содержат фамилия, пусть вернет True    
def list_meet_last_name(fields_list):
    counter_total = 0
    counter_meet = 0
    for list_item in fields_list:
        counter_total += 1
        if meet_last_name(list_item):
            counter_meet += 1
    # Конец подсчета
    ratio = counter_meet / counter_total
    if ratio > 0:
        return True, ratio
    # Не набралось нужного количества совпадений
    return False, ratio
 
# Пройти все столбцы    
def check_all_columns(df):
    columns_cnt = df.shape[1]
    for i in range(columns_cnt): # От 0 до columns_cnt-1
        lst = get_column(df, i)
        
        # Первый критерий
        result1 = list_meet_name(lst)
        if result1[0]:
            output_text.insert(tk.END, "В столбце " + str(i+1)
                + " предположительно содержится имя." + os.linesep)
            output_text.insert(tk.END, "Процент совпадений " + "{:.2f}".format(result1[1]*100)
                + "%." + os.linesep + os.linesep)
            continue # Все нашли, можно идти к следующему столбцу 
        
        # Второй критерий
        result2 = list_meet_last_name(lst)
        if result2[0]:
            output_text.insert(tk.END, "В столбце " + str(i+1)
                + " предположительно содержится фамилия." + os.linesep)
            output_text.insert(tk.END, "Процент совпадений " + "{:.2f}".format(result2[1]*100)
                + "%." + os.linesep + os.linesep)
            continue # Все нашли, можно идти к следующему столбцу
        
        # Соответствия критериям не найдено
        output_text.insert(tk.END, "Предположений для столбца " + str(i+1)
            + " не найдено." + os.linesep + os.linesep)
                                
# Диалог открытия файла
def do_dialog():
    name= fd.askopenfilename()
    return name  
   
# Обработка csv файла при помощи pandas
def pandas_read_csv(file_name):
    df = pd.read_csv(file_name, sep=';')
       
    cnt_columns = df.shape[1]
    label_03['text'] = cnt_columns 
    
    # Вывод имен столбцов
    column_names = [f"Столбец {i + 1}" for i in range(cnt_columns)]
    label_05['text'] = ", ".join(column_names)
    
    # Расчет кол-ва строк со знаком @ в столбце email
    headers = find_email(df)
    if headers:
        label_07['text'] = f"{headers} строк удовлетворяющих критерию"
    else:
        label_07['text'] = "Список не найден с символом @."
               
    # Расчет кол-ва строк со знаком +/-и цифрами в столбце phone
    headers = find_phone(df)
    if headers:
        label_09['text'] = f"{headers} строк удовлетворяющих критерию"
    else:
        label_09['text'] = "Список не найден с номерами."

    return df
    
# Обработчик нажатия кнопки
def process_button():
    file_name = do_dialog()
    label_01['text'] = file_name
    df = pandas_read_csv(file_name)
    
    headers = analyze_columns(df)
    for col_number, header in headers:
        output_text.insert(tk.END, f"Столбец {col_number + 1}: {header}\n")
    
    check_all_columns(df)
            
# Создание кнопки
button=tk.Button(window, text="Прочитать файл", font=("Arial", 10, "bold"), bg='#ff0000', command=process_button)
button.grid(row=6, column=1)

# Запуск цикла mainloop
window.mainloop()
