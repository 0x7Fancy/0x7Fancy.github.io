#include <stdio.h>

extern int add(int a, int b);
extern int sub(int a, int b);

int main() {
    printf("loader-static\n");

    int result = 0;
    result = add(1, 2);
    printf("add(1, 2) = %d\n", result);
    result = sub(9, 8);
    printf("sub(9, 8) = %d\n", result);

    return 0;
}

// gcc loader-static.c test.a -o test
