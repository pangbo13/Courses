#include <stdio.h>
#include <stdlib.h>

#define N 1024

double A[N][N][N];

void init_array()
{
    int i, j, k;
    for (k=0; k<N; k++) {
        for (j=0; j<N; j++) {
            for (i=0; i<N; i++) {
                A[k][j][i] = (1+(i*j+k)%1024)/3.0;
            }
        }
    }
}

void print_array()
{
    int i, j, k;

    for (k=0; k<N; k++) {
        for (j=0; j<N; j++) {
            for (i=0; i<N; i++) {
                fprintf(stderr, "%lf ", A[k][j][i]);
            }
            fprintf(stderr, "\n");
        }
        fprintf(stderr, "\n");
    }
}

int main()
{
    int i, j, k;

    init_array();
    // print_array();
#pragma scop
    for (k = 0; k < N; k++) {
        for (j = 0; j < N; j++) {
            for (i = 1; i < N; i++) {
                A[k][j][i] = A[k][j][i] * 0.4 - A[k][j][i-1] * 0.6;
            }
        }
    }

    for (k = 0; k < N; k++) {
        for (i = 0; i < N; i++) {
            for (j = 1; j < N; j++) {
                A[k][j][i] = A[k][j][i] * 0.5 - A[k][j-1][i] * 0.5;
            }
        }
    }

    for (j = 0; j < N; j++) {
        for (i = 0; i < N; i++) {
            for (k = 1; k < N; k++) {
                A[k][j][i] = A[k][j][i] * 0.6 - A[k-1][j][i] * 0.4;
            }
        }
    }
#pragma endscop

    print_array();

    return 0;
}
