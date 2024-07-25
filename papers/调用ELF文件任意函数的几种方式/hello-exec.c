#include <stdio.h>

__attribute__((visibility("default"))) int add(int a, int b) {
	return a + b;
}

__attribute__((visibility("hidden"))) int sub(int a, int b) {
	return a - b;
}

int main(int argc, char* argv[]) {
	printf("[hello-exec]\n");

	int c = add(1, 2);
	printf("add(1, 2) = %d\n", c);

	int d = sub(3, 4);
	printf("sub(3, 4) = %d\n", d);

	return 0;
}

// Position Independent Executable (default: -fPIC)
// gcc hello-exec.c -o test1
// Absolute Address Code
// gcc -fPIC -no-pie hello-exec.c -o test2
