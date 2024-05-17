#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>


int main(int argc, char** argv)
{	
	int fd;
	int freq[11];
	if(access("BC", F_OK) == -1)
		mkfifo("BC", 0666);
	if(access("CA", F_OK) == -1)
		mkfifo("CA", 0666);
	while(1)
	{	
		int sum = 0;
		fd = open("BC", O_RDONLY);
		if(read(fd, freq, sizeof(freq)) <= 0)
			break;
		close(fd);
		
		for(int i = 0; i < 11; i++)
			sum += freq[i];

		fd = open("CA", O_WRONLY);
		write(fd, &sum, sizeof(int));
		close(fd);
	}
	return 0;
}
