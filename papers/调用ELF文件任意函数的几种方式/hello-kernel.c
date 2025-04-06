#include <linux/init.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");

int add(int a, int b) {
	return a + b;
}

int sub(int a, int b) {
	return a - b;
}

static int hello_init(void) {
    printk("hello-kernel init\n");
    return 0;
}

static void hello_exit(void) {
    printk("hello-kernel exit\n");
}

module_init(hello_init);
module_exit(hello_exit);

// (required Makefile)
// make
//
// sudo insmod hello-kernel.ko
// sudo lsmod | grep hello_kernel
// sudo rmmod hello-kernel.ko
// sudo dmesg | grep hello-kernel
