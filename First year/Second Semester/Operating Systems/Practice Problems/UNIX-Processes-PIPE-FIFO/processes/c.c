#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int n = 0;
pthread_mutex_t m[3];

void *f(void *p)
{
    int id = (int)(long)p;  // Cast to long to avoid warnings
    pthread_mutex_lock(&m[id]);
    n += id;
    printf("%d ", n);
    pthread_mutex_unlock(&m[(id + 1) % 3]);
    return NULL;
}

int main()
{
    int i;
    pthread_t t[3];

    for (i = 0; i < 3; i++)
    {
        pthread_mutex_init(&m[i], NULL);
    }

    // Lock the mutexes in the required order
    pthread_mutex_lock(&m[1]);
    pthread_mutex_lock(&m[2]);

    for (i = 0; i < 3; i++)
    {
        pthread_create(&t[i], NULL, f, (void *)(long)i);  // Cast to long to avoid warnings
    }

    // Unlock the first mutex to start the sequence
    pthread_mutex_unlock(&m[0]);

    for (i = 0; i < 3; i++)
    {
        pthread_join(t[i], NULL);
    }

    for (i = 0; i < 3; i++)
    {
        pthread_mutex_destroy(&m[i]);
    }

    return 0;
}
