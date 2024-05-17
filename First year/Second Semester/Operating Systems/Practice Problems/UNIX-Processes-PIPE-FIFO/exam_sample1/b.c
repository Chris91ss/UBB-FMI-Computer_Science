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
	char s[101];
	int freq[11];
	if(access("AB", F_OK) == -1)
		mkfifo("AB", 0666);
	if(access("BA", F_OK) == -1)
		mkfifo("BA", 0666);
	if(access("BC", F_OK) == -1)
		mkfifo("BC", 0666);
	while(1)
	{	
		for(int i = 0; i < 11; i++)
			freq[i] = 0;		

		fd = open("AB", O_RDONLY);
		if(read(fd, s, sizeof(s)) <= 0)
			break;
		close(fd);

		for(int i = 0; i < strlen(s); i++)
		{
			if(s[i] > '0' && s[i] < '9')
				freq[s[i] - '0']++;
			else
				freq[10]++;
		}

		fd = open("BA", O_WRONLY);
		write(fd, freq, sizeof(freq));
		close(fd);

		fd = open("BC", O_WRONLY);
		write(fd, freq, sizeof(freq));
		close(fd);
	}
	return 0;
}
