#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>

int main(int argc, char** argv)
{
	int pid;

	printf("before\n");
	pid = fork();
	if(pid == 0)
	{
		printf("Child specific code pid=%d fork return=%d\n", getpid(), pid);
		exit(0);
	}
	printf("Parent specific code, CHILD PID=%d\n", pid);
	wait(0);
	return 0;
}
