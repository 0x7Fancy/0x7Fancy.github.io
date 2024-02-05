## 安卓逆向基础入门

Time: 2019.01.15  
Tags: 逆向分析,Android  

### 0x00 前言
最近，接到一个 APK 逆向的任务，正好借助这个机会系统的学习下 APK 逆向的相关技术。

本文梳理和整理了一些在 APK 逆向时会使用到的工具和方法，以及相关的 APK 基础知识。作为入门文档，全文大部分是基础内容和思路，不涉及技术细节或 anti 等内容。

Android 应用和 Java 关系紧密，其中逆向工具也大多需要 Java 的支持，所以需要预先安装 JDK 环境，其先导篇「configure android development env」包含了 Android 开发的一系列讲解，可以参考；当然逆向的真正的入门，应该是从开发开始的。


1. APK编译过程
2. 逆向常用工具
3. 静态分析
4. smalidea插件配置
5. 动态分析
6. adb工具
7. 调试设备的root环境
8. 修改APK
9. smali语言
10. so库分析
11. 总结

### 0x01 APK编译过程
**Android与Java**  
虽然 Android 也是使用 Java 进行开发(本文讨论范围仅限 Java)，但底层和 Java 并不相同。
<div align="center">
<img src="images/image1.png" width="300">
</br>[图1.Android与Java的关系]
</div>

**APK编译打包**  
如果从 Java 源码的角度来看，编译打包过程大致如下：

	1. 程序员开发编写 (*.java)
	2. 通过 Java 虚拟机编译 (*.java => *.class)
	3. 通过 Dex 工具 (*.class => *.dex)
	4. 通过 APK packager 打包 (*.apk)
	5. 对 APK 内的资源进行签名 (*.apk)

<div align="center">
<img src="images/image2.png" width="400">
</br>[图2.APK编译流程]
</div>


### 0x02 逆向常用工具
**APK中涉及到的文件类型**  
通过先导篇对 Android 开发的学习理解，以及 APK 的编译过程的了解，我们可以大致了解到 APK 逆向中可能会涉及到与程序逻辑相关的文件类型，也就是逆向工作中最关注的部分：

	1. *.java文件：源码文件
	2. *.class文件：Java编译器产生的中间文件
	3. *.dex文件：Dalvik虚拟机的可执行文件

将 APK 的逆向和传统的二进制逆向对比起来看：
<div align="center">
<img src="images/image3.png" width="400">
</br>[图3.APK逆向和二进制逆向的对比]
</div>

其中对 `dex` 文件进行反汇编可以得到 `smali` 文件，其中包含 `smali` 语言构成的程序逻辑，相当于二进制逆向中的汇编；通过对 `smali` 文件进行反编译，可以得到 `jar` 文件(Java ARchive)，其中包含 `Java` 源码。

**常用工具**  
那么在 APK 逆向这一块，有哪些工具可以帮助我们进行逆向分析呢？

	1.apktools: 对 APK 进行打包和解包，反编译其中的资源文件
	2.dex2jar: 将 *.dex 文件反编译为 *.jar 文件
	3.jd-gui / jadx / JEB: 读取解析 *.jar 文件
	4.adb: Android Debug Bridge，调试软件和设备的桥梁
	5.Eclipse / Android Studio: 开发和动态调试 APK
	6.jarsigner: APK 签名工具(JDK自带)
	7.IDA: 动态调试 APK，以及反编译和动态调试 so 文件

其中的小工具都打包在 `/tools` 目录下，需要安装的工具请自行下载安装。


### 0x03 静态分析
我们以 Android 中的 `HelloWorld` 项目为例，作为分析的样本。首先来学习如何进行静态分析 APK。

**反编译资源文件**  
APK包实际上就是一个压缩文件，可以使用解压工具对其解压，但其中的文件都是通过的编译后的二进制文件，无法直接进行读取分析。

通过 `apktools` 工具可以对 APK 进行解包，可以对 APK 中的资源文件进行反编译，以获得可以读取的文件。

	java -jar apktools.jar decode HelloWorld.apk

打开新生成的文件 `HelloWorld`，可以直接读取资源文件：
<div align="center">
<img src="images/image4.png" width="400">
</br>[图4.读取Android配置文件]
</div>

当然，其中还包括反汇编后的 `*.smali` 文件，可以进行分析理解，但效率很低。
<div align="center">
<img src="images/image5.png" width="400">
</br>[图5.读取smali代码文件]
</div>

**反编译代码**  
通过解压工具对 APK 解压，可以看到在根目录下有 `classes.dex` 文件，该文件是通过 Dex 工具编译打包后的源码，其中有整个项目的代码。

通过 `dex2jar` 工具可以对 `*.dex` 文件进行反编译：

	d2j-dex2jar.bat classes.dex

随后使用读取 `classes-dex2jar.jar` 文件的工具(jd-gui/jadx/JEB)进行分析：

<div align="center">
<img src="images/image6.png" width="400">
</br>[图6.反编译示例]
</div>

>附：对于同一个 jar 文件，有些工具可能无法反编译出某些函数，而其他工具可以，在遇到这种情况的时候，可以尝试换换工具。 
> 
>除此之外，某些 APK 进行了加固，反编译出的源码中的函数和变量都用 a、b、c 代替，不过还是勉强能读；而某些 APK 如果结合 so 文件进行加固，那么该方法根本无法反编译出结果，需要手动分析 so 并脱壳才可以继续分析。


### 0x04 smalidea插件配置
静态分析非常容易上手，也可以完成逻辑结构简单的 APK 的逆向工作；但在某些场景下，静态分析太过于复杂，又需要涉及到某一项具体运行后的值，就不得不需要进行动态调试了。

这里我们使用 Android Studio 进行动态调试，在动态调试前，需要首先安装 `smalidea` 插件，以便让 Android Studio 支持对 `smali` 的单行调试。

	1.下载插件 https://github.com/JesusFreke/smali
	2.Android Studio -> Preferences -> Plugins -> Install plugin from disk -> smalidea.zip
	3.重启 Android Studio

<div align="center">
<img src="images/image7.png" width="400">
</br>[图7.smalidea插件安装完成]
</div>

在 Android Studio 中不支持对 `smali` 的反编译，动态调试应该配合静态分析进行。


### 0x05 动态分析
和开发的时候一样，动态调试 APK 也涉及到 Android Studio 和设备这两部分的交互；其中 Android Studio 供用户进行操作、跟踪、查看，而设备负责运行该 APK，在两者之间充当桥梁的是 `ADB(Android Debug Bridge)`。

动态调试的步骤大致如下：

1. 修改 APK 至 debug 模式，反编译和二次打包
2. 以调试模式启动 APK
3. 转发调试端口
4. 新建远程调试，开始调试

下面进行详细的介绍。

**1.修改APK至debug模式**  
release 版本的 APK 不支持直接进行调试，需要先修改为 debug 模式。

###### 重打包
使用 `apktools` 将 APK 解包，在 `AndroidManifest.xml `文件中的 `application` 标签中添加 `android:debuggable="true"`

<div align="center">
<img src="images/image8.png" width="400">
</br>[图8.添加debuggable属性]
</div>


###### APK签名
APK 需要签名才能够在设备上运行，下面我们对重打包后的 APK 进行签名，需要使用到 `keytool` 和 `jarsigner` 工具。(这两个工具由 JDK 自带)

1.使用 `keytool` 工具创建密钥

	keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000

2.使用 `jarsigner` 和生成的密钥进行签名

	jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore test1.apk alias_name

>附：除了上述的修改 APK 至 debug 模式来进行调试，还可以修改 Android 系统的设置来支持 APK 的调试，直接修改 `/default.prop` 中的 `ro.debuggable` 为 1(需要设备的 root 权限)，即可直接对 APK 进行调试；该方法可以保证原 APK 的完整性。

**2.通过adb在设备上启动项目**  
接下来，我们使用 adb 工具将上一步中重打包后的 APK 安装到设备上。保证真机或模拟器正确的连接并启动 `USB 调试`。

1.安装 APK 至设备上

	adb install HelloWorld.apk

通过 abd 成功安装 APK 后，可以在设备上的 `/data/app/` 下找到该应用的包。

2.以 debug 模式启动 APK

	adb shell am start -D -n com.example.xx.HelloWorld/.MainActivity
	
其中 `-D` 表示以调试模式启动，`com.example.xx.HelloWorld` 为应用的包名，`.MainActivity` 为入口 activity。

成功启动后，可以在设备上看到应用等待调试的弹窗提示。

3.调试端口转发
先查看应用的进程号：

	adb shell ps

使用 `adb forward` 将进程转发到 tcp 端口上，以便调试器连接：

	adb forward tcp:5005 jdwp:7777

其中 `jdwp` 的全称为 `Java Debug Wire Protocol`，是调试器和设备之间的通信协议。

<div align="center">
<img src="images/image9.png" width="400">
</br>[图9.adb安装与启动应用]
</div>

>附：在低版本的 Android Studio 中有 DDMS(Dalvik Debug Monitor Service)，用来统一的监察设备的服务，底层同样也是使用的 ADB，有 GUI 方便使用。不过在我使用的版本中(3.2.1)，移除了 DDMS 的图标(可能是官方不推荐使用？)，不过可以通过 `C:\Users\John\AppData\Local\Android\Sdk\tools\monitor.bat` 启动 DDMS。

**3.Android Studio加载项目**  
###### 加载项目
在第一步中，使用了 `apktools` 对 APK 进行了解包，这里我们使用 Android Studio 加载解包后的项目。

	Android Studio -> File -> New -> Import Project

按向导逐步完成，加载完毕后，设置项目的路径 `Make Directory as -> Source Root`

<div align="center">
<img src="images/image10.png" width="350">
</br>[图10.设置项目源码路径]
</div>

随后项目结构将变成完整的项目结构，我们可以打开 `smali` 目录下查看代码，并且可以在代码的首部进行点击，以设置断点。

<div align="center">
<img src="images/image11.png" width="400">
</br>[图11.在smali中添加断点]
</div>

###### 配置远程调试
在第二步中，使用 adb 启动了应用并转发了调试端口至 `5005` 上，这里我们在 Android Studio 中配置连接该端口。打开 debug 设置：`Run -> Edit Configurations`，并点击配置窗口左上角 `Add New Configuration -> Remote`，然后配置端口。

<div align="center">
<img src="images/image12.png" width="400">
</br>[图12.设置远程调试端口]
</div>

**4.开始调试**  
完成以上三步后，可以开始调试了，点击 `Run -> Debug`，选择刚才设置的远程调试，代码将在断点处停止。

<div align="center">
<img src="images/image13.png" width="500">
</br>[图13.调试界面示例]
</div>

>附：在上文中，我们知道 adb 和 DDMS 都可以帮助建立调试器和设备之间的关系，但在某些情况下，连接并不是一定能成功，如果出现这种情况，可以尝试换换工具(可能是由于abd 和 DDMS 端口冲突？)


### 0x06 adb工具
在「0x05 动态分析」这一小节已经提到了 ADB(Android Debug Bridge)，并使用 adb 对设备进行了基础的操作，这里再详细说下该工具。

对于一台已经连接的设备，在打开 `USB 调试` 后，ADB 可以直接连接设备进行操作。

1.查看连接设备

	adb devices

2.进入设备的交互式 shell

	adb shell

3.安装应用程序

	adb install [apk]

4.启动应用程序

	adb shell am start -n [package]/.MainActivity
	或者 在交互式 shell 中：
	am start -n [package]/.MainActivity


### 0x07 调试设备的root环境
在使用 ADB 进入到真机或模拟器(Android 7.0 以上)的设备设备的交互式 shell 时，默认为 `shell` 用户，而在我们调试或是测试的过程中，`shell` 权限往往不能满足我们的需求。

所以对于真机和模拟器(Android 7.0 以上)的设备，需要先对设备进行 root 操作，这里就不展开了。

<div align="center">
<img src="images/image14.png" width="400">
</br>[图14.在交互式shell中获取root权限]
</div>

>附：模拟器 Android 6.0 及以下的设备，通过 adb 连接可以直接获得 root 权限，在配置模拟器时可以考虑选择这些版本，以便于后续调试。


### 0x08 修改APK
对于已发布的 APK，我们仍可以进行修改，以满足自己的功能需求。实际上在「0x05 动态分析」小节，我们已经使用到了该技术，我们修改了配置文件以便 APK 支持 debug 模式，这里我们再整理下。

**1.解包**  
使用 `apktools` 对 APK 进行解包

	java -jar apktools.jar decode test.apk

**2.修改**
对文件进行修改，可以替换图片，也可以修改配置文件，当然也可以修改程序逻辑，不过需要 `smali` 语法基础。

**3.打包签名**
在完成修改后，再次使用 `apktools` 进行打包

	java -jar apktools.jar build test -o test_new.apk

随后使用 `jarsigner` 进行二次签名

	jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore test1.apk alias_name

>附：APK 有两种签名模式，将影响我们对文件的修改情况：  
>1.jar 签名：仅对源码进行签名，资源文件不签名  
>2.apk 全签名：对所有文件进行签名
>
>若 APK 采用第一种方式进行签名，对其中的资源文件(如：图片)等资源的修改，不需要进行二次签名；而第二种方式，对任意文件的修改都需要进行二次签名。


### 0x09 smali语言
虽然 APK 的反编译效果非常好，在没有混淆的情况下，几乎可以得到源码；但在动态调试的过程中、或是某些混淆的代码，我们不得不理解分析 `smali` 代码。

所以掌握 `samli` 语法是逆向必须的，这里不展开，大家自行学习补充。


### 0x0A so库分析
在某些 APK 中，为了 `可移植性`、`重用`、`高性能`，会将部分函数封装为 `*.so` 库，或是将某些敏感函数(加密函数、代码混淆)封装进去。在逆向分析过程中，难免会遇到这种情况。

so库的分析可以参考传统二进制的逆向技巧，这里不展开。大家自行学习补充。


### 0x0B 总结
本文介绍了 Android APK 逆向入门的基本步骤，对 APK 中使用到的工具进行了简单的介绍，希望可以在大家初次接触 APK 时提供参考。


### 0x09References
developer.android: <https://developer.android.com/studio/build/>  
juejin: <https://juejin.im/entry/58d54b9144d9040068684957>  
cnblogs: <https://www.cnblogs.com/goodhacker/p/5592313.html>  
stayzeal: <http://blog.stayzeal.cn/2018/05/15/Android-Studio动态调试-Smail踩坑/>  
cnblogs: <https://www.cnblogs.com/yhjoker/p/8974119.html>  
jianshu: <https://www.jianshu.com/p/1ecee8ffbbed>  