#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv)
{
	int row, col;
	FILE* f;
	int** matrix;
	f = fopen(argv[1], "r");

	fscanf(f, "%d %d", &row, &col);
       	
	printf("rows:%d \ncols:%d \n", row, col);

	matrix = (int**)malloc(row * sizeof(int*));

	for(int i = 0; i < row; i++)
	{
		matrix[i] = (int*)malloc(col * sizeof(int));
                for(int j = 0; j < col; j++)
	        {
	        	fscanf(f, "%d", &matrix[i][j]);
	        }
	}
	
	fclose(f);

	for(int i = 0; i < row; i++)
	{
		for(int j = 0; j < col; j++)
		{
			printf("%2d ", matrix[i][j]);
		}
		printf("\n");
	}

	for(int i = 0; i < row; i++)
		free(matrix[i]);

	free(matrix);

	return 0;
}
