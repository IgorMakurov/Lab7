#Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию с использованием графического интерфейса.
#Допускается использовать любую графическую библиотеку питона. Рекомендуется использовать внутреннюю библиотеку питона  tkinter.

import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import itertools

# Функции для логики расписаний (без изменений из предыдущего ответа)
def check_shift_limits(schedule, num_men, num_women):
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

def calculate_efficiency(schedule):
    efficiency = 0
    for shift_workers in schedule:
        for worker in shift_workers:
            if worker[0] == 'M':
                efficiency += 100
            elif worker[0] == 'W':
                efficiency += 75
    return efficiency

def generate_schedules_algorithmic(num_men, num_women, num_places, num_shifts, max_schedules=None):
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
        if valid_schedule and check_shift_limits(shift_combination, num_men, num_women):
            efficiency = calculate_efficiency(shift_combination)
            all_schedules.append(shift_combination)
            if efficiency > best_efficiency:
                best_schedule = shift_combination
                best_efficiency = efficiency
            schedule_count += 1
            if max_schedules and schedule_count >= max_schedules:
                  break

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return elapsed_time, all_schedules, best_schedule, schedule_count, best_efficiency

def generate_schedules_pythonic(num_men, num_women, num_places, num_shifts, max_schedules=None):
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
        
        if valid_schedule and check_shift_limits(shift_combination, num_men, num_women):
            efficiency = calculate_efficiency(shift_combination)
            all_schedules.append(shift_combination)
            if efficiency > best_efficiency:
                best_schedule = shift_combination
                best_efficiency = efficiency
            schedule_count += 1
            if max_schedules and schedule_count >= max_schedules:
                break

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return elapsed_time, all_schedules, best_schedule, schedule_count, best_efficiency

# Функция для запуска генерации расписаний
def run_schedules(method, text_widget, num_men, num_women, num_places, num_shifts, max_schedules):
    text_widget.delete(1.0, tk.END)
    
    if method == "algorithmic":
        text_widget.insert(tk.END, "Алгоритмический способ:\n")
        elapsed_time, all_schedules, best_schedule, schedule_count, best_efficiency = generate_schedules_algorithmic(num_men, num_women, num_places, num_shifts, max_schedules)
    elif method == "pythonic":
        text_widget.insert(tk.END, "С помощью функций Питона:\n")
        elapsed_time, all_schedules, best_schedule, schedule_count, best_efficiency = generate_schedules_pythonic(num_men, num_women, num_places, num_shifts, max_schedules)
    else:
        text_widget.insert(tk.END, "Неверный метод.\n")
        return
    
    text_widget.insert(tk.END, "\nВсе расписания:\n")
    for i, schedule in enumerate(all_schedules):
        text_widget.insert(tk.END, f"\nРасписание {i+1}:\n")
        for shift_index, workers_perm in enumerate(schedule):
            text_widget.insert(tk.END, f"  Смена {shift_index+1}: ")
            for j, worker in enumerate(workers_perm):
                text_widget.insert(tk.END, f"Место {j+1}: {worker}  ")
            text_widget.insert(tk.END, "\n")

    text_widget.insert(tk.END, f"\nВсего расписаний: {schedule_count}\n")
    text_widget.insert(tk.END, f"Время выполнения: {elapsed_time:.4f} секунд\n")
    text_widget.insert(tk.END, f"Наилучшая эффективность: {best_efficiency}\n")
    
    if best_schedule:
        text_widget.insert(tk.END, "\nНаилучшее расписание:\n")
        for shift_index, workers_perm in enumerate(best_schedule):
           text_widget.insert(tk.END, f"  Смена {shift_index+1}: ")
           for j, worker in enumerate(workers_perm):
                text_widget.insert(tk.END, f"Место {j+1}: {worker}  ")
           text_widget.insert(tk.END, "\n")
    else:
        text_widget.insert(tk.END, "\nНе найдено ни одного корректного расписания.\n")
    text_widget.see(tk.END) # Scroll to end

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Генератор расписаний конвейера")

    # Input Frame
    input_frame = ttk.LabelFrame(root, text="Параметры")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    ttk.Label(input_frame, text="Мужчин:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    num_men_entry = ttk.Entry(input_frame)
    num_men_entry.insert(0, "8")
    num_men_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(input_frame, text="Женщин:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    num_women_entry = ttk.Entry(input_frame)
    num_women_entry.insert(0, "16")
    num_women_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(input_frame, text="Мест:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    num_places_entry = ttk.Entry(input_frame)
    num_places_entry.insert(0, "4")
    num_places_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(input_frame, text="Смен:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    num_shifts_entry = ttk.Entry(input_frame)
    num_shifts_entry.insert(0, "3")
    num_shifts_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    
    ttk.Label(input_frame, text="Макс. расписаний:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    max_schedules_entry = ttk.Entry(input_frame)
    max_schedules_entry.insert(0, "1000")
    max_schedules_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # Output Frame
    output_frame = ttk.LabelFrame(root, text="Результаты")
    output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    text_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=25)
    text_output.pack(padx=5, pady=5)

    # Buttons
    button_frame = ttk.Frame(root)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10)
    
    def run_alg_wrapper():
      num_men = int(num_men_entry.get())
      num_women = int(num_women_entry.get())
      num_places = int(num_places_entry.get())
      num_shifts = int(num_shifts_entry.get())
      max_schedules = int(max_schedules_entry.get())
      run_schedules("algorithmic", text_output, num_men, num_women, num_places, num_shifts, max_schedules)
    
    def run_py_wrapper():
      num_men = int(num_men_entry.get())
      num_women = int(num_women_entry.get())
      num_places = int(num_places_entry.get())
      num_shifts = int(num_shifts_entry.get())
      max_schedules = int(max_schedules_entry.get())
      run_schedules("pythonic", text_output, num_men, num_women, num_places, num_shifts, max_schedules)

    ttk.Button(button_frame, text="Алгоритмический", command=run_alg_wrapper).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="С помощью функций Питона", command=run_py_wrapper).grid(row=0, column=1, padx=5)
    
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
