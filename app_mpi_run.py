import subprocess
import numpy as np
from datetime import datetime
import csv
import time
import re

N = 1e7
C = 16
csv_file = "wyniki.csv"


def func(x1, x2):
    return np.sin(2 * x2) + (0.1 * (x1 ** 2)) + np.cos(x1 * x2)


def elipse(x):
    return 3 * np.sqrt(1 - ((x - 2) ** 2) / 4) + 1


# Nieprofesjonalna obrobka wyniku z pliku app_mpi
def get_result(result):
    x1_, x2_, f_ = np.array([]), np.array([]), np.array([])

    rr = str(result)
    rr = rr.split("]", -1)

    start = 'x'
    stop = 'y'

    for s in rr:
        x = s[s.find(start) + len(start):s.rfind(stop)]
        x = x.split(";", -1)
        if len(x) == 3:
            x1_, x2_, f_ = np.append(x1_, float(x[0])), np.append(x2_, float(x[1])), np.append(f_, float(x[2]))

    minimmum = f_.argmin()

    return [x1_[minimmum], x2_[minimmum], f_[minimmum]]


def save_result(t, r):
    run_date = datetime.today().strftime("%m/%d %H:%M:%S")
    x, y, f = r[0], r[1], r[2]

    # ['Plik', 'Datat', 'Czas Wyk.', 'Liczba pkt.', 'Proc/Thrds', 'x1', 'x2', 'f(x1,x2)']
    csv_row = ['MPI', run_date, t, '{:.1e}'.format(N), C,
               '{:.8f}'.format(x), '{:.8f}'.format(y), '{:.10f}'.format(f)]
    try:
        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(csv_row)
    except IOError:
        print("I/O error")


# Klasa importowana w pliku app_mpi, wygodne przenoszenie zmiennych
class MonteCarlo():
    def __init__(self):
        self.points = int(N)

    def monte_carlo(self):
        x1_values = np.random.default_rng().uniform(0, 2, (1, self.points))
        x2_values = np.random.default_rng().uniform(1, elipse(x1_values), (1, self.points))

        f_values = func(x1_values, x2_values)
        min_index = f_values.argmin()

        x1_min, x2_min, f_min = x1_values[0][min_index], x2_values[0][min_index], f_values[0][min_index]

        # print('Wynik: min f(x1 = {:.8f} , x2 = {:.8f}) = {:.12f}'.format(x1_min, x2_min, f_min))
        return 'x{:.8f};{:.8f};{:.12f}y'.format(x1_min, x2_min, f_min)


# Wywolanie komendy w mpiexec w konsoli i odczytanie wyniku z stdout
def main():
    start = time.perf_counter()
    command = ['mpiexec', '-np',  str(C), 'python', r'E:\Studia\Semestr_2\PRR\projekt_prr\app_mpi.py']

    result = subprocess.run(command, stdout=subprocess.PIPE)
    result = get_result(result.stdout)

    stop = time.perf_counter()
    run_time = round(stop - start, 4)

    save_result(run_time, result)

    # print(f'Czas wykonywania: {round(stop - start, 4)}')
    # print('Ilość punktów: {:.1e}'.format(N))

if __name__ == '__main__':
    main()