#include <mpi.h>
#include <math.h>
#include <stdio.h>

#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

void manager(int p);
void worker();
double f(double x);

int main (int argc, char *argv[])
{
	int id;
	int p;

	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &id);
	MPI_Comm_size(MPI_COMM_WORLD, &p);
    if (p < 2)
    {
        printf("The number of processes must be at least 2\n");
        MPI_Finalize();
        return 1;
    }

    if (!id)
    {
        manager(p);
    }
    else
    {
        worker();
    }
	MPI_Finalize();
	return 0;
}

double f(double x) {
    double result = -2.0;
    for (int i = 1; i <= 1000; ++i) {
        result += std::sin(std::pow(x, i));
    }
    return result;
}

void manager(int p)
{
    double low = 0.0;
    double high = 1.0;
    while (high - low > 1e-11)
    {
        double interval = (high - low) / p;
        for (int i = 1; i < p; ++i)
        {
            double x = low + i * interval;
            MPI_Send(&x, 1, MPI_DOUBLE, i, 0, MPI_COMM_WORLD);
        }
        for (int i = 1; i < p; ++i)
        {
            double buffer[2];
            MPI_Recv(&buffer, 2, MPI_DOUBLE, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            if (buffer[1] > 0) high = MIN(high, buffer[0]);
            else low = MAX(low, buffer[0]);
        }
    }
    // terminate workers
    for (int i = 1; i < p; ++i)
    {
        double x = -1;
        MPI_Send(&x, 1, MPI_DOUBLE, i, 0, MPI_COMM_WORLD);
    }
    printf("The root is %.10f\n", (low + high) / 2);
}

void worker()
{
    double buffer[2];
    while(true)
    {
        MPI_Recv(&buffer, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        if (buffer[0] < 0) break;
        buffer[1] = f(buffer[0]);
        MPI_Send(&buffer, 2, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
    }
}