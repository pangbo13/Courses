#include <stdio.h>
#include <stdlib.h>

#define min(a, b) ((a) < (b) ? (a) : (b))

#define N 1024

double A[N][N];

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
    for(int k = 0; k < N; k++) {
        for(int i = 0; i < N; i++) {
            for(int j = 0; j < N; j++) {
                A[i][j] = min(A[i][j], A[i][k] + A[k][j]);
            }
        }
    }
#pragma endscop

    print_array();

    return 0;
}
