#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

/*
* Compile using gcc -Wall -g -o matrix-from-text matrix-from-binary.c
* Edit the source code and recompile until you fix all compilation errors and warnings
* Run the program using command valgrind ./matrix-from-binary matrix.bin
* Edit the source code, recompile and run, until valgrind reports that no leaks are possible and the program output is
*   1  2  3
*   4  5  6
*   7  8  9
*   10 11 12
*   13 14 15
*   16 17 18
*   19 20 21
*/

int main(int argc, char** argv) {
    int fd, rows, cols, i, j;
    int** m;

    if(argc <= 1) {
        fprintf(stderr, "No input file specified");
        exit(1);
    }

    fd = open(argv[1], O_RDONLY);
    if(fd == -1) {
        perror("Failed to open input file");
        exit(1);
    }

    if(read(fd, &rows, sizeof(int)) <= 0) {
        perror("Could not read the number of rows");
        exit(1);
    }

    if(read(fd, &cols, sizeof(int)) <= 0) {
        perror("Could not read the number of columns");
        exit(1);
    }

    m = (int**)malloc(rows * sizeof(int));
    for(i=0; i<rows; i++) {
        m[i] = (int*)malloc(sizeof(int));
        read(fd, m[i], cols * sizeof(int));
        for(j=0; j<cols; j++) {
            printf("%2d", m[i][j]);
        }
	free(m[i]);
        printf("\n");
    }
    free(m);

    close(fd);
    return 0;
}
