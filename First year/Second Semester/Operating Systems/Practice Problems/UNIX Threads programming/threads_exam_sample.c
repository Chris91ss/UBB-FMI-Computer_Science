#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>


//Write a C program that will read from keyboard N lowercased strings and will send them to N separate threads (the threads will be initiated only after all N strings were read).
//The main process will also initiate a vector "V" with 26 zeros
//Important: The threads will not have to wait until all threads were initiated and created.
//Each thread "i" will receive as argument the "i-th" string and it will iterate over it character by character trying to compute an index considering the ASCII code of a character:
//a (97) -> 0
//b (98) -> 1
//c (99)-> 2
//etc.
//This index corresponds to a position in vector V that will have to be incremented during each character iteration.
//Before incrementing the thread will verify if it was the FIRST thread to increment the index of that character and print a corresponding message on the screen.
//In the end we will obtain a frequency vector for the characters found in the strings read from keyboard that will have to printed by the main process.
//Use optimal lock mechanisms to make sure there are no data corruptions, and a proper synchronization method to make all threads wait until all threads were created.

pthread_mutex_t mutex;


struct data {
	char *string;
	int *V;
};


void *f(void *a)
{
	struct data *d = (struct data*)a;
	for (int i = 0; i < strlen(d->string); i++)
    {
        int poz = d->string[i] - 'a';
        pthread_mutex_lock(&mutex);
        if (d->V[poz] == 0)
            printf("First thread to modify character '%c'\n", d->string[i]);
        d->V[poz]++;
        pthread_mutex_unlock(&mutex);
    }
	return NULL;
}


int main(int argc, char** argv)
{
	int N;
	printf("Enter the number of strings: ");
	scanf("%d", &N);
	char **strings = (char **) malloc(N * sizeof(char*));
	for(int i = 0; i < N; i++)
	{
		strings[i] = (char*) malloc(100 * sizeof(char));
		printf("Enter string %d: ", i + 1);
		scanf("%s", strings[i]);
	}

	pthread_mutex_init(&mutex, NULL);

	int *V = (int*) malloc(26 * sizeof(int));
	for(int i = 0; i < 26; i++)
		V[i] = 0;
	pthread_t t[N];
	struct data d[N];
	for(int i = 0; i < N; i++)
	{
		d[i].string = strings[i];
		d[i].V = V;
		pthread_create(&t[i], NULL, f, &d[i]);
	}

	for(int i = 0; i < N; i++)
		pthread_join(t[i], NULL);

	for(int i = 0; i < 26; i++)
		printf("%d ", V[i]);
	printf("\n");
	
	pthread_mutex_destroy(&mutex);
	free(strings);
	free(V);
	return 0;
}
