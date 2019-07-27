<p align="center">
    <img src="https://user-images.githubusercontent.com/19553554/61995478-bd21e980-b0bb-11e9-8206-5a5958e27b25.png" alt="Linux logo" width=200 />
</p>

<h1 align="center">📝 how</h1>
<p align="center">
    <em>Impressive Linux commands cheat sheet.</em>
</p>

### 🔰 安装

**pip 安装**
```bash
$ pip install how
```

**源码安装**
```bash
$ git clone https://github.com/chenjiandongx/how.git
$ cd how
$ pip install -r requirements.txt
$ python setup.py install
```

### 📝 使用

```bash
$ how
usage: how [-h] [-i] [-v] [COMMAND [COMMAND ...]]

Lovely Linux commands cheat sheet.

positional arguments:
  COMMAND        the puzzling command

optional arguments:
  -h, --help     show this help message and exit
  -i, --init     initialize all commands
  -v, --version  displays the current version of `how`
```

**示例**
```shell
$ how man
# man

查看 Linux 中的指令帮助

##  补充说明

man 命令 是 Linux 下的帮助指令，通过 man 指令可以查看 Linux 中的指令帮助、配
置文件帮助和编程帮助等信息。

###  语法

man(选项)(参数)

###  选项

-a：在所有的 man 帮助手册中搜索；
-f：等价于 whatis 指令，显示给定关键字的简短描述信息；
-P：指定内容时使用分页程序；
-M：指定 man 手册搜索的路径。

###  参数

-数字：指定从哪本 man 手册中搜索帮助； -关键字：指定要搜索帮助的关键字。

###  数字代表内容

1：用户在 shell 环境可操作的命令或执行文件；
2：系统内核可调用的函数与工具等
3：一些常用的函数(function) 与函数库(library)，大部分为 C 的函数库(libc)
4：设备文件说明，通常在/dev 下的文件
5：配置文件或某些文件格式
6：游戏(games)
7：惯例与协议等，如 Linux 文件系统，网络协议，ASCII code 等说明
8：系统管理员可用的管理命令
9：跟 kernel 有关的文件

###  实例

我们输入 man ls，它会在最左上角显示“LS（1）”，在这里，“LS”表示手册名称，而“（1）
”表示该手册位于第一节章，同样，我们输 man ifconfig 它会在最左上角显示“IFCONFIG（8）”。也可以这样输入命令：“man[章节号] 手册名称”。

man 是按照手册的章节号的顺序进行搜索的，比如：

man sleep

只会显示 sleep 命令的手册,如果想查看库函数 sleep，就要输入:

man 3 sleep
```

### 📅 Changelog

#### V0.1.0 - 2019-07-27
* Alpha: 第一个正式版发布

### 📃 LICENSE

MIT [©chenjiandongx](https://github.com/chenjiandongx)
