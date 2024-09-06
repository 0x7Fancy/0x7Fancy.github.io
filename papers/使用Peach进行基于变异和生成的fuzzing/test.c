#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>

// +------------------------------------------+
// | header | length | chunk1 | chunk2 | data |
// +------------------------------------------+
//   2bytes   4bytes   2bytes   4bytes   nbytes
int vuln(char* str, int len) {
    int offset = 0;

    if (len <= 12) {
        printf("data format error\n");
        return 0;
    }

    char* header = str + offset;
    offset = offset + 2;

    int length = atoi(str);
    offset = offset + 4;

    char* chunk1 = str + offset;
    offset = offset + 2;
    char* chunk2 = str + offset;
    offset = offset + 4;

    char* data = str + offset;

    if (length > 0xF0000000) {
        printf("length = %x\n", length);
        raise(SIGSEGV);
    }
    else if (data[0] == 'A') {
        printf("data[0] %c\n", data[0]);
        raise(SIGSEGV);
    }
    else {
        printf("OK\n");
    }
    
    return 0;
}

int main(int argc, char *argv[]) {
    char buf[1024]={0};

    FILE* fp = fopen(argv[1], "rb");
    int n = fread(buf, 1, 1024, fp);
    //printf("%d %s\n", n, buf);
    vuln(buf, n);

    return 0;
}
