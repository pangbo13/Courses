#include <mpi.h>
#include <math.h>
#include <stdio.h>

#define BLOCK_LOW(id, p, n) ((id) * (n) / (p) )

#define BLOCK_HIGH(id, p, n) (BLOCK_LOW((id) + 1, p, n) - 1)

#define BLOCK_SIZE(id, p, n) (BLOCK_LOW((id) + 1, p, n) - BLOCK_LOW((id), p, n))

#define BLOCK_OWNER(index, p, n) (((p) * ((index) + 1) - 1) / (n))

int main(int argc, char** argv)
{
    int id;
    int p;

    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &id);
    MPI_Comm_size(MPI_COMM_WORLD, &p);
    
    if (argc != 2) {
        if (id == 0)
            printf("Usage: %s N\n", argv[0]);
        MPI_Finalize();
        return 1;
    }
    const int N = atoi(argv[1]);

    int buffer_size = N * BLOCK_SIZE(id, p, N);
    int* buffer = new int[buffer_size];
    for (int i = 0; i < buffer_size; i++) buffer[i] = BLOCK_LOW(id, p, N) * N + i;

    for(int i = 0; i < p; i++) {
        MPI_Barrier(MPI_COMM_WORLD);
        if(id == i) {
            printf("id = %d, buffer = \n", id);
            for (int j = 0; j < buffer_size; j++) {
                printf("%d ", buffer[j]);
                if ((j + 1) % N == 0) printf("\n");
            }
            fflush(stdout);
        }
        MPI_Barrier(MPI_COMM_WORLD);
    }

    if (id == 0) {
        printf("==============\n");
        fflush(stdout);
    }

    if (id == 0) {
        int *matrix_buffer = new int[N * N];
        int *displs = new int[p];
        int *receive_counts = new int[p];
        for (int i = 0; i < p; i++) {
            displs[i] = BLOCK_LOW(i, p, N) * N;
            receive_counts[i] = BLOCK_SIZE(i, p, N) * N;
        }
        MPI_Gatherv(buffer, buffer_size, MPI_INT, matrix_buffer, receive_counts, displs, MPI_INT, 0, MPI_COMM_WORLD);
        for (int i = 0; i < N; i++) {
            for (int j = i + 1; j < N; j++) {
                int temp = matrix_buffer[i * N + j];
                matrix_buffer[i * N + j] = matrix_buffer[j * N + i];
                matrix_buffer[j * N + i] = temp;
            }
        }
        MPI_Scatterv(matrix_buffer, receive_counts, displs, MPI_INT, buffer, buffer_size, MPI_INT, 0, MPI_COMM_WORLD);
        delete[] matrix_buffer;
        delete[] displs;
        delete[] receive_counts;
    }else {
        MPI_Gatherv(buffer, buffer_size, MPI_INT, NULL, NULL, NULL, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Scatterv(NULL, NULL, NULL, MPI_INT, buffer, buffer_size, MPI_INT, 0, MPI_COMM_WORLD);
    }
    
    for(int i = 0; i < p; i++) {
        MPI_Barrier(MPI_COMM_WORLD);
        if(id == i) {
            printf("id = %d, buffer = \n", id);
            for (int j = 0; j < buffer_size; j++) {
                printf("%d ", buffer[j]);
                if ((j + 1) % N == 0) printf("\n");
            }
            fflush(stdout);
        }
        MPI_Barrier(MPI_COMM_WORLD);
    }

    delete[] buffer;
    MPI_Finalize();

    return 0;
}