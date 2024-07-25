#include <dlfcn.h>
#include <stdio.h>

typedef int (*FUNC_ADD) (int, int);
typedef int (*FUNC_SUB) (int, int);

int main(int argc, char* argv[]) {
    void* handle = dlopen("./hello-dyn.so", RTLD_LAZY);

    FUNC_ADD add = dlsym(handle, "add");
    FUNC_SUB sub = (FUNC_SUB)(*(long*)handle + 0x1111);

    int result = 0;
    result = add(1, 2);
    printf("add(1, 2) = %d\n", result);
    result = sub(9, 8);
    printf("sub(9, 8) = %d\n", result);

    dlclose(handle);
    return 0;
}

// gcc loader-dyn.c -o test
