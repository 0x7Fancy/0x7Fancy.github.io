## 构建Linux下的可移植Python环境

Time: 2019.07.04  
Tags: 开发  
PublicFiles: py2pyc.py,Setup.local  

### 0x00 前言
在某些情况下，我们可能需要一个即插即用的 Python 环境。

Python 官方提供了 Windows 的可移植版本，eg: `Windows x86-64 embeddable zip file`，也就是带有 `embeddable` 字符串的版本；但没有提供 Linux 环境下的。

本文介绍如何在 Linux 环境下静态编译 Python，制作 portable 版本。


### 0x01 编译环境

	Linux Centos7 x64
	Gcc version 4.8.5
	Python source 3.7

依赖组件按照错误提示进行补充安装。


### 0x02 静态编译
静态编译过程可以直接参考官方提供的文档：<https://wiki.python.org/moin/BuildStatically>；我们这里按照官方提供的步骤，逐步进行并补充说明。

**1.编译配置**  
执行 `configure` 进行编译前配置：

	# cd Python-3.7.3
	# ./configure LDFLAGS="-static" --disable-shared --enable-optimizations
	
参数说明：

	LDFLAGS="-static" => 设置为静态编译
	--disable-shared  => 不编译 python 的动态链接库
	--enable-optimizations  => 开启优化

**2.配置需要静态编译的库**  
实际上，在完成上一步后，就已经可以进行编译了：

	make LDFLAGS="-static" LINKFORSHARED=" "

但在上一步中我们设置了 `--disable-shared`，那么编译出来的 `python` 可执行文件是没有动态链接库支持的，如 `import socket` 也无法处理。

所以在编译前，我们必须要先对静态编译的模块进行配置，访问 `src/Modules/Setup.local` 文件：

	vim Modules/Setup.local

在首部注释后的第一行添加，表示后续的模块将被编译到 `python` 二进制中：

	*static*
	
紧接着添加需要的模块，如：

	math mathmodule.c _math.c # -lm # math library functions, e.g. sin()

想要添加其他的模块，参考 `src/Modules/Setup.dist` 文件，找到模块所对应的行(当然在该文件中，这些行是被注释的)，将这些行复制到 `Setup.local` 中，并去掉注释。

我们编写好的 `Setup.local` 文件，支持了大多数情况的使用，可以参考附件里的 [Setup.local]()


**3.编译**  
在完成上述配置后，可以进行编译，并得到支持模块的 `python` 二进制：

	make LDFLAGS="-static" LINKFORSHARED=" "

编译后的 `python` 二进制稍微大了些，使用 `strip` 裁剪下：

	# ls -lh python
	-rwxr-xr-x 1 root root 18M Jul  4 13:24 python
	# strip -s python
	# ls -lh python
	-rwxr-xr-x 1 root root 6.4M Jul  4 13:25 python


### 0x03 添加标准库
编译后的 `python` 二进制，在脱离编译目录的情况下，执行会发生错误：

	# cp python ~/python37 ; cd ~/python37
	# ./python
	Could not find platform independent libraries <prefix>
	Could not find platform dependent libraries <exec_prefix>
	Consider setting $PYTHONHOME to <prefix>[:<exec_prefix>]
	Fatal Python error: initfsencoding: unable to load the file system codec
	ModuleNotFoundError: No module named 'encodings'

	Current thread 0x00000000013688c0 (most recent call first):
	Aborted

原因是其缺少标准库文件的支持，我们复制编译目录下的 python 标准库：

	# cp -r Python-3.7.3/Lib ~/python37/lib/python3.7

目录结构如下：

	.
	|-- lib
	|   `-- python3.7
	`-- python37_x64

到这里为止，我们制作完成了 portable 版本的 python。在使用该版本时，需要先添加环境变量：

	# export PYTHONHOME=/root/python37/
	# ./python37_x64 
	Python 3.7.3 (default, Jul  4 2019, 14:34:33) 
	[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
	Type "help", "copyright", "credits" or "license" for more 	information.
	>>> 


### 0x04 最小化标准库
如果环境对 portable 的大小有限制，我们就需要减少容量，其中 `python` 二进制已经去除符号表了，所以我们只能对标准库进行裁剪，下面提供了些思路和方法。

**1.删减标准库**  
在某些环境下，我们可能用不到标准库中所有的组件，所以我们可以根据需求，对标准库中的内容进行删减，就可以减少 portable 版本的大小。

**2.编译pyc**  
python 支持对 `*.pyc` 的脚本进行加载，所以我们可以将标准库中的 `*.py` 都编译为 `*.pyc`，来减少存储空间。

使用标准库中的 `py_compile.py` 模块进行编译，eg：编译 `base64.py`：

	# ./python37_x64 -m py_compile lib/python3.7/base64.py
	[生成 =>]
	lib/python3.7/__pycache__/base64.cpython-37.pyc

随后，我们删除 `base64.py` 文件，该 `pyc` 文件重命名为 `base64.pyc`，然后放置在原来的位置 `lib/python3.7/`，删除 `__pycache__` 临时文件。

比较两文件的大小：

	20K lib/python3.7/base64.py
	17K lib/python3.7/base64.pyc

当然我们需要对 `lib` 库下的所有文件执行该操作，批量处理可以参考脚本 [py2pyc.py]()

>附：可以使用 `compileall.py` 模块，一次性编译所有的文件，然后再执行重命名、移动等操作。


**3.压缩打包**  
`python` 支持对 zip 方式压缩的 `Lib` 目录解析，所以我们使用这种方式进一步减少 portable 版本的大小。

在上一步中使用 [py2pyc.py]() 脚本，生成了完整编译后的目录 `pyc/[path]`，使用 `zip` 对目录进行压缩：

	# cd pyc/python3.7
	# zip -r python37.zip *

拷贝 `python37.zip` 到 `lib` 目录下，删除展开的 `lib/python3.7` 目录，最终目录结构如下：

	.
	|-- lib
	|   `-- python37.zip
	`-- python37_x64

运行演示：
	
	# ./python37_x64 
	Python 3.7.3 (default, Jul  4 2019, 14:34:33) 
	[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
	Type "help", "copyright", "credits" or "license" for more 	information.
	>>> 
	
比较压缩前后的 `lib` 库大小：

	[原始 Lib 目录]
	42M		Lib/
	[全部编译为 pyc 的目录]
	25M		python3.7
	[将 pyc 进行压缩打包]
	8.0M 	python37.zip
	
### 0x05References
<https://www.python.org>  
<https://wiki.python.org/moin/BuildStatically>  
<http://xiaoxia.org/2013/09/13/python-on-tomato/>  
<https://www.blackh4t.org/2018/02/06/how-to-compile-static-link-python/>  