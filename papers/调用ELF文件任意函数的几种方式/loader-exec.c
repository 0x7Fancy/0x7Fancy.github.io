#define _GNU_SOURCE

#include <stdio.h>
#include <dlfcn.h>

typedef int (*FUNC_ADD) (int, int);
typedef int (*FUNC_SUB) (int, int);

static int (*main_orig)(int, char **, char **);

int main_hook(int argc, char **argv, char **envp) {
    printf("main hook\n");
    printf("bypass address(main_orig) = %p\n", main_orig);

    void* handle = dlopen(NULL, RTLD_LAZY);
    FUNC_ADD add = (FUNC_ADD)(*(long*)handle + 0x1169);
    FUNC_SUB sub = (FUNC_SUB)(*(long*)handle + 0x1181);

    int result = 0;
    result = add(1, 2);
    printf("add(1, 2) = %d\n", result);
    result = sub(9, 8);
    printf("sub(9, 8) = %d\n", result);

    return 0;
}

int __libc_start_main(
    int (*main)(int, char **, char **),
    int argc,
    char **argv,
    int (*init)(int, char **, char **),
    void (*fini)(void),
    void (*rtld_fini)(void),
    void *stack_end) {
    // Save the real main function address
    main_orig = main;

    // Find the real __libc_start_main()...
    typeof(&__libc_start_main) orig = dlsym(RTLD_NEXT, "__libc_start_main");

    // ... and call it with our custom main function
    return orig(main_hook, argc, argv, init, fini, rtld_fini, stack_end);
}

// gcc -fPIC -shared loader-exec.c -o hook.so
// LD_PRELOAD=./hook.so ./test1
