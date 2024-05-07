#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/wait.h>


void f(int n)
{
	if(n > 0)
	{
		printf("child -> %d\n", n);
		if(fork() == 0)
			f(n - 1);
		wait(0);
	}
	exit(0);
}


int main(int argc, char** argv) {
	f(4);
	return 0;
}
