#include <stdio.h>
#include <pthread.h>
#define THREAD_NUMS 4

pthread_barrier_t barrier;

void *t0(void *param)
{
    printf("t0 ready\n");
    pthread_barrier_wait(&barrier);
}

void *t1(void *param)
{
    printf("t1 ready\n");
    pthread_barrier_wait(&barrier);
}

void *t2(void *param)
{
    printf("t2 ready\n");
    pthread_barrier_wait(&barrier);    
}

int main(void)
{
pthread_t t[3];
pthread_barrier_init(&barrier, NULL, 4);

pthread_create(&t[0], NULL, t0, NULL);
pthread_create(&t[1], NULL, t1, NULL);
pthread_create(&t[2], NULL, t2, NULL);

sleep(10);
pthread_barrier_wait(&barrier);

printf("all sub threads ready, go!\n");

pthread_barrier_destroy(&barrier);

}