#Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию с использованием графического интерфейса.
#Допускается использовать любую графическую библиотеку питона. Рекомендуется использовать внутреннюю библиотеку питона  tkinter.

import time
import itertools
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, END, Y, X, BOTH, RIGHT, TOP, BOTTOM, LEFT, filedialog
from tkinter import messagebox
from collections import defaultdict

# Функции расчета и генерации расписаний, которые были предоставлены ранее
def check_shift_limits(schedule, num_men, num_women, num_places, num_shifts):
    workers = ['M' + str(i+1) for i in range(num_men)] + ['W' + str(i+1) for i in range(num_women)]
    for worker in workers:
      shift_count = 0
      for shift_workers in schedule:
          for place_worker in shift_workers:
            if place_worker == worker:
                shift_count+=1
      if worker[0] == 'M' and shift_count > 2:
        return False
      if worker[0] == 'W' and shift_count > 1:
        return False
    return True

def calculate_efficiency(schedule, num_men, num_women):
    efficiency = 0
    for shift_workers in schedule:
        for worker in shift_workers:
            if worker[0] == 'M':
                efficiency += 100
            elif worker[0] == 'W':
                efficiency += 75
    return efficiency

def generate_schedules_algorithmic(num_men, num_women, num_places, num_shifts, max_schedules=None):
    print("\nАлгоритмический способ:")
    start_time = time.time()

    men_places = [1, 2]
    workers = ['M' + str(i+1) for i in range(num_men)] + ['W' + str(i+1) for i in range(num_women)]
    schedule_count = 0
    all_schedules = []
    best_schedule = None
    best_efficiency = 0
    
    for shift_combination in itertools.product(itertools.permutations(workers, num_places), repeat=num_shifts):
        
        valid_schedule = True
        for shift_workers in shift_combination:
            for place in men_places:
                if shift_workers[place - 1][0] != 'M':
                    valid_schedule = False
                    break
            if not valid_schedule:
                break
        if valid_schedule and check_shift_limits(shift_combination, num_men, num_women, num_places, num_shifts):
            efficiency = calculate_efficiency(shift_combination, num_men, num_women)
            all_schedules.append(shift_combination)
            if efficiency > best_efficiency:
                best_schedule = shift_combination
                best_efficiency = efficiency
            schedule_count += 1
            if max_schedules and schedule_count >= max_schedules:
                  break

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nВсего расписаний (алгоритмический способ): {schedule_count}")
    print(f"Время выполнения (алгоритмический способ): {elapsed_time:.4f} секунд")
    print(f"Наилучшая эффективность (алгоритмический способ): {best_efficiency}")
    return elapsed_time, all_schedules, best_schedule


def generate_schedules_pythonic(num_men, num_women, num_places, num_shifts, max_schedules=None):
    print("\nС помощью функций Питона:")
    start_time = time.time()

    men_places = [1, 2]
    workers = ['M' + str(i+1) for i in range(num_men)] + ['W' + str(i+1) for i in range(num_women)]
    
    schedule_count = 0
    all_schedules = []
    best_schedule = None
    best_efficiency = 0

    for shift_combination in itertools.product(itertools.permutations(workers, num_places), repeat=num_shifts):
       
        valid_schedule = True
        for shift_workers in shift_combination:
            if not all(shift_workers[place-1][0] == 'M' for place in men_places):
                valid_schedule = False
                break
        
        if valid_schedule and check_shift_limits(shift_combination, num_men, num_women, num_places, num_shifts):
            efficiency = calculate_efficiency(shift_combination, num_men, num_women)
            all_schedules.append(shift_combination)
            if efficiency > best_efficiency:
                best_schedule = shift_combination
                best_efficiency = efficiency
            schedule_count += 1
            if max_schedules and schedule_count >= max_schedules:
                break

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nВсего расписаний (с помощью функций Питона): {schedule_count}")
    print(f"Время выполнения (с помощью функций Питона): {elapsed_time:.4f} секунд")
    print(f"Наилучшая эффективность (с помощью функций Питона): {best_efficiency}")
    return elapsed_time, all_schedules, best_schedule


def display_schedules(text_widget, schedules, method_name):
    text_widget.insert(END, f"\nВсе расписания ({method_name}):\n")
    for i, schedule in enumerate(schedules):
        text_widget.insert(END, f"\nРасписание {i+1}:\n")
        for shift_index, workers_perm in enumerate(schedule):
            text_widget.insert(END, f"  Смена {shift_index+1}: ")
            for j, worker in enumerate(workers_perm):
                text_widget.insert(END, f"Место {j+1}: {worker}  ")
            text_widget.insert(END, "\n")

def display_best_schedule(text_widget, schedule, method_name):
    if schedule:
        text_widget.insert(END, f"\nНаилучшее расписание ({method_name}):\n")
        for shift_index, workers_perm in enumerate(schedule):
            text_widget.insert(END, f"  Смена {shift_index+1}: ")
            for j, worker in enumerate(workers_perm):
                 text_widget.insert(END, f"Место {j+1}: {worker}  ")
            text_widget.insert(END, "\n")
    else:
         text_widget.insert(END, f"\nНе найдено ни одного корректного расписания ({method_name})\n")


def run_schedule_generation(text_widget, num_men, num_women, num_places, num_shifts, max_schedules):
    text_widget.delete(1.0, END)  # Очистка текстового виджета

    # Запуск алгоритмического способа
    start_time_alg = time.time()
    time_algorithmic, all_schedules_alg, best_schedule_alg = generate_schedules_algorithmic(num_men, num_women, num_places, num_shifts, max_schedules)
    end_time_alg = time.time()
    time_algorithmic = end_time_alg - start_time_alg
    
    display_schedules(text_widget, all_schedules_alg, "алгоритмический способ")
    display_best_schedule(text_widget, best_schedule_alg, "алгоритмический способ")

    # Запуск Pythonic способа
    start_time_py = time.time()
    time_pythonic, all_schedules_py, best_schedule_py = generate_schedules_pythonic(num_men, num_women, num_places, num_shifts, max_schedules)
    end_time_py = time.time()
    time_pythonic = end_time_py - start_time_py
    
    display_schedules(text_widget, all_schedules_py, "с помощью функций Питона")
    display_best_schedule(text_widget, best_schedule_py, "с помощью функций Питона")

    text_widget.insert(END, "\nСравнение времени выполнения:\n")
    text_widget.insert(END, f"Алгоритмическим способом: {time_algorithmic:.4f} секунд\n")
    text_widget.insert(END, f"с помощью функций Питона: {time_pythonic:.4f} секунд\n")
    if time_algorithmic < time_pythonic:
        text_widget.insert(END, f"Алгоритмический способ быстрее на {time_pythonic - time_algorithmic:.4f} секунд.\n")
    elif time_pythonic < time_algorithmic:
        text_widget.insert(END, f"Способ с помощью функций Питона быстрее на {time_algorithmic - time_pythonic:.4f} секунд.\n")
    else:
        text_widget.insert(END, f"Времена выполнения способов равны.\n")


def start_generation():
    try:
        num_men = int(entry_men.get())
        num_women = int(entry_women.get())
        num_places = int(entry_places.get())
        num_shifts = int(entry_shifts.get())
        max_schedules = int(entry_max_schedules.get())

        if num_men <= 0 or num_women <= 0 or num_places <= 0 or num_shifts <= 0 or max_schedules <= 0 :
            messagebox.showerror("Ошибка", "Все значения должны быть положительными целыми числами.")
            return
        if num_places < 2:
             messagebox.showerror("Ошибка", "Количество мест должно быть больше 1, так как как минимум 2 места для мужчин")
             return

        run_schedule_generation(text_output, num_men, num_women, num_places, num_shifts, max_schedules)
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите целые числа для всех полей.")

# Инициализация главного окна
root = Tk()
root.title("Генератор расписаний")

# Размещение элементов интерфейса
Label(root, text="Количество мужчин:").grid(row=0, column=0, sticky="e")
entry_men = Entry(root)
entry_men.grid(row=0, column=1, sticky="w")
entry_men.insert(0, "8")  # Значение по умолчанию

Label(root, text="Количество женщин:").grid(row=1, column=0, sticky="e")
entry_women = Entry(root)
entry_women.grid(row=1, column=1, sticky="w")
entry_women.insert(0, "16") # Значение по умолчанию

Label(root, text="Количество мест:").grid(row=2, column=0, sticky="e")
entry_places = Entry(root)
entry_places.grid(row=2, column=1, sticky="w")
entry_places.insert(0, "4") # Значение по умолчанию

Label(root, text="Количество смен:").grid(row=3, column=0, sticky="e")
entry_shifts = Entry(root)
entry_shifts.grid(row=3, column=1, sticky="w")
entry_shifts.insert(0, "3") # Значение по умолчанию

Label(root, text="Макс. расписаний:").grid(row=4, column=0, sticky="e")
entry_max_schedules = Entry(root)
entry_max_schedules.grid(row=4, column=1, sticky="w")
entry_max_schedules.insert(0, "1000")  # Значение по умолчанию


Button(root, text="Сгенерировать", command=start_generation).grid(row=5, column=0, columnspan=2, pady=10)

# Текстовый виджет для вывода результатов
text_output = Text(root, wrap="word", height=20)
text_output.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Полоса прокрутки
scrollbar = Scrollbar(root, command=text_output.yview)
scrollbar.grid(row=6, column=2, sticky="ns")
text_output.config(yscrollcommand=scrollbar.set)


# Настройка сетки для изменения размера
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Запуск GUI
root.mainloop()
