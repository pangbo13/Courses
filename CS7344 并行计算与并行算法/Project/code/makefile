adi:
	gcc 1_adi.c -o 1_adi
	mpicc 1_adi_mpi.c -o 1_adi_mpi
floyd:
	gcc 3_floyd.c -o 3_floyd
	mpicc 3_floyd_mpi.c -o 3_floyd_mpi
all: adi floyd
clean:
	rm 1_adi 1_adi_mpi 3_floyd 3_floyd_mpi
run: all
	./1_adi
	mpirun -np 4 ./1_adi_mpi
	./3_floyd
	mpirun -np 4 ./3_floyd_mpi