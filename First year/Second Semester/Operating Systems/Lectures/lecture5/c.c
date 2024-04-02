#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>


int main(int argc, char** argv)
{
	int a[4] = {1, 2, 3, 4};
	//if(fork() == 0)
	//{
	//	a[2] += a[3];
	//	exit(0);
	//}
	//a[0] += a[1];
	//wait(0);
	//a[0] += a[2];
	//printf("%d\n", a[0]);
	//output is 6
	
	int p[2];
	pipe(p); // creates a pipe and puts in p the 2 file descriptors (one for reading one for writing) 0 for reading, 1 for writing
		 // always close the ending of a pipe if you don't need it
	if(fork() == 0)
	{
		close(p[0]);
		a[2] += a[3];
		write(p[1], &a[2], sizeof(int));
		close(p[1]);
		exit(0);
	}
	close(p[1]);
	a[0] += a[1];
	read(p[0], &a[2], sizeof(int));
	close(p[0]);
	wait(0);
	a[0] += a[2];
	printf("%d\n", a[0]);
	//output is 10 now
	return 0;
}
