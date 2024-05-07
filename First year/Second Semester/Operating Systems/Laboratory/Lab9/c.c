#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/wait.h>


int main(int argc, char** argv) {
 	int pid;
	for(int i = 0; i < 3; i++)
	{
 		pid = fork();
 		if(pid == 0) {
			printf("Child-only code number -> %d\n", i);
 			exit(0);
		}
	}
	//printf("Parent-only code\n");
	for(int i = 0; i < 3; i++) {
		printf("Parent-only code\n");
		wait(0);
	}
	return 0;
}
