#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>


//Write a C program that will read from keyboard N strings and will send them to N separate threads (the threads will be initiated only after all N strings were read).
//The main process will also initiate 2 vectors L and U, and a integer named S.

//Important: The threads will have to wait until all threads were initiated and created.

//Each thread "i" will receive the "i-th" read string and it will check if the string starts with an uppercase or lowercase letter:
//If it starts with an uppercase letter it will be added in vector U, otherwise in vector L.
//If the string starts with a digit it will increment a shared variable S.

//Before inserting the thread will verify if it was the FIRST thread to insert a value in one of the 2 vectors and print a corresponding message on the screen.

//In the end the master will print the size of L and U and the value of S

//Use optimal lock mechanisms to make sure there are no data corruptions, and a proper synchronization method to make all threads wait until all threads were created.



pthread_mutex_t mutex;
pthread_barrier_t barrier;


struct data{
    char *string;
    char **L;
    int *len_L;
    char **U;
    int *len_U;
    int *S;
    int *thread_index;
};


void *f(void *a)
{
    pthread_barrier_wait(&barrier);
    struct data *d = (struct data*)a;
    pthread_mutex_lock(&mutex);
    if(d->string[0] >= 'A' && d->string[0] <= 'Z')
    {
        if((*d->len_U) == 0)
            printf("The thread %d was the first to insert in U\n", (*d->thread_index));
        d->U[(*d->len_U)] = d->string;
        (*d->len_U)++;
    }
    else if(d->string[0] >= 'a' && d->string[0] <= 'z')
    {
        if((*d->len_L) == 0)
            printf("The thread %d was the first to insert in L\n", (*d->thread_index));
        d->L[(*d->len_L)] = d->string;
        (*d->len_L)++;
    }
    else if(d->string[0] >= '0' && d->string[0] <= '9')
    {
        (*d->S)++;
    }
    pthread_mutex_unlock(&mutex);

    return NULL;
}


int main(int argc, char** argv)
{
    int N;
    printf("Enter the number of strings: ");
    scanf("%d", &N);

    char **strings = (char**) malloc(N * sizeof(char*));
    for(int i = 0; i < N; i++)
    {
        strings[i] = (char*) malloc(100 * sizeof(char));
        printf("Enter the string %d: ", i + 1);
        scanf("%s", strings[i]);
    }

    pthread_mutex_init(&mutex, NULL);
    pthread_barrier_init(&barrier, NULL, N);
    pthread_t t[N];

    struct data d[N];
    char **L = (char**) malloc(N * sizeof(char*));
    int len_L = 0;
    char **U = (char**) malloc(N * sizeof(char*));
    for(int i = 0; i < N; i++)
    {
        L[i] = (char*) malloc(100 * sizeof(char));
        U[i] = (char*) malloc(100 * sizeof(char));
    }
    int len_U = 0;
    int S = 0;
    int index[N];
    for(int i = 0; i < N; i++)
    {
        index[i] = i + 1;
        d[i].string = strings[i];
        d[i].L = L;
        d[i].len_L = &len_L;
        d[i].U = U;
        d[i].len_U = &len_U;
        d[i].S = &S;
        d[i].thread_index = &index[i];
        pthread_create(&t[i], NULL, f, &d[i]);
    }

    for(int i = 0; i < N; i++)
        pthread_join(t[i], NULL);

    printf("The size of L is: %d\n", len_L);
    printf("The size of U is: %d\n", len_U);
    printf("The value of S is: %d\n", S);


    pthread_mutex_destroy(&mutex);
    pthread_barrier_destroy(&barrier);
    free(strings);
    free(L);
    free(U);
    return 0;
}