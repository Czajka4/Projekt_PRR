from mpi4py import MPI
from app_mpi_run import MonteCarlo


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

# Funcja wywyolywana przez kompilator mpi w cythonie
# Uruchamiane z app_mpi_run.py


def main():
    # Proces glowny
    if rank == 0:
        data = [MonteCarlo() for _ in range(nprocs)]
    else:
        data = None

    # Wywolywane przez procesy robocze:
    data = comm.scatter(data, root=0)

    results = []
    mc = data.monte_carlo()
    results.append(mc)
    results = comm.gather(results, root=0)

    if rank == 0:
        for r in results:
            print(r)


if __name__ == '__main__':
    main()
