## Linux 标准输出编码问题

2017-07-25 17:03:52

<div class="a">最近遇到了一个编码问题，新换了台服务器后，代码在本地运行正常，可部署到服务器上就出现编码错误。初步判断是系统的编码问题，以下测试证实了我的想法：

```python
import sys
print(sys.getdefaultencoding())
print(sys.stdout.encoding)
```
</div>

执行结果：

```
UTF-8
ANSI_X3.4-1968
```

也可以在系统中运行命令 `locale` 查看当前系统的语言和编码。

最终我通过为系统添加环境变量的方法解决了这个问题：

首先执行 `vi /etc/profile` ，然后在文件的末尾添加以下内容：

```shell
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
```

如果想让系统使用中文语言则改为 `zh_CN.UTF-8` 。 

保存文件后执行 `source /etc/profile` 来让更改立即生效。

 如果这时使用 supervisor 启动应用依然出错，则可完全退出 supervisor 后重启：

```
$ supervisorctl shutdown
$ supervisord
```

