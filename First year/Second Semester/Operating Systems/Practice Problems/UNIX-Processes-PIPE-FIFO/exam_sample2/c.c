#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>


int main(int argc, char** argv)
{
    while(1)
    {
        int U[101], u_index = 0;
        int L[101], l_index = 0;
        int fd;
        fd = open("B2C", O_RDONLY);
        read(fd, U, sizeof(U));
        read(fd, &u_index, sizeof(int));
        read(fd, L, sizeof(L));
        read(fd, &l_index, sizeof(int));
        close(fd);

        int sum = u_index + l_index;

        printf("The sum of the sizes of the vectors is: %d\n", sum);
    }
    return 0;
}