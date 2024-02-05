## busybox添加applet命令

Time: 2019.03.25  
Tags: 开发,IoT  


### 0x00 前言

busybox 是一个集成了一百多个最常用 linux 命令和工具的软件，其被称作是嵌入式开发的瑞士军刀。

在使用 busybox 的嵌入式设备上，输入 linux 命令，最终都是进入到 busybox 进行解析执行，eg:

	[root@CentOSx64 bin]# ls -l pwd
	lrwxrwxrwx 1 root root 7 Mar 25 03:27 pwd -> busybox
	[root@CentOSx64 bin]# ./pwd
	/root/busybox/_install/bin

但在日常使用中，可能会遇到这种情况：

	./busybox tree
	tree: applet not found

表示 busybox 中没有该命令。本文简单的介绍了如何向 busybox 中添加命令(applet)。


### 0x01 源码简介
busybox 的源码从整体上可以分为三个大部分。

**1.busybox架构**  
busybox 架构部分为 busybox 的运行提供了基本支持。加载并调用各个 applet 扩展。

**2.busybox实用库**  
busybox 的可复用函数都被定义在 libbb 下面的文件中，其它的 applet 通过对这些函数的调用进行实现，以减小最后的文件大小。

**3.busybox的applet扩展**  
每一个命令在 busybox 中都是一个 applet 扩展。分布在各个类别的文件夹下(eg: networking，loginutils)


### 0x02 添加 applet
添加 applet 的步骤，可概括为以下五步：

	1.编写 applet 源码
	2.添加 applet 配置参数
	3.添加编译参数
	4.在 applet 器中添加注册
	5.添加 usage 说明

不同版本的 busybox 有微小的差别，这里以 `v1.31.0` 为例，添加一个 `hello` 命令，直接输出提示信息。

**1.编写 applet 源码**  
根据命令的分类，选择在不同的文件夹下添加 applet(eg: networking，loginutils)，这里选择在 `miscutils` 文件夹下添加命令。

在该目录下创建 `[command].c`，也就是 `hello.c`，编写代码：

	#include "libbb.h"

	int hello_main(int argc, char* argv[]) {
	    printf("This is test command. hello\n");
	    return 0;
	}

代码注解：

1. `libbb.h` 中包含了大量常用的头文件(eg: stdio.h)
2. `main` 函数以 `[command]_main` 定义

详细的编写规则可以参考：<https://github.com/mirror/busybox/blob/master/docs/new-applet-HOWTO.txt>  


**2.添加 applet 配置参数**  
在该 applet 的文件夹下，找到 `Config.src` 文件，也就是 `miscutils/Config.src`，在文件中的 `INSERT` 行以下，添加配置，使得该 applet 可以在配置界面中显示出来：

	config HELLO
	bool "hello test"
	default y
	help
	The add busybox command test

配置注解：

1. `config HELLO` 定义 applet 名
2. `bool "hello test"` 布尔指，配置文件中显示的简介信息
3. `default y` 布尔值默认为 true，表示默认勾选该 applet
4. `help` 以及下一行，为该 applet 的帮助信息

>附：不要尝试在 `Config.in` 中添加配置，因为 `Config.in` 是由 `make menuconfig`(等其他配置命令) 以 `Config.src` 为模版自动生成。


**3.添加编译参数**  
在该 applet 的文件夹下，找到 `Kbuild.src` 文件，也就是 `miscutils/Kbuild.src`，添加配置，使得该 applet 可以进行编译：

	lib-$(CONFIG_HELLO) += hello.o

>附：同样不要尝试在 `Kbuild` 中添加配置。

**4.在 applet 器中添加注册**  
打开 `include/applets.src.h`，在文件中的 `INSERT` 行以下，添加注册 `HELLO` applet：

	IF_HELLO(APPLET(hello, BB_DIR_USR_BIN, BB_SUID_DROP))

配置注解：

1. 参数1 `hello`：命令名称
2. 参数2 `BB_DIR_USR_BIN`：执行 make install 时的安装路径
3. 参数3 `BB_SUID_DROP`：命令的权限

>附：同样不要尝试在 `applets.h` 中添加配置。


**5.添加 usage 说明**  
打开 `include/usage.src.h`，在文件中的 `INSERT` 行以下，添加 `HELLO` 使用说明：

	#define hello_trivial_usage \
		"hello trivial usage"
	#define hello_full_usage \
		"hello full usage"
	#define hello_example_usage \
		"hello example usage"

配置注解

1. `trivial`: 命令简要帮助说明
2. `full`: 命令完整帮助说明
3. `example`: 使用说明样例

>附：同样不要尝试在 `usage.h` 中添加配置。

**6.编译运行**  
在 linux 平台上直接进行编译，以测试添加的 `hello` 命令(编译步骤参考 `0x03 编译`)。

	./busybox hello
	This is test command. hello


### 0x03 编译
针对不同的目标环境，搭建交叉编译环境，然后再进行编译。

**1.配置编译参数**  
使用 `make menuconfig` 进行编译配置，进入 `Settings->Build Options->() Cross Compiler prefix` 选项下，即可填写交叉编译器前缀(eg: `arm-linux-gnu-`)。随后退出保存设置。

**2.编译**  
在 busybox 源码根目录下执行 `make` 进行编译。

**3.打包**  
编译完成后，在 busybox 源码根目录下将生成 `busybox` 的二进制程序，为了便于命令使用，需要为每个命令建立软链接，如

	ln -s busybox cp

当然，可以使用 `make install` 自动生成所有命令的软链接，执行完后，将在当前目录下生成 `_install` 文件夹，目录如下：

	_install/
	|-- bin
	|-- linuxrc -> bin/busybox
	|-- sbin
	`-- usr

其中 `bin / sbin / usr` 存放的就是命令的软链接。

### 0x04 References
busybox官网：<https://www.busybox.net>  
busybox源码：<https://github.com/mirror/busybox>  
新建applet文档：<https://github.com/mirror/busybox/blob/master/docs/new-applet-HOWTO.txt>  
CSDN.添加busybox命令：<https://blog.csdn.net/xgbing/article/details/7697573>  
CSDN.busybox源码结构：<https://blog.csdn.net/tshaun007/article/details/17266089>  