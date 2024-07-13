#include <mpi.h>
#include <math.h>
#include <stdio.h>
#include <time.h>

#define BLOCK_LOW(id, p, n) ((id) * (n) / (p) )

#define BLOCK_HIGH(id, p, n) (BLOCK_LOW((id) + 1, p, n) - 1)

#define BLOCK_SIZE(id, p, n) (BLOCK_LOW((id) + 1, p, n) - BLOCK_LOW((id), p, n))

#define BLOCK_OWNER(index, p, n) (((p) * ((index) + 1) - 1) / (n))

void merge(int *part1, int size1, int *part2, int size2, int *result) {
    int i = 0, j = 0, k = 0;
    while(i < size1 && j < size2) {
        if(part1[i] < part2[j]) result[k++] = part1[i++];
        else result[k++] = part2[j++];
    }
    while(i < size1) result[k++] = part1[i++];
    while(j < size2) result[k++] = part2[j++];
}

void local_merge_sort(int *numbers, int n) {
    if(n <= 1) return;
    int mid = n / 2;
    local_merge_sort(numbers, mid);
    local_merge_sort(numbers + mid, n - mid);
    int *temp = new int[n];
    int i = 0, j = mid, k = 0;
    merge(numbers, mid, numbers + mid, n - mid, temp);
    for(int i = 0; i < n; i++) numbers[i] = temp[i];
    delete[] temp;
}

bool is_power_of_2(int n) {
    return (n & (n - 1)) == 0;
}

int main(int argc, char** argv){
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
    if (!is_power_of_2(p)) {
        if (id == 0)
            printf("The number of processes must be a power of 2\n");
        MPI_Finalize();
        return 1;
    }

    const int N = atoi(argv[1]);
    int *numbers;
    int *receive_buffer;
    int *sorted_buffer;
    // Generate random numbers
    if (id == 0)
    {
        numbers = new int[N];
        srand(time(NULL));
        for (int i = 0; i < N; i++)
            numbers[i] = rand() % 1000;

        // printf("Before sort: ");
        // for (int i = 0; i < N; i++) {
        //     printf("%d ", numbers[i]);
        // }
        // printf("\n");
    }

    MPI_Barrier(MPI_COMM_WORLD);
    double elapsed_time = -MPI_Wtime();

    if (id == 0) {
        int *displs = new int[p];
        int *receive_counts = new int[p];
        for (int i = 0; i < p; i++) {
            displs[i] = BLOCK_LOW(i, p, N);
            receive_counts[i] = BLOCK_SIZE(i, p, N);
        }
        receive_buffer = new int[BLOCK_SIZE(id, p, N)];
        MPI_Scatterv(numbers, receive_counts, displs, MPI_INT, receive_buffer, BLOCK_SIZE(id, p, N), MPI_INT, 0, MPI_COMM_WORLD);
        delete[] displs;
        delete[] receive_counts;
        delete[] numbers;
    } else {
        receive_buffer = new int[BLOCK_SIZE(id, p, N)];
        MPI_Scatterv(NULL, NULL, NULL, MPI_INT, receive_buffer, BLOCK_SIZE(id, p, N), MPI_INT, 0, MPI_COMM_WORLD);
    }
    local_merge_sort(receive_buffer, BLOCK_SIZE(id, p, N));
    sorted_buffer = receive_buffer;
    receive_buffer = NULL;
    int task_id = id;
    int local_buffer_size = BLOCK_SIZE(id, p, N);
    int aggregate_size = 1;
    while ((0x1 << aggregate_size) <= p)
    {
        if (id % (0x1 << aggregate_size) != 0) {
            int target_id = id >> aggregate_size << aggregate_size;
            MPI_Send(&local_buffer_size, 1, MPI_INT, target_id, 0, MPI_COMM_WORLD);
            MPI_Send(sorted_buffer, local_buffer_size, MPI_INT, target_id, 0, MPI_COMM_WORLD);
            delete[] sorted_buffer;
            break;
        } else {
            int *local_part = sorted_buffer;
            sorted_buffer = NULL;
            int source_id = id + (0x1 << (aggregate_size - 1));
            int receive_buffer_size;
            MPI_Recv(&receive_buffer_size, 1, MPI_INT, source_id, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            receive_buffer = new int[receive_buffer_size];
            MPI_Recv(receive_buffer, receive_buffer_size, MPI_INT, source_id, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            sorted_buffer = new int[local_buffer_size + receive_buffer_size];
            merge(local_part, local_buffer_size, receive_buffer, receive_buffer_size, sorted_buffer);
            delete[] local_part;
            delete[] receive_buffer;
            local_buffer_size += receive_buffer_size;
            aggregate_size++;
        }
    }

    elapsed_time += MPI_Wtime();
    if (id == 0) {
        // printf("After sort: ");
        // for (int i = 0; i < N; i++) {
        //     printf("%d ", sorted_buffer[i]);
        // }
        printf("\n");
        printf("Elapsed time: %lf\n", elapsed_time);
    }

    MPI_Finalize();
}