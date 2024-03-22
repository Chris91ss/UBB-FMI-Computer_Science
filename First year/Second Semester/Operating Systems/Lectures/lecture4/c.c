#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>

//run the command: while true; do clear; ps -f -u USERNAME; sleep 1; done
//in a console and this program in another to see zombies

int main(int argc, char** argv)
{
	int i;
	for(i = 0; i < 3; i++)
	{
		if(fork() == 0)
		{
			sleep(5);
			exit(0);
		}
	}

	sleep(10);
	
	for(i = 0; i < 3; i++)
	{
		wait(0);
	}
	return 0;
}
