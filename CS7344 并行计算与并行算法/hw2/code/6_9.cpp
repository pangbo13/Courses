
#include <mpi.h>
#include <stdio.h>
#include <cmath>

void reduce(const int *sendbuf, int *recvbuf, int count, int root) {
    int rank, size;
    int *tempbuf = new int[count];
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    if(rank == root) {
        for (int i = 0; i < count; i++) {
            recvbuf[i] = 0;
        }
        for(int i = 0; i < size; i++) {
            if(i != root) {
                MPI_Recv(tempbuf, count, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                for (int j = 0; j < count; j++) {
                    recvbuf[j] += tempbuf[j];
                }
            } else {
                for (int j = 0; j < count; j++) {
                    recvbuf[j] += sendbuf[j];
                }
            }
        }
    } else {
        MPI_Send(sendbuf, count, MPI_INT, root, 0, MPI_COMM_WORLD);
    }
    delete[] tempbuf;
}

int main(int argc, char** argv) {
    int rank, size;
    const int buffer_size = 1000;
    double elapsed_time;
    int send[buffer_size];
    int sum[buffer_size] = {0};

    for (int i = 0; i < buffer_size; i++) {
        send[i] = i + 1;
    }

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    MPI_Barrier(MPI_COMM_WORLD);
    elapsed_time = -MPI_Wtime();

    for(int i = 0; i < 10000; i++) {
        reduce(send, sum, buffer_size, 0);
        // MPI_Reduce(send, sum, buffer_size, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    }

    if (rank == 0) {
        elapsed_time += MPI_Wtime();
        printf("Execution time: %8.6f\n", elapsed_time);
    }
    MPI_Finalize();
    
    return 0;
}