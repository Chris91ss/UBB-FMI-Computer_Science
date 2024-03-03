#include <stdlib.h>
#include <stdio.h>


/*
* Compile using gcc -Wall -g -o matrix-from-text matrix-from-text.c
* Edit the source code and recompile until you fix all compilation errors and warnings
* Run the program using command valgrind ./matrix-from-text matrix.txt
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
    FILE* f;
    int rows, cols, i, j;
    int** m;

    f = fopen(argv[1], "r");
    if(f == NULL) {
        perror("Nu am putut deschide fisierul cu matricea");
        return 1;
    }

    fscanf(f, "%d %d", &rows, &cols);
    m = (int**)malloc(rows*sizeof(int*));
    for(i=0; i<rows; i++) {
        m[i] = (int*)malloc(sizeof(int));
        for(j=0; j<cols; j++) {
            fscanf(f, "%d", &m[i][j]);
        }
    }
    fclose(f);

    for(i=0; i<rows; i++) {
        for(j=0; j<cols; j++) {
            printf("%2d ", m[i][j]);
        }
        printf("\n");
    }

    for(i=0; i<rows; i++)
    {
	free(m[i]);
    }

    free(m);

    return 0;
}
