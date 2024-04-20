#include "header.h"

int main(int argc, char** argv){
	int shmid;
	struct absp *x;

	shmid = shmget(3203, 0, 0);
	x = shmat(shmid, 0, 0);

	srand(time(NULL));
	while(1) {
		x->a = x->a + x-> b;
		x->b = x->a * x->b;
		if(x->p == x->s) { 
			break;
		}
	}

	shmdt(x);

	return 0;
}
