##Python 中的迟绑定 (late binding)

2017-07-26 11:25:31

<div class="a">

> Python 只有在需要时才去寻找变量的值

定义一个函数：
```python
def example(x):
    return x * var
```
变量 var 尚不存在，然而 python 并不会在执行 def 语句的时候报错。在这个阶段 python 并不会去寻找变量 var 的值。</div>

当调用这个函数时：
```python
example(6)
NameError: global name 'var' is not defined
```
现在报错了，所以 python 只有在你调用 example 函数时才会寻找 var 变量。
```python
var = 10
example(6)
60# var is referring to 10

var = 20
example(6)
120# var is referring to 20
```
现在我们来判断一下这两段代码的执行结果：
```python
def foo(y):
    return lambda y : y * 2
print(foo(4)(1))

def bar(y):
    return lambda x : y * 2
print(bar(4)(1))
```
第一段代码结果为 2，因为在 lambda 函数被调用时 y 的值为 1。
第二段代码结果为 8，因为在 lambda 函数被调用时 y 的值为 4。

下面这段代码被视为 Python 程序员常犯的错误：
```python
def create_multipliers():
    return [lambda x : i * x for i in range(5)]
for multiplier in create_multipliers():
    print multiplier(2)
```
预期的结果：
```python
0
2
4
6
8
```
实际执行结果却是：
```python
8
8
8
8
8
```
在了解了 python 迟绑定的特性之后可以判断是因为在 lambda 函数实际执行的时候循环早已结束，而此时的 i 等于 4。

如果想达到预期的效果可以这样写：

```python
def create_multipliers():
    return [lambda x, i = i : i * x for i in range(5)]
for multiplier in create_multipliers():
    print multiplier(2)
```
这样，lambda 函数中的 i 就在每次循环中被赋值了。
