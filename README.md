**[Home](./README.md) / [Tags](./tags.md) / [Archives](./archives.md) / [Reviews](https://github.com/0x7Fancy/0x7Fancy.github.io/issues) / [About](./about.md)**

## **Home**

### [基于树莓派DIY制作电子相框](papers/基于树莓派DIY制作电子相框)
**(2024.05.22) 其他**  
最近家里拍摄的照片越来越多，但没有一个良好的展示的方式，通常冲洗照片可能还需要照片墙或者相册，这样也挺麻烦的，所以考虑 DIY 制作一个电子相框用来滚动播放，正巧家里还有一块闲置的树莓派 zero，本文就次进行记录。

----------------

### [调用ELF文件任意函数的几种方式](papers/调用ELF文件任意函数的几种方式)
**(2024.05.07) 开发/逆向分析**  
动态链接库是一种把共享的代码制作为公共的库文件，以减少软件的冗余存储占用以及提高运行效率的软件开发优化方案，如 Linux 下的动态链接库(Shared Object) `.so` 文件，根据设计开发人员可以通过调用动态链接库的导出函数，快速实现业务功能。

Linux 下常见的可执行文件 ELF 格式包括：二进制程序(`EXEC`)、动态链接库(`so`)、静态链接库(`a`)、内核模块(`ko`)、等等，那么这些格式是否可以像动态链接库的函数一样被外部所调用，从而在闭源情况下实现对软件的二次开发，或者用于辅助逆向分析呢？本文就此进行探讨和实现。

----------------

### [xz-utils后门代码分析](papers/xz-utils后门代码分析)
**(2024.04.22) 逆向分析/恶意软件**  
[xz-utils](https://github.com/tukaani-project/xz) 是一种使用 LZMA 算法的数据压缩/解压工具，文件后缀名通常为 `*.xz`，是 Linux 下广泛使用的压缩格式之一。

2024.03.29 由微软工程师 Andres Freund 披露了开源项目 xz-utils 存在的[后门漏洞](https://www.openwall.com/lists/oss-security/2024/03/29/4)，漏洞编号为 [CVE-2024-3094](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-3094)，其通过供应链攻击的方式劫持 sshd 服务的身份认证逻辑，从而实现认证绕过和远程命令执行，该后门涉及 liblzma.so 版本为 5.6.0 和 5.6.1，[影响范围](https://mp.weixin.qq.com/s/CFuqNN36M9DgO1FAGVy5GA)包括 Debian、Ubuntu、Fedora、CentOS、RedHat、OpenSUSE 等多个主流 Linux 发行版，具体影响版本主要是以上发行版的测试版本和实验版本。

截止本文发布，距离 xz-utils 后门披露已经过去三个星期了，全球安全研究人员在互联网上发布了大量的高质量[分析报告](#references)，这帮助我们对 xz-utils 后门事件进行详尽的理解。本文将从这些分析报告出发，对其进行翻译、整理和复现，并围绕着 xz-utils 后门代码部分进行分析研究，了解攻击者的技术方案和实施细节，从而在防御角度提供一定的技术支持。

----------------

### [afl语法变异插件Grammar-Mutator的基本使用](papers/afl语法变异插件Grammar-Mutator的基本使用)
**(2024.01.09) fuzzing**  
变异算法是 fuzzing 中非常重要的一个环节，良好的变异算法能产出较高的路径覆盖率，从而提高发现 crash 的概率；afl/afl++ 默认提供的变异算法在通用情况下表现优秀，但对于格式要求严格的数据则显得无能为力，基于语法的变异是一种优秀的变异算法优化方案，并具有良好的普适性，安全研究人员通过对理解数据格式编写对应的语法树生成器，从而可以准确的生成符合要求的数据，极大的提高路径覆盖率。

最近工作中和同事 @ghost461 一起研究学习 afl++ 的语法变异插件 Grammar-Mutator，本文对此进行梳理，并详细介绍 Grammar-Mutator 的使用和基本原理。

----------------

### [PVE环境安装Windows11操作系统](papers/PVE环境安装Windows11操作系统)
**(2023.12.29) 运维**  
最近日常工作中遇到一个 Windows11 操作系统的前置要求，由于安装 Windows11 操作系统需要硬件满足一定的要求，恰巧我日常工作环境又使用 ProxmoxVE 虚拟机，果不其然遇到了一些坑，本文对此进行简要记录。

----------------

### [TinyInst的插桩实现原理分析](papers/TinyInst的插桩实现原理分析)
**(2023.10.12) 开发/代码分析/fuzzing**  
TinyInst 是一个基于调试器原理的轻量级动态检测库，由 Google ProjectZero 团队开源，支持 Windows、macOS、Linux 和 Android 平台。同 DynamoRIO、PIN 工具类似，解决二进制程序动态检测的需求，不过相比于前两者 TinyInst 更加轻量级，更加便于用户理解，更加便于程序员进行二次开发。

本文将通过分析 TinyInst 在 Windows 平台上的插桩源码，来理解 TinyInst 的基本运行原理；为后续调试 TinyInst 的衍生工具(如 Jackalope fuzzing 工具)或二次开发打下基础。

----------------

### [fread函数r和rb模式对比](papers/fread函数r和rb模式对比)
**(2023.07.26) 开发**  
在初学 C 语言时，我们都学会了通过 `fread()` 函数来读取文件内容，也充分理解了需要使用 `r` 模式来打开文本文件，使用 `rb` 模式来打开二进制文件，这样才可以正确读取文件内容。

而实际场景下只有 Windows 系统区分 `r/rb`，Linux 系统不区分；我们在一个将 Linux 项目改写为 Windows 项目的过程中，忽略了该问题，从而导致一系列的无效 DEBUG。

本文以 C 语言的 `stdio` 库的 `fread()` 函数为例，从 `r/rb` 的表现出发，探讨 `r/rb` 的具体的差异细节，并通过源码进行分析校对。

----------------

### [Ubuntu图片查看器EoG的fuzzing](papers/Ubuntu图片查看器EoG的fuzzing)
**(2023.07.14) fuzzing**  
`Eye of Gnome Image Viewer` (EoG) 是 Ubuntu 中的默认图片查看应用程序，作为图片查看器同时开放源码，非常适合 fuzzing 漏洞挖掘入门。

在 2022.12 月学习 fuzzing 时，尝试使用 afl++ 对 EoG 进行漏洞挖掘，虽然整个过程较为简单，但仍有不少值得记录的点，遂在这个时间点进行复盘时重新梳理并整理成文。

----------------

### [折腾P40显卡本地运行LLM的环境](papers/折腾P40显卡本地运行LLM的环境)
**(2023.07.11) LLM**  
2023.6 月，随着开源大模型(LLM: Large Language Model)越来越多，在本地部署大模型成为触手可及的事情，高性能消费级显卡如 4090、3080Ti 可以满足基本的部署需求，当然还可以直接租赁云厂商提供的 GPU 算力。

长时间租赁服务器仍是一个性价比较低的投入，而实验室正好有一台闲置的服务器，几个同事一商量就准备将其配置成一台拥有 GPU 计算卡的服务器。

本文梳理并记录了与同事(@Hcamael / @ghost461)一起使用 NVIDIA P40 显卡配置 LLM 运行环境的折腾过程。

----------------

### [ChatGLM的部署和使用](papers/ChatGLM的部署和使用)
**(2023.07.06) LLM**  
随着 LLaMA 模型的开源，清华大学也推出了专精中文领域的 ChatGLM-6B；ChatGLM-6B 使用了和 ChatGPT 相似的技术，经过约 1T 标识符的中英双语训练，结合监督微调、反馈自助、人类反馈强化学习等技术，最终 62 亿参数的 ChatGLM-6B 已经能生成相当符合人类偏好的回答。

紧随着 ChatGLM-6B 的开源，清华大学又推出了其第二代版本 ChatGLM2-6B，在原有的模型基础之上拥有了更强大的性能、更长的上下文以及更高效的推理。

ChatGLM-6B 模型默认大小(FP16)只需要 13GB 的显存即可运行，经过 INT4 量化最小可达 6GB，完全可以在消费级显卡上搭建自己的 ChatGPT。

本文记录了 ChatGLM-6B 的部署过程以及使用说明。



**[>>>more papers](archives.md)**