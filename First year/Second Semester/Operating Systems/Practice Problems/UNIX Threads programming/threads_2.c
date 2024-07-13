#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>


pthread_mutex_t mutex;
pthread_barrier_t barrier;


struct data{
	char *s;
	int *V;
};

void *f(void *a)
{
	struct data *d = (struct data*)a;
	pthread_barrier_wait(&barrier);
	for(int i = 0; i < strlen(d->s); i++)
	{	
		pthread_mutex_lock(&mutex);
		int poz = d->s[i] - '0';
		if(d->s[i] >= '0' && d->s[i] <= '9')
			d->V[poz]++;
		else
			d->V[10]++;
		pthread_mutex_unlock(&mutex);
	}
	return NULL;
}


int main(int argc, char **argv)
{
	int N;
	printf("Enter the number of strings: ");
	scanf("%d", &N);
	
	char **strings = (char**) malloc(N * sizeof(char *));
	for(int i = 0; i < N; i++)
	{
		strings[i] = (char *) malloc(100 * sizeof(char));
		printf("Enter the string %d: ", i + 1);
		scanf("%s", strings[i]); 
	} 

	pthread_mutex_init(&mutex, NULL);
	pthread_barrier_init(&barrier, NULL, N);
	

	int *V = (int*) malloc(11 * sizeof(int));
	for(int i = 0; i < 11; i++)
		V[i] = 0;
	pthread_t t[N];
	struct data d[N];
	for(int i = 0; i < N; i++)
	{
		d[i].s = strings[i];
		d[i].V = V;
		pthread_create(&t[i], NULL, f, &d[i]);
	}

	for(int i = 0; i < N; i++)
		pthread_join(t[i], NULL);
	
	for(int i = 0; i < 11; i++)
		printf("%d ", V[i]);

	printf("\n");

	free(strings);
	free(V);
	pthread_mutex_destroy(&mutex);
	pthread_barrier_destroy(&barrier);
	return 0;
}
