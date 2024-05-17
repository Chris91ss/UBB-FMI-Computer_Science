#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/wait.h>


//Write 2 processes. The first one randomly generates a number between 1000 and 10000,
//the second tries to guess it (it still generates a row) and sends it to the first process. The first process tells him if
//the number was <, > or = with the one to be guessed. The program stops when the second
//process guesses the number (received = from the first process).
