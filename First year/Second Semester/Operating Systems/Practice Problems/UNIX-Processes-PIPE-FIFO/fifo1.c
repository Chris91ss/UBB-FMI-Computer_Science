#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>


//Write 2 c programs.
//Program nr. 1:
//The program will receive 2 integer numbers as command line arguments. The
//program will spawn 2 child precesses, one process will calculate the sum and
//the other one the product of the numbers received as a command line
//arguments. Afte doing the calculations both processes will write the results
//into a fifo.
//Program nr. 2:
//The program will read 2 numbers from the fifo previously mentioned and
//display on the standard output the greatest common divisor of the 2 numbers.
//The name of the fifo will be passed as a command line argument.
//NOTES:
//For passing the exam:
// * all c souce codes must be compiled without any syntax errors or warnings
//   using the folowing command: gcc -Wall -g
// * no crashes/runtime errors are allowed
//For obtaining the maximum grade:
// * no memory leaks/context errors allowed
// * no envirounment presetup/cleanup allowed (aka. the programs will have to
//create/delete the fifo during the execution)
//GOOD LUCK!!



int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s num1 num2\n", argv[0]);
        return 1;
    }

    int num1 = atoi(argv[1]);
    int num2 = atoi(argv[2]);

    mkfifo("fifo_file", 0666);

    if (fork() == 0) {
        int sum = num1 + num2;
        int fd = open("fifo_file", O_WRONLY);
        write(fd, &sum, sizeof(sum));
        close(fd);
        exit(0);
    }

    if (fork() == 0) {
        int product = num1 * num2;
        int fd = open("fifo_file", O_WRONLY);
        write(fd, &product, sizeof(product));
        close(fd);
        exit(0);
    }

    wait(0);
    wait(0);

    return 0;
}
