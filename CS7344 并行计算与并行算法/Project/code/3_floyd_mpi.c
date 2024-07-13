#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define BLOCK_LOW(id, p, n) ((id) * (n) / (p) )

#define BLOCK_HIGH(id, p, n) (BLOCK_LOW((id) + 1, p, n) - 1)

#define BLOCK_SIZE(id, p, n) (BLOCK_LOW((id) + 1, p, n) - BLOCK_LOW((id), p, n))

#define BLOCK_OWNER(index, p, n) (((p) * ((index) + 1) - 1) / (n))

#define min(a, b) ((a) < (b) ? (a) : (b))

#define N 1024

double A[N][N];
// double K[N];

void init_array()
{
    int i, j;

    srand(123);
    for(i= 0; i < N; i++) {
        for(j= 0; j < N; j++) {
            double ra = 1.0 + ((double)N * rand() / (RAND_MAX + 1.0));
            A[i][j] = ra;
        }
    }
    for(i= 0; i < N; i++) {
        A[i][i] = 0;
    }
}

void print_array()
{
    int i, j;

    for(i=0; i<N; i++) {
        for(j=0; j<N; j++) {
            fprintf(stderr, "%lf ", A[i][j]); 
        }
        fprintf(stderr, "\n");
    }
}

int main()
{
    init_array();

#pragma scop
    MPI_Init(NULL, NULL);
    int p, id;
    MPI_Comm_size(MPI_COMM_WORLD, &p);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);


    for(int k = 0; k < N; k++) {
        MPI_Bcast(A[k], N, MPI_DOUBLE, BLOCK_OWNER(k, p, N), MPI_COMM_WORLD);
        for(int i = BLOCK_LOW(id, p, N); i <= BLOCK_HIGH(id, p, N); i++) {
            for(int j = 0; j < N; j++) {
                A[i][j] = min(A[i][j], A[i][k] + A[k][j]);
            }
        }
    }
#pragma endscop
    if (id == 0) {
        int *disp = (int *)malloc(p * sizeof(int));
        int *count = (int *)malloc(p * sizeof(int));
        for(int i = 0; i < p; i++) {
            count[i] = BLOCK_SIZE(i, p, N) * N;
            disp[i] = BLOCK_LOW(i, p, N) * N;
        }
        MPI_Gatherv(NULL, 0, MPI_DOUBLE, A[BLOCK_LOW(id, p, N)], count, disp, MPI_DOUBLE, 0, MPI_COMM_WORLD);
        free(disp);
        free(count);
        print_array();
    } else{
        MPI_Gatherv(A[BLOCK_LOW(id, p, N)], BLOCK_SIZE(id, p, N) * N, MPI_DOUBLE, NULL, NULL, NULL, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    }
    MPI_Finalize();
    return 0;
}
