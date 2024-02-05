## Lucky勒索病毒分析与文件解密  

Time: 2018.12.04  
Tags: 逆向分析,恶意软件  
Author: Hcamael & 0x7F@knownsec404  
Refer: https://paper.seebug.org/758/  


### 0x00 前言

近日，互联网上爆发了一种名为 lucky 的勒索病毒，该病毒会将指定文件加密并修改后缀名为 `.lucky`。

知道创宇 404 实验室的炼妖壶蜜罐系统最早于 2018.11.10 就捕捉到该勒索病毒的相关流量，截止到 2018.12.04 日，该病毒的 CNC 服务器依然存活。

根据分析的结果可以得知 lucky 勒索病毒几乎就是 Satan 勒索病毒，整体结构并没有太大改变，包括 CNC 服务器也没有更改。Satan 病毒一度变迁：最开始的勒索获利的方式变为挖矿获利的方式，而新版本的 lucky 勒索病毒结合了勒索和挖矿。

知道创宇 404 实验室在了解该勒索病毒的相关细节后，迅速跟进并分析了该勒索病毒；着重分析了该病毒的加密模块，并意外发现可以利用伪随机数的特性，还原加密密钥，并成功解密了文件，Python 的解密脚本链接： <https://github.com/knownsec/Decrypt-ransomware>。

本文对 lucky 勒索病毒进行了概要分析，并着重分析了加密流程以及还原密钥的过程。


### 0x01 lucky 病毒简介
lucky 勒索病毒可在 Windows 和 Linux 平台上传播执行，主要功能分为「文件加密」、「传播感染」与「挖矿」。

**文件加密**  
lucky 勒索病毒遍历文件夹，对如下后缀名的文件进行加密，并修改后缀名为 `.lucky`：

	bak,sql,mdf,ldf,myd,myi,dmp,xls,xlsx,docx,pptx,eps,
	txt,ppt,csv,rtf,pdf,db,vdi,vmdk,vmx,pem,pfx,cer,psd

为了保证系统能够正常的运行，该病毒加密时会略过了系统关键目录，如：

	Windows: windows, microsoft games, 360rec, windows mail 等等
	Linux: /bin/, /boot/, /lib/, /usr/bin/ 等等

**传播感染**  
lucky 勒索病毒的传播模块并没有做出新的特色，仍使用了以下的漏洞进行传播：

	1.JBoss反序列化漏洞(CVE-2013-4810)
	2.JBoss默认配置漏洞(CVE-2010-0738)
	3.Tomcat任意文件上传漏洞（CVE-2017-12615）
	4.Tomcat web管理后台弱口令爆破
	5.Weblogic WLS 组件漏洞（CVE-2017-10271）
	6.Windows SMB远程代码执行漏洞MS17-010
	7.Apache Struts2远程代码执行漏洞S2-045
	8.Apache Struts2远程代码执行漏洞S2-057

**挖矿**  
该勒索病毒采用自建矿池地址：`194.88.105.5:443`，想继续通过挖矿获得额外的收益。同时，该矿池地址也是 Satan 勒索病毒变种使用的矿池地址。

**运行截图**  
<div align="center">
<img src="Images/Image1.png" width="400">
</div>


### 0x02 病毒流程图
lucky 勒索病毒的整体结构依然延续 Satan 勒索病毒的结构，包括以下组件：

	预装载器：fast.exe/ft32，文件短小精悍，用于加载加密模块和传播模块
	加密模块：cpt.exe/cry32，加密模块，对文件进行加密
	传播模块：conn.exe/conn32，传播模块，利用多个应用程序漏洞进行传播感染
	挖矿模块：mn32.exe/mn32，挖矿模块，连接自建矿池地址
	服务模块：srv.exe，在 windows 下创建服务，稳定执行

流程图大致如下：

<div align="center">
<img src="Images/Image2.png" width="500">
</div>

lucky 勒索病毒的每个模块都使用了常见的壳进行加壳保护，比如 `UPX`，`MPRESS`，使用常见的脱壳软件进行自动脱壳即可。


### 0x03 加密流程
对于一个勒索病毒来说，最重要的就是其加密模块。在 lucky 勒索病毒中，加密模块是一个单独的可执行文件，下面对加密模块进行详细的分析。(以 Windows 下的 `cpt.exe` 作为分析样例)

**1.脱去upx**  
`cpt.exe` 使用 upx 进行加壳，使用常见的脱壳工具即可完成脱壳。

**2.加密主函数**  
使用 IDA 加载脱壳后的 `cpt.exe.unp`，在主函数中有大量初始化的操作，忽略这些操作，跟入函数可以找到加密逻辑的主函数，下面对这些函数进行标注：

<div align="center">
<img src="Images/Image3.png" width="400">
</div>

`generate_key`: 生成 60 位随机字符串，用于后续加密文件。  
`wait_sleep`: 等待一段时间。  
`generate_session`: 生成 16 位随机字符串，作为用户的标志(session)。  
`lucky_crypto_entry`: 具体加密文件的函数。   
`send_info_to_server`: 向服务器报告加密完成。  

大致的加密流程就是函数标注的如此，最后写入一个文件 `c:\\_How_To_Decrypt_My_File_.Dic`，通知用户遭到了勒索软件加密，并留下了比特币地址。

**3.generate_key()**  
该函数是加密密钥生成函数，利用随机数从预设的字符串序列中随机选出字符，组成一个长度为 60 字节的密钥。

<div align="center">
<img src="Images/Image4.png" width="300">
</div>

`byte_56F840` 为预设的字符串序列，其值为：

	ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789

**4.generate_session()**  
加密模块中使用该函数为每个用户生成一个标识，用于区分用户；其仍然使用随机数从预设的字符串序列中随机选出字符，最后组成一个长度为 16 字节的 session，并存入到 `C:\\Windows\\Temp\\Ssession` 文件下。

<div align="center">
<img src="Images/Image5.png" width="400">
</div>

其中 `byte_56F800` 字符串为：

	ABCDEFGHIJPQRSTUVWdefghijklmnopqrstuvwx3456789


**5.lucky\_crypto\_entry()**  
###### 文件名格式
该函数为加密文件的函数入口，提前拼接加密文件的文件名格式，如下：

<div align="center">
<img src="Images/Image6.png" width="400">
</div>

被加密的文件的文件名格式如下：

	[nmare@cock.li]filename.AiVjdtlUjI9m45f6.lucky

其中 `filename` 是文件本身的名字，后续的字符串是用户的 session。

###### 通知服务器
在加密前，还会首先向服务器发送 HTTP 消息，通知服务器该用户开始执行加密了：

<div align="center">
<img src="Images/Image7.png" width="400">
</div>

HTTP 数据包格式如下：

	GET /cyt.php?code=AiVjdtlUjI9m45f6&file=1&size=0&sys=win&VERSION=4.4&status=begin HTTP/1.1

###### 文件筛选
在加密模块中，lucky 对指定后缀名的文件进行加密：

<div align="center">
<img src="Images/Image8.png" width="400">
</div>

被加密的后缀名文件包括：

	bak,sql,mdf,ldf,myd,myi,dmp,xls,xlsx,docx,pptx,eps,
	txt,ppt,csv,rtf,pdf,db,vdi,vmdk,vmx,pem,pfx,cer,psd

**6.AES_ECB 加密方法**  
lucky 使用先前生成的长度为 60 字节的密钥，取前 32 字节作为加密使用，依次读取文件，按照每 16 字节进行 `AEC_ECB` 加密。

<div align="center">
<img src="Images/Image9.png" width="400">
</div>

除此之外，该勒索病毒对于不同文件大小有不同的处理，结合加密函数的上下文可以得知，这里我们假设文件字节数为 n：

1. 对于文件末尾小于 16 字节的部分，不加密
2. 若 n > 10000000 字节，且当 n > 99999999 字节时，将文件分为 n / 80 个块，加密前 n / 16 个块
3. 若 n > 10000000 字节，且当 99999999 <= n <= 499999999 字节时，将文件分为 n / 480 个块，加密前 n / 16 个块
4. 若 n > 10000000 字节，且当 n > 499999999 字节时，将文件分为 n / 1280 个块，加密前 n / 16 个块

对于每个文件在加密完成后，lucky 病毒会将用于文件加密的 AES 密钥使用 RSA 算法打包并添加至文件末尾。

**7.加密完成**  
在所有文件加密完成后，lucky 再次向服务器发送消息，表示用户已经加密完成；并在 `c:\\_How_To_Decrypt_My_File_.Dic`，通知用户遭到了勒索软件加密。

加密前后文件对比：

<div align="center">
<img src="Images/Image10.png" width="400">
</div>


### 0x04 密钥还原
在讨论密钥还原前，先来看看勒索病毒支付后流程。

如果作为一个受害者，想要解密文件，只有向攻击者支付 1BTC，并把被 RSA 算法打包后的 AES 密钥提交给攻击者，攻击者通过私钥解密，最终返回明文的 AES 密钥用于文件解密；可惜的是，受害者即便拿到密钥也不能立即解密，lucky 勒索病毒中并没有提供解密模块。

勒索病毒期待的解密流程：
<div align="center">
<img src="Images/Image11.png" width="300">
</div>

**那么，如果能直接找到 AES 密钥呢？**

在完整的分析加密过程后，有些的小伙伴可能已经发现了细节。AES 密钥通过 `generate_key()` 函数生成，再来回顾一下该函数：

<div align="center">
<img src="Images/Image4.png" width="300">
</div>

利用当前时间戳作为随机数种子，使用随机数从预设的字符串序列中选取字符，组成一个长度为 60 字节的密钥。

**随机数=>伪随机数**  
有过计算机基础的小伙伴，应该都知道计算机中不存在真随机数，所有的随机数都是伪随机数，而伪随机数的特征是「对于一种算法，若使用的初值(种子)不变，那么伪随机数的数序也不变」。所以，如果能够确定 `generate_key()` 函数运行时的时间戳，那么就能利用该时间戳作为随机种子，复现密钥的生成过程，从而获得密钥。

**确定时间戳**  
###### 爆破
当然，最暴力的方式就是直接爆破，以秒为单位，以某个有标志的文件(如 PDF 文件头)为参照，不断的猜测可能的密钥，如果解密后的文件头包含 `%PDF`(PDF 文件头)，那么表示密钥正确。

###### 文件修改时间
还有其他的方式吗？文件被加密后会重新写入文件，所以从操作系统的角度来看，被加密的文件具有一个精确的修改时间，可以利用该时间以确定密钥的生成时间戳：

<div align="center">
<img src="Images/Image12.png" width="250">
</div>

如果需要加密的文件较多，加密所花的时间较长，那么被加密文件的修改时间就不是生成密钥的时间，应该往前推移，不过这样也大大减少了猜测的范围。

###### 利用用户 session
利用文件修改时间大大减少了猜测的范围；在实际测试中发现，加密文件的过程耗时非常长，导致文件修改时间和密钥生成时间相差太多，而每次都需要进行检查密钥是否正确，需要耗费大量的时间，这里还可以使用用户 session 进一步缩小猜测的范围。

回顾加密过程，可以发现加密过程中，使用时间随机数生成了用户 session，这就成为了一个利用点。利用时间戳产生随机数，并使用随机数生成可能的用户 session，当找到某个 session 和当前被加密的用户 session 相同时，表示该时刻调用了 `generate_session()` 函数，该函数的调用早于文件加密，晚于密钥生成函数。

<div align="center">
<img src="Images/Image13.jpg" width="350">
</div>

找到生成用户session 的时间戳后，再以该时间为起点，往前推移，便可以找到生成密钥的时间戳。

补充：实际上是将整个还原密钥的过程，转换为寻找时间戳的过程；确定时间戳是否正确，尽量使用具有标志的文件，如以 PDF 文件头 `%PDF` 作为明文对比。

**还原密钥**  
通过上述的方式找到时间戳，利用时间戳就可以还原密钥了，伪代码如下：

	sequence = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
	key = []
	timestamp = 1542511041
	srand(timestamp)
	for (i = 0; i < 60; i++) {
		key[i] = sequence[rand() % 0x3E]
	}

**文件解密**  
拿到了 AES 密钥，通过 AES_ECB 算法进行解密文件即可。

其中注意两点：

	1. 解密前先去除文件末尾的内容(由 RSA 算法打包的密钥内容)
	2. 针对文件大小做不同的解密处理。


### 0x05 总结
勒索病毒依然在肆掠，用户应该对此保持警惕，虽然 lucky 勒索病毒在加密环节出现了漏洞，但仍然应该避免这种情况；针对 lucky 勒索病毒利用多个应用程序的漏洞进行传播的特性，各运维人员应该及时对应用程序打上补丁。

除此之外，知道创宇 404 实验室已经将文中提到的文件解密方法转换为了工具，若您在此次事件中，不幸受到 lucky 勒索病毒的影响，可以随时联系我们。


### 0x06 References
tencent: <https://s.tencent.com/research/report/571.html>  
绿盟: <https://mp.weixin.qq.com/s/uwWTS_ta29YlYntaZN3omQ>  
深信服: <https://mp.weixin.qq.com/s/zA1bK1sLwaZsUvuOzVHBKg>  
Python 的解密脚本:  <https://github.com/knownsec/Decrypt-ransomware>