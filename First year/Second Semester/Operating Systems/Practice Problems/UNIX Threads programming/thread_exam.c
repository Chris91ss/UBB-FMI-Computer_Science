#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


//Write a C program that will read from keyboard N numbers and will send them to N separate threads.
//The main process will also initiate 2 vectors L and U, and an integer named S.

//Each thread will receive the correspondent number read from keyboard (thread i will receive the i-th number read from keyboard), variable S, and the 2 vectors L and U as function argument, and WILL NOT START until all threads were created.
//After all threads were created and initiated, each thread will check if the number received starts with an even or an odd digit:
//If it starts with an even digit it will be added in vector U, otherwise in vector L.
//It will also sum the number received to the variable S.

//Before inserting the thread will verify if it was the FIRST thread to insert a value in one of the 2 vectors and print a corresponding message on the screen.

//In the end the master will print the size of L and U and the value of S

//Use optimal lock mechanisms to make sure there are no data corruptions, and a proper synchronization method to make all threads wait until all threads were created.

pthread_barrier_t barrier;
pthread_mutex_t mutex;

struct data {
	int *L;
	int *len_L;
	int *U;
	int *len_U;
	int *S;
	int num;
};


void *f(void *a)
{
	struct data *d = (struct data *)a;
	pthread_barrier_wait(&barrier);
	pthread_mutex_lock(&mutex);
	int nr = d->num;
	while(nr >= 10)
		nr /= 10;
	if(nr % 2 == 0)
	{
		if((*d->len_U) == 0)
			printf("First thread to insert in U\n");
		d->U[*d->len_U] = d->num;
		(*d->len_U)++;
	}
	else
	{	if((*d->len_L) == 0)
			printf("First thread to insert in L\n");
		d->L[*d->len_L] = d->num;
		(*d->len_L)++;
	}	
	(*d->S) += d->num;
	pthread_mutex_unlock(&mutex);
	return NULL;
}


int main(int argc, char** argv)
{
	int N;
	printf("Enter the number of elements: ");
	scanf("%d", &N);
	
	pthread_t t[N];
	pthread_barrier_init(&barrier, NULL, N);
	pthread_mutex_init(&mutex, NULL);
	
	int number[N];
	for(int i = 0; i < N; i++)
	{
		printf("Enter a number for thread %d:", i + 1);
		scanf("%d", &number[i]);
	}
	struct data d[N];
	int *L = (int*) malloc(N * sizeof(int));
	int len_L = 0;
	int *U = (int*) malloc(N * sizeof(int));
	int len_U = 0;
	int S = 0;
	for(int i = 0; i < N; i++)
	{
		d[i].L = L;
		d[i].len_L = &len_L;
		d[i].U = U;
		d[i].len_U = &len_U;
		d[i].S = &S;
		d[i].num = number[i];
		pthread_create(&t[i], NULL, f, &d[i]);
	}

	for(int i = 0; i < N; i++)
		pthread_join(t[i], NULL);
	
	printf("The size of L is: %d\n", len_L);
	printf("The size of U is: %d\n", len_U);
	printf("The sum S is: %d\n", S);
	

	pthread_barrier_destroy(&barrier);
	pthread_mutex_destroy(&mutex);	
	free(L);
	free(U);
	return 0;
}
