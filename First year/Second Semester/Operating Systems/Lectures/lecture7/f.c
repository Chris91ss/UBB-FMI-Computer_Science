#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

int n = 100;

void* f(void* a)
{
	int i;
	for(i = 0; i < n; i++) {
		printf("%d\n", *(int*)a);
	}
	free(a);
	return NULL;
}

int main(int argc, char** argv) {
	int i;
	pthread_t t[10];
	//int a[10];	
	int *a;	

//	for(i = 0; i < 10; i++) {
//		pthread_create(&t[i], NULL, f, &i); // each thread gets the address of i which is wrong, we need separate i's for each thread
//	}

//	for(i = 0; i < 10; i++) {
// 		a[i] = i;
//		pthread_create(&t[i], NULL, f, &a[i]);
//	}
	for(i = 0; i < 10; i++) {
		a = (int*)malloc(sizeof(int));
		*a = i;
		pthread_create(&t[i], NULL, f, a);
	}
	for(i = 0; i < n; i++) {
		printf("main\n");
	}
	for(i = 0; i < 10; i++) {
		pthread_join(t[i], NULL);
	}	
	return 0;
}
