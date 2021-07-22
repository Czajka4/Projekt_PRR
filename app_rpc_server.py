import numpy as np
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer


class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def elipse(x):
    return 3 * np.sqrt(1 - ((x - 2) ** 2) / 4) + 1


def func(x1, x2):
    return np.sin(2*x2) + (0.1 * (x1**2)) + np.cos(x1*x2)


def monte_carlo(N):
    x1_values = np.random.default_rng().uniform(0, 2, (1, N))
    x2_values = np.random.default_rng().uniform(1, elipse(x1_values), (1, N))

    f_values = func(x1_values, x2_values)
    min_index = f_values.argmin()

    x1_min, x2_min, f_min = x1_values[0][min_index], x2_values[0][min_index], f_values[0][min_index]
    #print('Wynik: min f(x1 = {:.8f} , x2 = {:.8f}) = {:.12f}'.format(x1_min, x2_min, f_min))

    return f"{x1_min};{x2_min};{f_min}"


# Uruchomienie serwera
# SimpleThreadedXMLRPCServer - wersja serwera obsługująca wątki
def main():
    server = SimpleThreadedXMLRPCServer(("localhost", 3000))
    server.register_function(monte_carlo)

    try:
        print('Serwer działa...')
        server.serve_forever()
    except KeyboardInterrupt:
        print("Zamykanie")


if __name__ == '__main__':
    main()
