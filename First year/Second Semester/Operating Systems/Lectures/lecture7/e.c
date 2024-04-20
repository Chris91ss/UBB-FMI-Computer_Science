#include <stdio.h>
#include <pthread.h>

int n = 10;

void* f(void* a)
{
	int i;
	for(i = 0; i < n; i++) {
		printf("%s\n", (char*)a);
	}
	return NULL;
}

int main(int argc, char** argv) {
	int i;
	pthread_t ta, tb;

	pthread_create(&ta, NULL, f, "fa");
	pthread_create(&tb, NULL, f, "fb");
	for(i = 0; i < n; i++) {
		printf("main\n");
	}
	pthread_join(ta, NULL);	
	pthread_join(tb, NULL);	
	return 0;
}
