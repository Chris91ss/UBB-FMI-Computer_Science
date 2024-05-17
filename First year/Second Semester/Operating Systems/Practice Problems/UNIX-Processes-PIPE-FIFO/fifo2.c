#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int gcd(int a, int b) {
    if (b == 0)
        return a;
    return gcd(b, a % b);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s fifo_name\n", argv[0]);
        return 1;
    }

    int fd = open(argv[1], O_RDONLY);
    int num1, num2;

    read(fd, &num1, sizeof(num1));
    read(fd, &num2, sizeof(num2));

    printf("GCD of %d and %d is %d\n", num1, num2, gcd(num1, num2));

    close(fd);
    unlink(argv[1]);

    return 0;
}
