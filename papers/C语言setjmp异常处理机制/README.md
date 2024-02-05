## C语言setjmp异常处理机制

Time: 2023.01.06  
Tags: 开发  


### 0x00 前言

最近在阅读一个项目源码时，遇到了 C 语言标准库中的 `setjmp` 功能，在此之前没有接触过，所以在阅读源码的时候无法正确的理解调用流程。

通过 Google 了解到 `setjmp` 在 C 语言中常用于异常处理机制的实现，本文使用简单的 demo 介绍 `setjmp` 的使用方法。

本文测试环境：
```
Ubuntu 18.04 x64
gcc 7.5.0
```

### 0x01 goto/setjmp
C 语言语法中提供 `goto` 关键词用于无条件跳转，虽然 `goto` 可能破坏程序的结构化设计、混淆程序执行流程，但合理规范的使用 `goto` 能够提高代码质量。

`goto` 的执行流程如下：
```
#include <stdio.h>

int main(int argc, char* argv[]) {
    printf("before goto\n");

    goto END_LABEL;
    printf("flag\n");

END_LABEL:
    printf("after goto\n");

    return 0;
}

#
before goto
after goto
```

不过 `goto` 只能用于函数内部的跳转，`setjmp` 则是 `goto` 的升级版，可用于跨函数的跳转；不过要进行跨函数的跳转，就必须处理上下文的问题(寄存器/信号/etc)，`setjmp` 和 `longjmp` 是一组用于跳转的语句。

>实际上 `goto` 也需要处理上下文，如我们应该避免在 `goto` 和 `LABEL` 之间声明/定义变量。

**`int setjmp(jmp_buf env)`**
调用 `setjmp` 用于初始化 `jmp_buf` 缓冲区，并设置跳转位置；若直接调用 `setjmp`，该函数返回 0 值，若通过 `longjmp` 跳转至此，该函数返回非 0 值。

**`void longjmp(jmp_buf env, int value)`**
调用 `longjmp` 用于从 `jmp_buf` 中还原上下文环境，并跳转至 `setjmp` 处。`value` 参数可以传递至 `setjmp` (返回值)。

glibc 中的实现如下：https://sourceware.org/git/?p=glibc.git;a=blob;f=sysdeps/x86_64/setjmp.S

### 0x02 setjmp执行流程
我们通过以下 demo 演示 `setjmp` 的执行流程：
```
#include <stdio.h>
#include <setjmp.h>

jmp_buf buf;

void second() {
    printf("second\n");
    longjmp(buf, 1);
}

void first() {
    second();
    printf("first\n");
}

int main() {
    if (!setjmp(buf)) {
        first();
    }
    else {
        printf("main\n");
    }

    return 0;
}

#
second
main
```

以上程序中，首先执行到 `setjmp`，直接调用所以返回 `0`，进入 `if` 分支并调用 `frist()` 函数，随后调用 `second()` 函数，在 `second()` 函数中输出后调用 `longjmp`，`longjmp` 将恢复上下文环境，并跳转至 `setjmp` 的位置，随后 `setjmp` 返回 `1`，进入 `else` 分支，执行完毕。

### 0x03 异常处理实现
利用 `setjmp/longjmp` 我们可以在 C 语言中实现异常处理机制，如下：
```
#include <stdio.h>
#include <setjmp.h>

#define try if(!setjmp(buf))
#define catch else
#define throw longjmp(buf, 1)

jmp_buf buf;

int check_zero(int n) {
    if (n == 0) {
        throw;
    }
    else {
        printf("ok\n");
    }
    return 0;
}

int main() {
    int num = 1;

    scanf("%d", &num);
    try {
        check_zero(num);
    }
    catch {
        printf("error\n");
    }

    return 0;
}
```

我们使用 `setjmp/longjmp` 仿造现代编程语言中的 `try-catch` 实现了 C 语言下的异常处理机制，执行程序后，输入 `0` 则会进入 `catch` 分支输出 `error`。

### 0x04 协程实现
`setjmp/longjmp` 还能在 C 语言中实现协程，以下 demo 演示了两个协程的交替执行：
```
#include <stdio.h>
#include <setjmp.h>

jmp_buf bufferA, bufferB;

void routineB(); // forward declaration 

void routineA() {
    int r;

    printf("(A1)\n");

    r = setjmp(bufferA);
    if (r == 0) routineB();

    printf("(A2) r=%d\n",r);

    r = setjmp(bufferA);
    if (r == 0) longjmp(bufferB, 20001);

    printf("(A3) r=%d\n",r);

    r = setjmp(bufferA);
    if (r == 0) longjmp(bufferB, 20002);

    printf("(A4) r=%d\n",r);
}

void routineB() {
    int r;

    printf("(B1)\n");

    r = setjmp(bufferB);
    if (r == 0) longjmp(bufferA, 10001);

    printf("(B2) r=%d\n", r);

    r = setjmp(bufferB);
    if (r == 0) longjmp(bufferA, 10002);

    printf("(B3) r=%d\n", r);

    r = setjmp(bufferB);
    if (r == 0) longjmp(bufferA, 10003);
}


int main(int argc, char **argv) {
    routineA();
    return 0;
}

#
(A1)
(B1)
(A2) r=10001
(B2) r=20001
(A3) r=10002
(B3) r=20002
(A4) r=10003
```

### 0x05 其他
本文仅简单介绍了 `setjmp/longjmp` 的基本使用，由于 `setjmp` 只对非易失的寄存器进行保存，更不会处理堆栈上下文，产生数据污染问题，导致实际使用过程中非常容易出现内存错误，在生产环境中需要进行严格的预研和测试。


### 0x06 References  
https://en.wikipedia.org/wiki/Setjmp.h  
http://ibillxia.github.io/blog/2011/05/03/Exception-handling-mechanism-in-c/
http://caozong.top/178/
https://stackoverflow.com/questions/14685406/practical-usage-of-setjmp-and-longjmp-in-c
https://www.cnblogs.com/zengqh/archive/2011/06/17/2477414.html
https://blog.lucode.net/backend-development/talk-about-setjmp-and-longjmp.html  
https://sourceware.org/git/?p=glibc.git;a=blob;f=sysdeps/x86_64/setjmp.S  
