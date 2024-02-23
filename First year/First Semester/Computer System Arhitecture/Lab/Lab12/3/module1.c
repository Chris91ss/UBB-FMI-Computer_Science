# include <stdio.h>


void read_input(char str[]);


int main(void) {
    char str[100];
    printf("Enter a string (mustn't be longer than 100 characters): ");
    read_input(str);

    char numbers[100][100];
    int numbers_index = 0;

    for (int i = 0; str[i]; ++i) {
        if (str[i] >= '1' && str[i] <= '9') {
            int j = 0;

            if (str[i - 1] == '-') {
                numbers[numbers_index][j++] = '-';
            }

            while (str[i] >= '0' && str[i] <= '9') {
                numbers[numbers_index][j++] = str[i++];
            }

            numbers_index++;
        }
    }

    printf("The digit string is: ");
    for (int i = 0; i < numbers_index; ++i)
        printf("%s ", numbers[i]);

    scanf("%s", str);

    return 0;
}