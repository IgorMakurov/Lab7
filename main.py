#Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию с использованием графического интерфейса.
#Допускается использовать любую графическую библиотеку питона. Рекомендуется использовать внутреннюю библиотеку питона  tkinter.

import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import itertools

# Константы
NUM_STATIONS = 8
NUM_SHIFTS = 3
TOTAL_WORKERS = 24
NUM_WOMEN = 16
NUM_MEN = 8
POWER_STATIONS = [2, 5]  # Индексы станций, требующих мужчин (нумерация с 1)

#Проверяет мужчин на силовых станциях и чтобы женщины не повторялись
def is_valid_schedule_advanced(schedule):
    # Проверка наличия мужчин на силовых станциях
    for shift_schedule in schedule:
        for station_index in POWER_STATIONS:
          station = station_index - 1
          if shift_schedule[station] == 0:
              pass
          else:
              return False
    # Проверка, что каждая женщина работает только в одну смену
    women_shifts = [None] * NUM_WOMEN  # Для каждой женщины записываем номер ее смены
    for shift_index, shift_schedule in enumerate(schedule):
        for station_index, worker_type in enumerate(shift_schedule):
            if worker_type == 1:  # Если на позиции женщина
                woman_id = shift_index * NUM_STATIONS + station_index  # Уникальный ID для каждой женщины
                if women_shifts[woman_id % NUM_WOMEN] is None:
                    women_shifts[woman_id % NUM_WOMEN] = shift_index
                elif women_shifts[woman_id % NUM_WOMEN] != shift_index:
                    return False  # Женщина работает в более чем одной смене
    return True

#Возвращает расписание в виде строки.
def print_schedule(schedule):
    schedule_str = ""
    for shift, shift_schedule in enumerate(schedule, 1):
        schedule_str += f"Смена {shift}: "
        for station, worker_type in enumerate(shift_schedule, 1):
            schedule_str += f"Ст{station}: {'М' if worker_type == 0 else 'Ж'} "
        schedule_str += "\n"
    return schedule_str

#Генерирует расписания с учетом ограничений и выводит по мере формирования в текстовое поле.
def generate_schedules_advanced(output_text):
    output_text.insert(tk.END, "Генерация расписаний с ограничением: Каждая женщина может работать только в одной смене в день:\n\n")
    schedules_count = 0
    all_shift_options = list(generate_shift_options())

    for schedule in itertools.product(all_shift_options, repeat=NUM_SHIFTS):
        if is_valid_schedule_advanced(schedule):
            schedules_count += 1
            output_text.insert(tk.END, print_schedule(schedule))
            output_text.update()
    output_text.insert(tk.END, f"\nВсего допустимых расписаний: {schedules_count}\n")
    return schedules_count

#Генерирует варианты расписания на одну смену.
def generate_shift_options():
  for p0 in range(2):
    for p1 in range(2):
      for p2 in range(2):
        for p3 in range(2):
          for p4 in range(2):
            for p5 in range(2):
              for p6 in range(2):
                for p7 in range(2):
                  yield [p0, p1, p2, p3, p4, p5, p6, p7]
                  
#Запускает генератор и измеряет время выполнения.
def run_generator(output_text, progress_bar):
    start_time = time.time()
    count = generate_schedules_advanced(output_text)
    end_time = time.time()
    execution_time = end_time - start_time
    output_text.insert(tk.END, f"Время выполнения: {execution_time:.4f} секунд\n")
    progress_bar['value'] = 100

#Запускает генерацию расписаний в отдельном потоке.
def start_calculation(output_text, progress_bar):
    progress_bar['value'] = 0
    output_text.delete("1.0", tk.END)
    
    # Запускает в отдельном потоке
    root.after(100, lambda: run_generator(output_text, progress_bar))
    progress_bar.start(10) # Запускает анимацию прогресса

# Создание основного окна
root = tk.Tk()
root.title("Генератор расписаний")
root.geometry("800x600")


# Создание текстового поля для вывода расписаний
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Создание прогресс-бара
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
progress_bar.pack(pady=10)

# Создание кнопки для запуска генерации
start_button = tk.Button(root, text="Сгенерировать расписания", 
                        command=lambda: start_calculation(output_text, progress_bar))
start_button.pack(pady=10)

root.mainloop()