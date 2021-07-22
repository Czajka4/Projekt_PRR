import numpy as np
import time
from datetime import datetime
from xmlrpc.client import ServerProxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

N = int(1e7)   # ilosc punktow
C = 16
csv_file = "wyniki.csv"


def save_result(t, x, y, f):
    run_date = datetime.today().strftime("%m/%d %H:%M:%S")

    # ['Plik', 'Datat', 'Czas Wyk.', 'Liczba pkt.', 'Proc/Thrds', 'x1', 'x2', 'f(x1,x2)']
    csv_row = ['xml_RPC', run_date, t, '{:.1e}'.format(N), C,
               '{:.8f}'.format(x), '{:.8f}'.format(y), '{:.10f}'.format(f)]
    try:
        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(csv_row)
    except IOError:
        print("I/O error")


# Adres odpytywania
def submit_server():
    server = ServerProxy("http://localhost:3000/", allow_none=True)
    return server.monte_carlo(N)


def main():
    start = time.perf_counter()
    x1_, x2_, f_ = np.array([]), np.array([]), np.array([])

    # ThreadPoolExecutor wbudowane api do pythonowych wątków
    # Wysyłamy zapytania w wielu wątkach
    with ThreadPoolExecutor() as executor:
        funtion_result = {executor.submit(submit_server) for _ in range(C)}
        for future in as_completed(funtion_result):
            r = future.result()    # blokuje aż wartość będzie gotowa
            r = r.split(";", -1)
            x1_, x2_, f_ = np.append(x1_, float(r[0])), np.append(x2_, float(r[1])), np.append(f_, float(r[2]))

    minimmum = f_.argmin()
    x1_m, x2_m, f_m = x1_[minimmum], x2_[minimmum], f_[minimmum]

    stop = time.perf_counter()
    run_time = round(stop - start, 4)
    save_result(run_time, x1_m, x2_m, f_m)

    # print(f'Czas wykonywania: {round(stop - start, 4)}')
    # print('Ilość punktów: {:.1e}'.format(N))


if __name__ == '__main__':
    main()
