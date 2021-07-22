import csv
import time
import numpy as np
from datetime import datetime


N = int(1e3)   # ilosc punktow
csv_file = "wyniki.csv"


def save_result(t, x, y, f):
    # Dopisz wynik do pliku csv
    run_date = datetime.today().strftime("%m/%d %H:%M:%S")

    # ['Plik', 'Datat', 'Czas Wyk.', 'Liczba pkt.', 'Proc/Thrds', 'x1', 'x2', 'f(x1,x2)']
    csv_row = ['Sekwencyjny', run_date, t, '{:.1e}'.format(N), 1,
               '{:.8f}'.format(x), '{:.8f}'.format(y), '{:.10f}'.format(f)]
    try:
        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(csv_row)
    except IOError:
        print("I/O error")


def ellipse(x):
    # Obliczenie krawedzi elipsy dla danego x
    return 3 * np.sqrt(1 - ((x - 2) ** 2) / 4) + 1


def func(x1, x2):
    # Obliczenie wartosci funkcji dla danych x1 i x2
    return np.sin(2*x2) + (0.1 * (x1**2)) + np.cos(x1*x2)


def main():
    # Glowna funckcja
    # N losowych (roz. jednost.) punktow z przedzialu 0-2
    # N punktow z przedzialu losowany x - krawedz elispy (y)
    x1_values = np.random.default_rng().uniform(0, 2, (1, N))
    x2_values = np.random.default_rng().uniform(1, ellipse(x1_values), (1, N))

    f_values = func(x1_values, x2_values)
    min_index = f_values.argmin()   # Znajdujemy indeks minimum

    return x1_values[0][min_index], x2_values[0][min_index], f_values[0][min_index]


if __name__ == '__main__':
    start = time.perf_counter()

    X1, X2, F_min = main()

    stop = time.perf_counter()
    run_time = round(stop - start, 4)   # Czas wykonywania main()

    save_result(run_time,  X1, X2, F_min)

    print(f'Czas wykonywania: {run_time}')
    print('Ilość punktów: {:.1e}'.format(N))
    print('Wynik: min f(x1 = {:.8f} , x2 = {:.8f}) = {:.12f}'.format(X1, X2, F_min))
