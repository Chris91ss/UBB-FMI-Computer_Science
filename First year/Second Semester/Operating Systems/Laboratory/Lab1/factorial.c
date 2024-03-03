#include <stdio.h>

int factorial(int n);

int main(int argc, char** arcv)
{
	int n;
	scanf("%d", &n);
	printf("The factorial of n is: %d\n", factorial(n));
	return 0;
}

int factorial(int n)
{
	if(n == 0)
	   return 1;
	return n * factorial(n - 1);
}
