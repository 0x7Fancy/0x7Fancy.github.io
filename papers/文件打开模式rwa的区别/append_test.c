#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

void* write_without_append(void* args) {
    sleep(1);

    int tid = pthread_self();
    char buf[32] = {0};
    sprintf(buf, "0x%08x\n", tid);

    int fd = open("./test", O_CREAT | O_RDWR, 0644);
    lseek(fd, 0, SEEK_END);
    write(fd, buf, strlen(buf));
    close(fd);

    return 0;
}

void* write_with_append(void* args) {
    sleep(1);

    int tid = pthread_self();
    char buf[32] = {0};
    sprintf(buf, "0x%08x\n", tid);

    int fd = open("./test", O_CREAT | O_RDWR | O_APPEND, 0644);
    write(fd, buf, strlen(buf));
    close(fd);

    return 0;
}

int main(int argc, char* argv[]) {
    int MAX_THREAD = 20;
    pthread_t id[MAX_THREAD];
    int i = 0;

    for (i = 0; i < MAX_THREAD; i++) {
        //pthread_create(&id[i], NULL, (void*)write_without_append, NULL);
        pthread_create(&id[i], NULL, (void*)write_with_append, NULL);
    }

    for (i = 0; i < MAX_THREAD; i++) {
        pthread_join(id[i], NULL);
    }
    return 0;
}
