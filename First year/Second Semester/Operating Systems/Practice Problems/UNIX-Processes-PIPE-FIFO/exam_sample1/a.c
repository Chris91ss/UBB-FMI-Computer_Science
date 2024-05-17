#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

// Write multiple C programs that can be labeled as A, B, C
// Process A:
//       - will read from keyboard lowercased strings (that can contain alphanumerical characters) (until x is written) and will send them to process B using FIFOs
// Process B:
//       - will receive the string from process A.
//	 - will initiate a vector V with 11 zeros and it will iterate over it character by character checking if the character is a digit or not, and incrementing an index of the vector as following:
//	 	0 -> 0
//		1 -> 1
//		2 -> 2
//		...
//		9 -> 9
//		not a digit -> 10

//	This frequency vector for the digits + non-digits found in the string will be send to:
//		- process A
//		- process C

//Processes C:
//	- will receive the frequency vector from the process B and it will sum up all the values and it will send it back to process A that will print it on the screen.

// The programs are responsible to check if the fifo exists and create it if it is not.



int main(int argc, char** argv)
{
	char s[101];
	int freq[11];
	int fd;
	if(access("AB", F_OK) == -1)
		mkfifo("AB", 0666);
	if(access("BA", F_OK) == -1)
		mkfifo("BA", 0666);
	if(access("CA", F_OK) == -1)
		mkfifo("CA", 0666);

	while(1)
	{
		printf("Enter a string or x to stop: ");
		scanf("%s", s);
		if(s[0] == 'x')
			break;
		fd = open("AB", O_WRONLY);
		write(fd, s, sizeof(s));
		close(fd);

		
		fd = open("BA", O_RDONLY);
		read(fd, freq, sizeof(freq));
		close(fd);
		for(int i = 0; i < 11; i++)
			printf("%d ", freq[i]);
		printf("\n");
			
		int sum = 0;
		fd = open("CA", O_RDONLY);
		read(fd, &sum, sizeof(int));
		printf("The sum is: %d\n", sum);
		close(fd);
	}
		
	return 0;
}
