def worker(task):
    a, b = task
    return a**2 + b**2
def func(x):
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    print(size, rank, x)
    return

def main(pool):
    import numpy as np

    x = np.linspace(0,1,pool.comm.size-1)
    results = pool.map(func, x)
    pool.close()

    print(results[:8])


if __name__ == "__main__":
    import sys
    from schwimmbad import MPIPool
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    pool = MPIPool(comm)

    if not pool.is_master():
        pool.wait()
        #sys.exit(0)
    else:
        main(pool)
    print(pool.comm.size)
    #main(pool)
    import numpy as np
    #pool.map(func,np.linspace(0,1,pool.comm.size))
    print("all is done.")
    #if (MPI.Is_initialized()):
    #    print("finalizing..")
    #    MPI.Finalize() 
