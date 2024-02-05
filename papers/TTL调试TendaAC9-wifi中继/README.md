## TTL调试TendaAC9-wifi中继

Time: 2019.09.10  
Tags: IoT,逆向分析  


### 0x00 前言
  
前段时间看到 Tenda，TP-Link 路由器老是爆洞，就想跟入研究一下，正巧手里有个空闲的 Tenda AC9 wifi 中继器，想着这估计和路由器比较类似，就着手试试。

wifi 中继器这种 IoT 设备本身的研究价值不是很大，原因是它肯定不会暴露在公网上，不过还是以学习的目的来动手做做。最终的结果是发现这个设备跑的是个 `eCos` 操作系统，和 linux 有一定的差别，也就没有深入下去了。

就本次尝试而言，本文就讲讲 IoT 分析/挖掘漏洞的前置工作----获取固件的思路，以及如何通过 TTL 调试设备。


### 0x01 获取固件
在 IoT 挖掘漏洞之前，肯定要先拿到二进制文件，然后才能对其进行分析。获取固件有以下方式(从易到难)：

**1.官方提供下载**  
部分设备，官方直接公开了固件的下载地址，直接下载即可。

**2.设备提供shell**  
部分设备，提供了 telnet / ssh 功能(或者可以在后台手动打开)，我们可以直接通过这种方式获取 shell，打包估计或者直接拷贝二进制文件。

**3.升级截获**  
官方没有提供下载，但设备有「升级更新」功能，可以将升级更新的数据报文抓取出来，提取其中的下载地址，或者从流量还原升级包。

**4.调试接口打包**  
如果设备有调试接口，可以连接调试接口获取 shell，然后打包固件到本地，或者直接拷贝目标二进制文件。

**5.flash读取**  
使用编程器，连接到设备的 flash 芯片上，读取出固件内容。

>附：通过以上方式拿到固件后，使用 binwalk 或者 sasquatch 工具对固件进行解包，然后就可以拿到目标二进制文件了。不过有部分固件做了加密处理，无法正常解包，可以使用「调试接口打包」的方式获取 shell，然后直接拿到目标二进制文件


### 0x02 AC9分析
Tenda AC9 wifi 中继器：

<div align="center">
<img src="images/image1.png" width="500">
</br>[1.Tenda AC9 wifi 中继器](图片来源于官网)
</div>

想要挖掘 Tenda AC9 这个设备的漏洞，就要先获取固件；

按照以上的步骤，我从官网下载到了该设备的固件，但遗憾的是，固件被加密了无法正常的解包，所以开始尝试接入到调试接口。


### 0x03 TTL调试前的准备
我们要打开设备进行飞线连接接口，这里先介绍下一些工具：

**1.一套螺丝刀**  
拆除设备外壳

**2.TTL转USB模块**  
可以连接设备上的 `UART` 接口，并转为 USB 口，可以与电脑连接。

大概是这样的：

<div align="center">
<img src="images/image2.png" width="500">
</br>[2.TTL转USB模块](图片来源于淘宝)
</div>

没有的话，淘宝上直接买，10-20元左右。

**3.万用表**  
在设备板子上，寻找 `UART` 接口，并测试 `UART` 接口电压。

**4.导线若干**  
连接「TTL转USB模块」和设备的 `UART` 口。

**5.USB延长线**  
(非必须，不过真的好用)

连接「TTL转USB模块」和电脑。

**6.minicom**  
电脑上安装 `minicom` 工具，用于连接调试接口和操作 shell。


### 0x04 UART接口
**UART接口标注**  
`UART` 接口在大部分设备上都有，从板子上找 `UART` 的标注，一般情况下都是 4-5 个 pin 引脚(排列整齐)，或者标注有：`GND`、`RX`、`TX`、`VCC`。

	GND: 接地pin，一般不接，有时 rx 和 tx 有问题接上可以解决
	RX: 读取数据pin，外部设备从该引脚读取数据
	TX: 发送数据pin，外部设备通过该引脚发送数据到设备
	VCC: 直流供电pin，一般为 3.3v，不使用

<div align="center">
<img src="images/image3.png" width="500">
</br>[3.标注的UART接口](图片来源于伏宸安全实验室)
</div>

**没有UART接口标注**  
当然也有些设备没有标注，这时候我们就用「万用表」对 4-5 pin 的(排列整齐)的接口进行电压测试。

其中 `UART` 接口有三种电压：`1.8v`、`3.3v`、`5v`，其中 `3.3v` 的情况最多。

`UART` 接口的电压特性：

	1.GND 电压为 0v
	2.RX 电压为 1.8v / 3.3v / 5v

所以，我们使用万用表进行测试，满足这个特性的引脚，我们就用「TTL转USB模块」进行连接，再给设备通电启动，然后在电脑上的 `minicom` 查看是否有输出(乱码也可以)(后面详细介绍)。

<div align="center">
<img src="images/image4.png" width="400">
</br>[4.Tenda AC9 板]
</div>

左侧 4 个 pin 为 `UART` 接口，没有标注，从上往下分别是：`GND`、`TX`、`RX`、`VCC`。

>附：「TTL转USB模块」实际上很容易坏，有时候没有输出，可能是这个模块坏了；测试方式是：将该设备连接到电脑上，使用 minicom 配置访问，然后将「TTL转USB模块」上的 RX 连接到 TX，然后在 minicom 中输入，看是否可以正常回显。


### 0x05 minicom
通过上一步，可能成功将 「TTL转USB模块」连接到了 UART 接口，接下来就使用 `minicom` 进行操作。(这里以 Mac 为例)

**1.查找设备**  
在 MAC 上查找到 usb 串口设备：

	$ ls /dev/*
	(以 "tty" 开头，非常明显的设备名，在我这里是：)
	tty.usbserial-A73OXMJ5

**2.minicom配置**  
以 `sudo` 启动 `minicom` 进行配置：

	# sudo minicom -s

将直接进入到配置中：

<div align="center">
<img src="images/image5.png" width="600">
</br>[5.minicom配置界面]
</div>

选择 `Serial port setup` 进入配置，设置设备名为 `tty.usbserial-A73OXMJ5`，设置波特率 `38400`(Tenda AC9)，关闭 `Hardware Flow Control`，返回查看输出。(设备名根据不同电脑而不同，波特率根据不同设备而不同，有些时候有输出，但是是乱码，表示波特率不正确)

<div align="center">
<img src="images/image6.png" width="600">
</br>[6.minicom配置界面]
</div>

**3.获取到shell**  
设置正确后，我们就获取到了设备的 shell，这里以 Tenda AC9 为例：

<div align="center">
<img src="images/image7.png" width="600">
</br>[7.Tenda AC9 调试shell]
</div>

>类 Linux 系统下 `screen [dev] [bits]` 命令也可以实现 `minicom` 的功能，可以尝试下：`screen /dev/tty.usbserial-A73OXMJ5 38400`

### 0x06 打包固件
拿到 shell 过后，我们就可以对固件进行打包，或者拉取目标二进制文件，开始逆向分析了。

<div align="center">
<img src="images/image8.png" width="600">
</br>[8.version命令(Tenda AC9)]
</div>

但我们这里就比较遗憾了，Tenda AC9 这个设备使用的是 `eCos` 实时操作系统(embedded configurable operating system)，不同于 `Linux`，也就没有再深入了。

### 0x07 References
<https://paper.seebug.org/649/>  
<https://zhuanlan.zhihu.com/p/25893717>  
<https://future-sec.com/iot-security-hardware-debuging.html>  