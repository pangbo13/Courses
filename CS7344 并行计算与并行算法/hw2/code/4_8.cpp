
#include <mpi.h>
#include <stdio.h>
#include <cmath>

bool isPrime(int num) {
    if (num <= 1) {
        return false;
    }
    for (int i = 2; i <= std::sqrt(num); i++) {
        if (num % i == 0) {
            return false;
        }
    }
    return true;
}

int main(int argc, char** argv) {
    int rank, size;
    int count = 0;
    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    int start = rank * (1000000 / size) + 1;
    int end = (rank + 1) * (1000000 / size) + 1;
    
    if (rank == size - 1) {
        end = 1000000;
    }
    
    for (int i = start; i < end; i += 2) {
        if (isPrime(i)) {
            if (isPrime(i + 2)) count++;
            else i += 2;
        }
    }
    
    int total_count;
    MPI_Reduce(&count, &total_count, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    
    if (rank == 0) {
        printf("Total count: %d\n", total_count);
    }
    
    MPI_Finalize();
    
    return 0;
}