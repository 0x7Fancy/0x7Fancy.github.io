<div align="center">

[**Home**](./README.md) / [**Tags**](./tags.md) / [**Archives**](./archives.md) / [**Reviews**](https://github.com/0x7Fancy/0x7Fancy.github.io/issues) / [**About**](./about.md)
</div>

## **Home**

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

----------------

### [StableDiffusion的cpu推理使用](papers/StableDiffusion的cpu推理使用)
**(2023.06.27) 其他**  
ChatGPT 的爆火督促我去接触学习一些大模型的基本原理，在这过程中又看到很多小伙伴用 Stable Diffusion 工具文生图玩得不亦乐乎，虽然 Stable Diffusion 采用的是扩散模型，不过也想借此机会尝试一下。

不过我没有推荐配置的显卡，好在 Stable Diffusion 也支持使用 CPU 进行推理，只是速度慢一些，用于学习场景足够了。本文将详细介绍工具搭建流程以及基本使用。

----------------

### [搭建基于llama.cpp的LLaMA模型](papers/搭建基于llama.cpp的LLaMA模型)
**(2023.06.26) LLM**  
ChatGPT 从 2022.12 月掀起了大模型人工智能的浪潮，随后在一段时间内，各大团队都开源了自家的大模型，这无疑是入门学习大模型的好机会；但是大模型基本都需要大显存的显卡作为硬件支持，按时付费租赁云厂商的机器是个不错的选择，不过大神 Georgi Gerganov 根据 Meta 开源的 Python LLaMA 推理代码重写了 C++ 的版本 `llama.cpp`，可在 MacOS 和 Linux 平台上使用 CPU 进行推理。

随后伴随着 Meta LLaMA 模型的泄露，结合 llama.cpp 我们就可以在本地不需要显卡搭建部署大模型。

本文将以入门学习大模型的角度，详细介绍 llama.cpp 的搭建流程以及使用示例。

----------------

### [基于快照的fuzz工具wtf的基础使用](papers/基于快照的fuzz工具wtf的基础使用)
**(2023.06.15) fuzzing**  
wtf (https://github.com/0vercl0k/wtf) 是一种分布式、代码覆盖引导、可定制、基于快照的跨平台模糊器，设计用于 fuzz 在 Microsoft Windows 平台上运行的用户模式或内核模式的目标。

在日常的 fuzz 的工作中，通常我们都需要先大致分析目标软件，然后对其输入点构造 harness，才可以使用工具对 harness 进行 fuzz，从而发现目标软件的潜在漏洞。构造 harness 不是一件容易的事情，这取决于安全研究人员分析解构目标软件的程度，除此之外，在部分软件中，只有进行完整的、复杂的初始化操作和预设，才能保证 harness 调用的输入点函数能够正常运行。

针对这一问题，基于快照的 fuzz 工具 wtf 吸引了我的注意；我们可以对正常运行的目标软件打下内存快照，然后对该内存快照进行 fuzz，这种方式可以不必编写 harness，并在一定程度上减少分析目标软件的成本。

本文从基于快照这一个特性出发，介绍 wtf 工具的基础使用和注意事项。



**[>>>more papers](archives.md)**