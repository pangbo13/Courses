#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define N 1024
#define DIM_SIZE 2
#define MPI_SIZE 4
#define BLOCK_SIZE (N/DIM_SIZE)
#define BLOCK_LOW(i) ((i) * BLOCK_SIZE)
#define BLOCK_HIGH(i) (BLOCK_LOW(i+1) - 1)

double A[N][N][N];

int block_owner(int i,int j,int k){
    return ((k - i) % DIM_SIZE + DIM_SIZE) % DIM_SIZE * DIM_SIZE + ((j - i) % DIM_SIZE + DIM_SIZE) % DIM_SIZE;
}

void block_id(int id,int* i,int* j,int* k){
    int j0,k0;
    j0 = id % DIM_SIZE;
    k0 = id / DIM_SIZE;
    int delta = 0;
    if (*i != -1) {
        delta = *i;
    } else if (*j != -1) {
        delta = *j - j0;
    } else if (*k != -1)
    {
        delta = *k - k0;
    }
    *i = (delta % DIM_SIZE + DIM_SIZE) % DIM_SIZE;
    *j = ((j0 + delta) % DIM_SIZE + DIM_SIZE) % DIM_SIZE;
    *k = ((k0 + delta) % DIM_SIZE + DIM_SIZE) % DIM_SIZE;
}

void pack_array(double *buffer, int i0, int j0, int k0, int i1, int j1, int k1){
    int index = 0;
    for (int k = k0; k <= k1; k++){
        for (int j = j0; j <= j1; j++){
            for (int i = i0; i <= i1; i++){
                buffer[index++] = A[k][j][i];
            }
        }
    }
}

void unpack_array(double *buffer, int i0, int j0, int k0, int i1, int j1, int k1){
    int index = 0;
    for (int k = k0; k <= k1; k++){
        for (int j = j0; j <= j1; j++){
            for (int i = i0; i <= i1; i++){
                A[k][j][i] = buffer[index++];
            }
        }
    }
}

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
    int p, id;

    init_array();

    MPI_Init(NULL,NULL);
    MPI_Comm_size(MPI_COMM_WORLD,&p);
    MPI_Comm_rank(MPI_COMM_WORLD,&id);
    
    if(p != MPI_SIZE){
        if(id == 0){
            printf("The number of MPI processes must be %d\n",MPI_SIZE);
        }
        MPI_Finalize();
        return 1;
    }
    if(N % DIM_SIZE != 0 || DIM_SIZE * DIM_SIZE != MPI_SIZE){
        if(id == 0){
            printf("N must be divisible by DIM_SIZE and DIM_SIZE * DIM_SIZE must be equal to MPI_SIZE\n");
        }
        MPI_Finalize();
        return 1;
    }

    // if (id == 0) print_array();
#pragma scop
    int block_i,block_j,block_k;
    double *recv_buffer = (double *)malloc(sizeof(double) * BLOCK_SIZE * BLOCK_SIZE);
    double *send_buffer = (double *)malloc(sizeof(double) * BLOCK_SIZE * BLOCK_SIZE);
    MPI_Request request;
    // i
    for(block_i = 0; block_i < DIM_SIZE; block_i++){
        block_j = block_k = -1;
        block_id(id,&block_i,&block_j,&block_k);
        if (block_i != 0) {
            int source = block_owner(block_i - 1,block_j,block_k);
            MPI_Recv(recv_buffer,BLOCK_SIZE * BLOCK_SIZE,MPI_DOUBLE,source,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
            unpack_array(recv_buffer,BLOCK_LOW(block_i) - 1,BLOCK_LOW(block_j),BLOCK_LOW(block_k),BLOCK_LOW(block_i) - 1,BLOCK_HIGH(block_j),BLOCK_HIGH(block_k));
        }
        for (int i = BLOCK_LOW(block_i); i <= BLOCK_HIGH(block_i); i++)
        {
            if (i == 0) continue;
            for (int j = BLOCK_LOW(block_j); j <= BLOCK_HIGH(block_j); j++)
            {
                for (int k = BLOCK_LOW(block_k); k <= BLOCK_HIGH(block_k); k++)
                {
                    A[k][j][i] = A[k][j][i] * 0.4 - A[k][j][i-1] * 0.6;
                }
            }
        }
        if (block_i != DIM_SIZE - 1) {
            MPI_Barrier(MPI_COMM_WORLD);
            pack_array(send_buffer,BLOCK_HIGH(block_i),BLOCK_LOW(block_j),BLOCK_LOW(block_k),BLOCK_HIGH(block_i),BLOCK_HIGH(block_j),BLOCK_HIGH(block_k));
            int dest = block_owner(block_i + 1,block_j,block_k);
            MPI_Isend(send_buffer,BLOCK_SIZE * BLOCK_SIZE,MPI_DOUBLE,dest,0,MPI_COMM_WORLD,&request);
        }
    }
    MPI_Barrier(MPI_COMM_WORLD);
    
    // j
    for (block_j = 0; block_j < DIM_SIZE; block_j++){
        block_i = block_k = -1;
        block_id(id,&block_i,&block_j,&block_k);
        if (block_j != 0) {
            int source = block_owner(block_i,block_j - 1,block_k);
            MPI_Recv(recv_buffer,BLOCK_SIZE * BLOCK_SIZE,MPI_DOUBLE,source,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
            unpack_array(recv_buffer,BLOCK_LOW(block_i),BLOCK_LOW(block_j) - 1,BLOCK_LOW(block_k),BLOCK_HIGH(block_i),BLOCK_LOW(block_j) - 1,BLOCK_HIGH(block_k));
        }
        for (int j = BLOCK_LOW(block_j); j <= BLOCK_HIGH(block_j); j++)
        {
            if (j == 0) continue;
            for (int i = BLOCK_LOW(block_i); i <= BLOCK_HIGH(block_i); i++)
            {
                for (int k = BLOCK_LOW(block_k); k <= BLOCK_HIGH(block_k); k++)
                {
                    A[k][j][i] = A[k][j][i] * 0.5 - A[k][j-1][i] * 0.5;
                }
            }
        }
        if (block_j != DIM_SIZE - 1) {
            MPI_Barrier(MPI_COMM_WORLD);
            pack_array(send_buffer,BLOCK_LOW(block_i),BLOCK_HIGH(block_j),BLOCK_LOW(block_k),BLOCK_HIGH(block_i),BLOCK_HIGH(block_j),BLOCK_HIGH(block_k));
            int dest = block_owner(block_i,block_j + 1,block_k);
            MPI_Isend(send_buffer,BLOCK_SIZE * BLOCK_SIZE,MPI_DOUBLE,dest,0,MPI_COMM_WORLD,&request);
        }
    }
    MPI_Barrier(MPI_COMM_WORLD);

    // k
    for (block_k = 0; block_k < DIM_SIZE; block_k++){
        block_i = block_j = -1;
        block_id(id,&block_i,&block_j,&block_k);
        if (block_k != 0) {
            int source = block_owner(block_i,block_j,block_k - 1);
            MPI_Recv(recv_buffer,BLOCK_SIZE * BLOCK_SIZE,MPI_DOUBLE,source,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
            unpack_array(recv_buffer,BLOCK_LOW(block_i),BLOCK_LOW(block_j),BLOCK_LOW(block_k) - 1,BLOCK_HIGH(block_i),BLOCK_HIGH(block_j),BLOCK_LOW(block_k) - 1);
        }
        for (int k = BLOCK_LOW(block_k); k <= BLOCK_HIGH(block_k); k++)
        {
            if (k == 0) continue;
            for (int j = BLOCK_LOW(block_j); j <= BLOCK_HIGH(block_j); j++)
            {
                for (int i = BLOCK_LOW(block_i); i <= BLOCK_HIGH(block_i); i++)
                {
                    A[k][j][i] = A[k][j][i] * 0.6 - A[k-1][j][i] * 0.4;
                }
            }
        }
        if (block_k != DIM_SIZE - 1) {
            MPI_Barrier(MPI_COMM_WORLD);
            pack_array(send_buffer,BLOCK_LOW(block_i),BLOCK_LOW(block_j),BLOCK_HIGH(block_k),BLOCK_HIGH(block_i),BLOCK_HIGH(block_j),BLOCK_HIGH(block_k));
            int dest = block_owner(block_i,block_j,block_k + 1);
            MPI_Isend(send_buffer,BLOCK_SIZE * BLOCK_SIZE,MPI_DOUBLE,dest,0,MPI_COMM_WORLD,&request);
        }
    }
    MPI_Barrier(MPI_COMM_WORLD);
    free(recv_buffer);
    free(send_buffer);

    // gather data to root
    if(id == 0){
        double *buffer = (double *)malloc(sizeof(double) * BLOCK_SIZE * BLOCK_SIZE * BLOCK_SIZE);
        for (int source = 1; source < p; source++)
        {
            for(block_i = 0; block_i < DIM_SIZE; block_i++){
                block_j = block_k = -1;
                block_id(source,&block_i,&block_j,&block_k);
                MPI_Recv(buffer,BLOCK_SIZE * BLOCK_SIZE * BLOCK_SIZE,MPI_DOUBLE,source,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
                unpack_array(buffer,BLOCK_LOW(block_i),BLOCK_LOW(block_j),BLOCK_LOW(block_k),BLOCK_HIGH(block_i),BLOCK_HIGH(block_j),BLOCK_HIGH(block_k));
            }
        }
        free(buffer);
    } else{
        double *buffer = (double *)malloc(sizeof(double) * BLOCK_SIZE * BLOCK_SIZE * BLOCK_SIZE);
        for (block_i = 0; block_i < DIM_SIZE; block_i++)
        {
            block_j = block_k = -1;
            block_id(id, &block_i, &block_j, &block_k);
            pack_array(buffer,BLOCK_LOW(block_i),BLOCK_LOW(block_j),BLOCK_LOW(block_k),BLOCK_HIGH(block_i),BLOCK_HIGH(block_j),BLOCK_HIGH(block_k));
            MPI_Send(buffer,BLOCK_SIZE * BLOCK_SIZE * BLOCK_SIZE,MPI_DOUBLE,0,0,MPI_COMM_WORLD);
        }
        free(buffer);
    }
#pragma endscop
    if (id == 0)
        print_array();
    MPI_Finalize();
    return 0;
}