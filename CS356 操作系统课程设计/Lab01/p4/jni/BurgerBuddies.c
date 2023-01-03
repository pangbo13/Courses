/*Burger Buddies
A program to simulate Burger Buddies Problem.
Author: pangbo
*****************************************************
compile:
    ndk-build   #for android
    make        #for linux
macros:
    COOK_MAX_SLEEP_TIME: max time (in microsecond) for a cook to make a burger.
    CUSTOM_MAX_COME_TIME: the max time (in second) that the last customer comes.
    TIME_LIMIT: max execute time, if not defined, the main thread will wait until all threads exit.
note: This program should be compiled under the standard of c11.

useage:
    BBC Cooks Cashiers Customers RackSize
params:
    Cooks: number of cooks.
    Cashiers: number of cashiers.
    Customers: number of customers.
    RackSize: size of rack.
return value:
    0 - program exits normally.
    255 - number of params error.
    254 - value of params error.
*/

#include <pthread.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <unistd.h> 
#include <semaphore.h>

// #define TIME_LIMIT 60
#define COOK_MAX_SLEEP_TIME 3000000 //3s
#define CUSTOM_MAX_COME_TIME 30 //30s

int num_cooks;
int num_cashiers;
int num_customers;
int rack_size;
int served_customers;
int exit_flag;
//structure of cook
struct cook_t
{
    pthread_t pid;
    int cook_id;
}*cooks;

void init_cook(struct cook_t* cook,int id){
    cook->cook_id = id;
}

//structure of cashier
struct cashier_t
{
    pthread_t pid;
    int cashier_id;
}*cashiers;

void init_cashier(struct cashier_t* cashier,int id){
    cashier->cashier_id = id;
}

//structure of customer
struct customer_t
{
    pthread_t pid;
    int customer_id;
}*customers;

void init_customer(struct customer_t* customer,int id){
    customer->customer_id = id;
}

//structure of rack
struct rack_t{
    int size;   //size of rack
    int current;    //current number of burgers
    sem_t mutex;
    sem_t not_full;
    sem_t not_empty;
}rack;

void init_rack(struct rack_t* rack,int max_size){
    rack->size = max_size;
    rack->current = 0;
    sem_init(&(rack->mutex),0,1);
    sem_init(&(rack->not_full),0,1);
    sem_init(&(rack->not_empty),0,0);
}

//structure of queue
struct queue_t
{
    int size;   //number of cashiers
    int current;    //current waiting customers
    sem_t mutex;
    sem_t not_full; 
    sem_t not_empty;
}queue;

void init_queue(struct queue_t* queue,int max_size){
    queue->size = max_size;
    queue->current = 0;
    sem_init(&(queue->mutex),0,1);
    sem_init(&(queue->not_full),0,1);
    sem_init(&(queue->not_empty),0,0);
}

void set_exit_flag(){
    //no pthread_cancel func in Android so we use a global variable
    exit_flag = 1;
    //resume all the threads
    sem_post(&(queue.not_full));
    sem_post(&(rack.not_full));
    sem_post(&(queue.not_empty));
    sem_post(&(rack.not_empty));
}

void cook_action(struct cook_t* self){
    while(!exit_flag){
        usleep(rand()%COOK_MAX_SLEEP_TIME);
        //wait until rack is not full
        sem_wait(&(rack.not_full));
        if(exit_flag){
            //exit if time limit exceeded
            sem_post(&(rack.not_full));
            break;
        }
        sem_wait(&(rack.mutex));
        rack.current++;
        printf("Cook[%d] makes a burger.\n",self->cook_id);
        if(rack.current<rack.size) sem_post(&(rack.not_full));
        if(rack.current==1) sem_post(&(rack.not_empty));
        sem_post(&(rack.mutex));
    }
}
void customer_action(struct customer_t* self){
    sleep(rand()%CUSTOM_MAX_COME_TIME);
    if(exit_flag) return;
    printf("Customer[%d] comes.\n",self->customer_id);
    //wait if no cashier is available
    sem_wait(&(queue.not_full));
    if(exit_flag){
        sem_post(&(queue.not_full));
        return;
    }
    sem_wait(&(queue.mutex));
    queue.current++;
    //uncomment following line to enable the output when customer finish waiting
    // printf("Customer[%d] places an order.\n",self->customer_id);
    if(queue.current<queue.size) sem_post(&(queue.not_full));
    if(queue.current==1) sem_post(&(queue.not_empty));
    sem_post(&(queue.mutex));
}

void cashier_action(struct cashier_t* self){
    while(!exit_flag){
        //wait if there is no customer
        sem_wait(&(queue.not_empty));
        if(exit_flag){
            //exit if all jobs done
            sem_post(&(queue.not_empty));
            break;
        }
        sem_wait(&(queue.mutex));
        queue.current--;
        printf("Cashier[%d] accepts an order.\n",self->cashier_id);
        if(queue.current>0) sem_post(&(queue.not_empty));
        if(queue.current==queue.size-1) sem_post(&(queue.not_full));
        sem_post(&(queue.mutex));

        //get a burger from rack
        sem_wait(&(rack.not_empty));
        if(exit_flag){
            //exit if all jobs done
            sem_post(&(rack.not_empty));
            break;
        }
        sem_wait(&(rack.mutex));
        rack.current--;
        printf("Cashier[%d] takes a burger to customer.\n",self->cashier_id);
        if(rack.current>0) sem_post(&(rack.not_empty));
        if(rack.current==rack.size-1) sem_post(&(rack.not_full));
        served_customers++;
        if(served_customers==num_customers){
            //all the customers were served
            set_exit_flag();
        }
        sem_post(&(rack.mutex));
    }
}

int main(int argc, char const *argv[])
{
    //initialize random number generator
    srand(time(NULL));
    //initialize global variables
    exit_flag = 0;
    served_customers = 0;
    if(argc!=5) {
        printf("Usage: BBC Cooks Cashiers Customers RackSize\n");
        return -1;
    }
    num_cooks = atoi(argv[1]);
    num_cashiers = atoi(argv[2]);
    num_customers = atoi(argv[3]);
    rack_size = atoi(argv[4]);
    if(!(num_cooks>0&&num_cashiers>0&&num_customers>0&&rack_size>0)){
        printf("Params error!\n");
        printf("Usage: BBC Cooks Cashiers Customers RackSize\n");
        return -2;
    }
    printf("Cooks[%d],Cashiers[%d],Customers[%d]\n",num_cooks,num_cashiers,num_customers);

    //initialize data structures
    cooks = (struct cook_t*) malloc(num_cooks*sizeof(struct cook_t));
    for(int i=0;i<num_cooks;i++) init_cook(cooks+i,i);
    cashiers = (struct cashier_t*) malloc(num_cashiers*sizeof(struct cashier_t));
    for(int i=0;i<num_cashiers;i++) init_cashier(cashiers+i,i);
    customers = (struct customer_t*) malloc(num_customers*sizeof(struct customer_t));
    for(int i=0;i<num_customers;i++) init_customer(customers+i,i);
    init_rack(&rack,rack_size);
    init_queue(&queue,num_cashiers);
    
    printf("Begin run.\n");
    //start all the threads
    for(int i=0;i<num_cooks;i++)
        pthread_create(&(cooks[i].pid),NULL,(void*)(struct cook_t *)cook_action,&(cooks[i]));
    for(int i=0;i<num_cashiers;i++)
        pthread_create(&(cashiers[i].pid),NULL,(void*)(struct cashier_t *)cashier_action,&(cashiers[i]));
    for(int i=0;i<num_customers;i++)
        pthread_create(&(customers[i].pid),NULL,(void*)(struct customer_t *)customer_action,&(customers[i]));

    #ifdef TIME_LIMIT
    sleep(TIME_LIMIT);
    set_exit_flag();
    #endif

    //wait for all the threads
    for(int i=0;i<num_cooks;i++) pthread_join(cooks[i].pid,NULL);
    for(int i=0;i<num_cashiers;i++) pthread_join(cashiers[i].pid,NULL);
    for(int i=0;i<num_customers;i++) pthread_join(customers[i].pid,NULL);
    
    printf("Process end.\n");

    //destory semaphores
    sem_destroy(&(rack.not_full));
    sem_destroy(&(rack.not_empty));
    sem_destroy(&(rack.mutex));
    sem_destroy(&(queue.not_full));
    sem_destroy(&(queue.not_empty));
    sem_destroy(&(queue.mutex));
    
    free(cooks);
    free(cashiers);
    free(customers);

    return 0;
}
