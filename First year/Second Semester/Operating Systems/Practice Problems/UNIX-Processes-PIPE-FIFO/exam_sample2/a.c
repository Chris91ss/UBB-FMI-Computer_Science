//Write multiple C programs that can be labeled as A, B and C.

//Process A:
//    - will read from keyboard numbers (until 0 is written) and will send them to process B using FIFOs
//Process B:
//    - will receive the number from process A using FIFOs.
//    - will receive the number and it iterate over it digit by digit checking if the digit is an odd or an even digit:
//            If it is an even digit it will be added in vector U, otherwise in vector L.
//            In the same time it will compute the sum of the digits in a variable S.

//    After L, U, S are computed they will be sent as follows:
//        - S to process A
//        - L, U to process C
//        using FIFOs

//Processes C:
//    - Will receive the L and U from process A and it will sum up their sizes and print the result on the screen.


#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>


int main(int argc, char** argv)
{
    while(1)
    {
        int fd;
        int n;
        printf("Input a number or 0 to stop: ");
        scanf("%d", &n);
        if(n == 0)
            break;
        fd = open("A2B", O_WRONLY);
        write(fd, &n, sizeof(int));
        close(fd);

        int S = 0;
        fd = open("B2A", O_RDONLY);
        read(fd, &S, sizeof(int));
        close(fd);

        printf("The sum of the digits is: %d\n", S);
    }
    return 0;
}