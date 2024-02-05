## QEMU虚拟化的基本使用

Time: 2022.08.23  
Tags: 运维  


### 0x00 前言

使用过不少 PC 端的虚拟机软件，比如 MAC 上备受好评的 Parallels Desktop，Windows 上最常用的 Vmware Workstation，以及开源的全平台 VirtualBox，这些软件各自几乎都能覆盖到大多数的应用场景，其提供的 GUI 界面也便于用户操作。

但是这些软件只能运行硬件 CPU 架构对应的虚拟机，当我们在 amd64 平台上想运行 arm 的程序就无能为力了，而 QEMU 的软件模拟可以满足这一需求；除此之外，苹果公司发行 arm 版的 MacBook，想在虚拟机中使用常规的 amd64 的操作系统，也不得不使用 QEMU。

QEMU 默认使用命令行进行操作，虽然使用上存在一定的门槛，但熟悉虚拟机使用的小伙伴能够很快理解其中的参数配置；本文对 QEMU 的基本使用进行介绍。

### 0x01 概要
QEMU 的全称为 `Quick Emulator`，是一款由法布里斯·贝拉（Fabrice Bellard）等人编写的通用且免费的可执行硬件虚拟化的开源仿真器。其通过软件模拟(动态二进制转换)的方式可以实现对不同架构硬件设备的模拟运行，除此之外，可以借助宿主机的硬件虚拟化技术(如 KVM) 实现高性能的运行。

QEMU 提供了多种运行模式，其中最常使用的是：
* 用户模式(User Mode)：QEMU 运行与宿主机不同架构，但同样操作系统和运行时的单一程序(如在 x86 的 Linux 系统上运行一个来自于 arm Linux 的程序)
* 系统模式(System Mode)：QEMU 模拟一个完整的计算机系统，包括各种硬件设备，在其上运行操作系统

我们常说的虚拟机对应的就是系统模式，本文我们只对系统模式的使用进行介绍；这里我们使用的测试环境如下：
```
MacOS 12.3
QEMU 7.0.0
```

在 mac 上直接使用 `brew` 即可完成安装：
```
brew install qemu
```

安装完成后可以看到以下命令：
<div align="center">
<img src="Images/qemu_commands.png" width="500">
</br>[qemu命令列表]
</div>

>PS: mac 默认安装只有系统模式，若是 Linux 下安装的话，还会有用户模式的命令，如 `qemu-x86_64`

我们这里直接启动试试 `qemu-system-x86_64`，可以看到如下虚拟机运行界面，由于我们没有配置启动设备，最后提示 `No bootable device`：
<div align="center">
<img src="Images/qemu-run-without-configure.png" width="500">
</br>[无配置直接运行qemu]
</div>

### 0x02 安装ubuntu
QEMU 配置完成后，我们来尝试安装一台虚拟机，来梳理基本使用流程，了解 QEMU 的使用从帮助开始，如 `qemu-system-x86_64 -h`；这里我们使用的 `ubuntu-16.04.6-server-i386.iso` 镜像。

在安装操作系统前，首先我们需要创建一个文件作为虚拟机的磁盘，这就和我们使用其他虚拟机在配置环节设置磁盘大小一样，只不过在 QEMU 中需要首先配置：
```
# 创建一个大小为 10GB 的 qcow2 格式的磁盘文件
qemu-img create -f qcow2 ubuntu16.04_x86.qcow2 10G
# 查看磁盘信息
qemu-img info ubuntu16.04_x86.qcow2
```
<div align="center">
<img src="Images/qemu-img-info.png" width="500">
</br>[查看创建的磁盘文件信息]
</div>

随后我们便可以启动虚拟机，常规的虚拟机配置，在 QEMU 中通过命令行参数的方式进行设置：
```
qemu-system-x86_64 -boot c -smp 1 -m 1024 -hda ubuntu16.04_x86.qcow2 -cdrom ubuntu-16.04.6-server-i386.iso
```

其中参数表示：
```
-boot c 设置启动项从 `c` CD光驱启动
-smp 1 设置 CPU 核心数为 1
-m 1024 设置内存为 1024MB
-hda ubuntu16.04_x86.qcow2 指定磁盘文件
-cdrom ubuntu-16.04.6-server-i386.iso 设置光驱镜像
```

和我们使用其他虚拟机软件的配置基本一致，只不过使用参数进行设置了而已，启动后可以看到如下画面：
<div align="center">
<img src="Images/ubuntu-install.png" width="500">
</br>[ubuntu安装界面]
</div>

接下来就正常安装系统，需要注意一点网络配置时会自动设置 `10.0.2.15`，这里默认即可；网络问题我们下文再来研究。

安装完成后，我们就可以正常使用了：
```
qemu-system-x86_64 -smp 1 -m 1024 -hda ubuntu16.04_x86.qcow2
```

和上面命令基本一致，取消了光驱设备，默认 `boot` 从硬盘启动。如下：
<div align="center">
<img src="Images/ubuntu-launch.png" width="500">
</br>[ubuntu正常启动]
</div>

**硬件虚拟化技术**  
QEMU 默认启动采用的虚拟化技术是 TCG(Tiny Code Generator)，指的是软件模拟的虚拟化技术，除此之外还有 KVM / HAX / HVF 等，我们这里是 macOS 操作系统，使用如下命令即可采用对应的硬件虚拟化技术：
```
qemu-system-x86_64 -machine accel=hvf -smp 1 -m 1024 -hda ubuntu16.04_x86.qcow2
```
>通常都建议使用硬件虚拟化技术，能极大的提高虚拟机性能。

### 0x03 网络与访问
当我们使用安装好的 `ubuntu16.04` 时，几乎和其他虚拟机软件没有区别，但细心的同学应该发现了虚拟机可以正常使用网络，但在宿主机上却不能正常访问到 `10.0.2.15`，无法 ping 通，也无法通过 `nc 10.0.2.15 22` 连通。

这是因为 QEMU 网络默认使用 `User模式`(其他还有 Tap / Hubs / Socket)，User 模式采用的 `SLiRP` 进行实现，纯软件模拟实现了 TCP/IP 协议栈，在工作表现上和 NAT 很像；在 User 模式下：
1. 不接受任何外部发起的访问
2. 软件模拟，性能较差
3. 默认不支持 ping

>QEMU 网络默认 User 模式，其默认配置为：网关为 10.0.2.2，DNS 服务器为 10.0.2.3，开启 DHCP 服务器，为客户机分配 10.0.2.15

那么我们如何才能访问虚拟机的服务呢？这里可以采用 QEMU 提供的端口转发的功能，启动虚拟机时使用如下参数：
```
qemu-system-x86_64 -smp 1 -m 1024 -hda ubuntu16.04_x86.qcow2 -nic user,hostfwd=tcp:127.0.0.1:7777-:22
```

前面部分都是一致的，网络部分参数如下：
```
-nic user,hostfwd=tcp:127.0.0.1:7777-:22
表示使用 user 模式网络
并设置端口转发：从宿主机的 127.0.0.1:7777 转发至虚拟机的 22 端口
```

随后便可以在宿主机上通过 ssh 连接访问虚拟机了：
```
ssh ubuntu@127.0.0.1 -p 7777
```

按此方法可以应对大部分的网络场景，当然还可以使用 Tap 网络模式，该模式需要宿主机配置 Tap 虚拟网卡，最后搭建真正意义的网络配置。

### 0x04 其他
**1.无界面启动**  
按如上 ubuntu 虚拟机，我们通常会使用 `ssh` 连接使用，这时候界面就不重要了，可以使用如下命令进行无界面启动：
```
qemu-system-x86_64 -smp 1 -m 1024 -hda ubuntu16.04_x86.qcow2 -nic user,hostfwd=tcp:127.0.0.1:7777-:22 -nographic
```

**2.VNC访问**  
有些场景我们不太想使用 QEMU 的虚拟机 GUI，那么可以使用 VNC 来访问，使用如下

VNC 可以提供剪切板复制，文件拷贝等功能，比起 QEMU 的虚拟机 GUI 还更好用一些；使用如下命令开启 VNC 访问：
```
qemu-system-x86_64 -vnc 127.0.0.1:0,password -monitor stdio
```

其参数表示：
```
-vnc 127.0.0.1:0,password 开启 vnc 在 127.0.0.1:5900(+0)，需要密码
-monitor stdio 进入 qemu 观察者模式，连接至标准输入输出
```

随后在 QEMU 控制台中设置 VNC 密码，再使用 VNC 客户端连接即可：
<div align="center">
<img src="Images/set-vnc-password.png" width="500">
</br>[设置VNC密码]
</div>

**3.文件共享**  
文件共享也是虚拟机使用中必不可少的功能，但 QEMU 这一点支持得不太好；

我们可以以宿主机为网络中转站，在其上搭建上传下载的 web 服务，来完成文件共享，虚拟机内使用浏览器或 curl 即可访问；直接使用 nc 传文件也可以，最后手动 md5 校验一下：
```
# 宿主机 => 虚拟机
# 宿主机
nc -lvnp 7777 < test
# 虚拟机
nc 10.0.2.2 7777 > test
```

除此之外，还可以磁盘挂载的方式进行文件共享：
```
# 在 Linux 宿主机上初始化磁盘文件 (mac 还需要额外的工具 ext4fuse)
dd if=/dev/zero of=share.img bs=4M count=1k
mkfs.ext4 share.img
# 虚拟机启动时附加进去
qemu-system-x86_64 -smp 1 -m 1024 -hda ubuntu16.04_x86.qcow2 -hdb share.img
# 随后两侧挂载文件即可访问
```

### 0x05 References
<https://www.qemu.org/>  
<https://www.qemu.org/docs/master/system/qemu-manpage.html>  
<https://wiki.qemu.org/Documentation/Networking>  
<https://www.jianshu.com/p/e1a4b5b808e0>  
<https://pjw.io/articles/2014/02/14/the-quick-guide-to-qemu-setup-translate/>  
<https://wiki.archlinux.org/title/QEMU_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)>  
<https://wiki.archlinux.org/title/QEMU#VNC>  
<https://man.archlinux.org/man/qemu.1>  