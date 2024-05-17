#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>


int main(int argc, char** argv)
{
    while(1)
    {
        int fd;
        int n;
        int U[101], u_index = 0;
        int L[101], l_index = 0;
        int S = 0;
        fd = open("A2B", O_RDONLY);
        read(fd, &n, sizeof(int));
        close(fd);
        while(n > 0)
        {
            if(n % 2 == 0)
            {
                U[u_index] = n % 10;
                u_index++;
            }
            else
            {
                L[l_index] = n % 10;
                l_index++;
            }
            S += n % 10;
            n = n / 10;
        }

        printf("The vector U is: ");
        for(int i = 0; i < u_index; i++)
            printf("%d ", U[i]);
        printf("\n");
        printf("The vector L is: ");
        for(int i = 0; i < l_index; i++)
            printf("%d ", L[i]);
        printf("\n");


        fd = open("B2A", O_WRONLY);
        write(fd, &S, sizeof(int));
        close(fd);
        fd = open("B2C", O_WRONLY);
        write(fd, U, sizeof(U));
        write(fd, &u_index, sizeof(int));
        write(fd, L, sizeof(L));
        write(fd, &l_index, sizeof(int));
        close(fd);
    }
    return 0;
}