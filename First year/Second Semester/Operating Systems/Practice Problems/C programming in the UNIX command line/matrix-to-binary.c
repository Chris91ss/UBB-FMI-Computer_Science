#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

/*
* Compile using gcc -Wall -g -o matrix-to-binary matrix-to-binary.c
* Edit the source code and recompile until you fix all compilation errors and warnings
* Run the program using command valgrind ./matrix-to-binary matrix.txt matrix.bin
* Edit the source code, recompile and run, until valgrind reports that no leaks are possible
* Check the content of file matrix.bin using command xxd matrix.bin and repeat the steps above until the output of the command is as below.
* 0000000: 0700 0000 0300 0000 0100 0000 0200 0000  ................
* 0000010: 0300 0000 0400 0000 0500 0000 0600 0000  ................
* 0000020: 0700 0000 0800 0000 0900 0000 0a00 0000  ................
* 0000030: 0b00 0000 0c00 0000 0d00 0000 0e00 0000  ................
* 0000040: 0f00 0000 1000 0000 1100 0000 1200 0000  ................
* 0000050: 1300 0000 1400 0000 1500 0000            ............
*/

int main(int argc, char** argv) {
    int** m;
    FILE* f;
    int i, j, rows, cols, fd;

    f = fopen(argv[1], "r");
    if(f == NULL) {
        perror("Could not open file");
        return 1;
    }
    fscanf(f, "%d %d", &rows, &cols);

    m = (int**)malloc(rows * sizeof(int*));
    for(i=0; i<rows; i++) {
        m[i] = (int*)malloc(sizeof(int));
        for(j=0; j<cols; j++) {
            fscanf(f, "%d", &m[i][j]);
        }
    }
    fclose(f);

    fd = open(argv[2], O_CREAT | O_WRONLY, 00600);
    if(fd == -1) {
        perror("Could not open destination file");
        return 1;
    }
    write(fd, &rows, sizeof(int));
    write(fd, &cols, sizeof(int));
    for(i=0; i<rows; i++) {
        for(j=0; j<cols; j++) {
            write(fd, &m[i][j], sizeof(int));
        }
	free(m[i]);
    }
    close(fd);

    free(m);
    return 0;
}
