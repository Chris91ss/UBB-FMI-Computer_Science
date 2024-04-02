#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>


int main(int argc, char** argv)
{
	if(fork() == 0)
	{
		if(execlp("echo", "echo", "asdf", NULL) == -1)
		{
			perror("Something went bad");
			exit(0);
		}
	}
	printf("We echoed!\n");
	wait(0);
	return 0;
}
