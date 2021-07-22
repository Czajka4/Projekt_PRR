import time
import csv
from os import cpu_count
from datetime import datetime
import numpy as np
from threading import Thread
from queue import Queue

N = int(1e7)   # ilosc punktow
C = 16  # 16
csv_file = "wyniki.csv"


def save_result(t, x, y, f):
    run_date = datetime.today().strftime("%m/%d %H:%M:%S")

    # ['Plik', 'Datat', 'Czas Wyk.', 'Liczba pkt.', 'Proc/Thrds', 'x1', 'x2', 'f(x1,x2)']
    csv_row = ['Threads', run_date, t, '{:.1e}'.format(N), C,
               '{:.8f}'.format(x), '{:.8f}'.format(y), '{:.10f}'.format(f)]
    try:
        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(csv_row)
    except IOError:
        print("I/O error")


def elipse(x):
    return 3 * np.sqrt(1 - ((x - 2) ** 2) / 4) + 1


def func(x1, x2):
    return np.sin(2*x2) + (0.1 * (x1**2)) + np.cos(x1*x2)


def monte_carlo(reults_queue):
    x1_values = np.random.default_rng().uniform(0, 2, (1, N))
    x2_values = np.random.default_rng().uniform(1, elipse(x1_values), (1, N))

    f_values = func(x1_values, x2_values)
    min_index = f_values.argmin()

    x1_min, x2_min, f_min = x1_values[0][min_index], x2_values[0][min_index], f_values[0][min_index]

    # print('Wynik: min f(x1 = {:.8f} , x2 = {:.8f}) = {:.12f}'.format(x1_min, x2_min, f_min))
    reults_queue.put(np.array([x1_min, x2_min, f_min]))     # Wrzucamy wynik na kolejke
    reults_queue.task_done()


def main():
    start = time.perf_counter()
    x1_, x2_, f_ = np.array([]), np.array([]), np.array([])

    q = Queue(maxsize=0)
    threads = []

    # Tworzenie watkow
    for _ in range(C):
        t = Thread(target=monte_carlo, args=(q,))
        t.start()
        threads.append(t)

    # łączenie wątków
    for t in threads:
        t.join()

    # łączenie wyników na kolejce
    q.join()

    # odczyt koejnych wyników z kolejki, koleność zapisu dowolna, szukamy minimum
    while not q.empty():
        r = q.get()
        x1_, x2_, f_ = np.append(x1_, r[0]), np.append(x2_, r[1]),  np.append(f_, r[2])

    minimmum = f_.argmin()
    x1_m, x2_m, f_m = x1_[minimmum], x2_[minimmum], f_[minimmum]

    stop = time.perf_counter()
    run_time = round(stop - start, 4)
    save_result(run_time, x1_m, x2_m, f_m)

    # print(f"CPU: {C}")
    # print(f'Czas wykonywania: {round(stop-start, 4)}')
    # print('Ilość punktów: {:.1e}'.format(N))


if __name__ == '__main__':
    main()
