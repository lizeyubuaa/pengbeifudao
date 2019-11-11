# **容器(container)、可迭代对象(iterable)、迭代器(iterator)、生成器(generator)、列表/集合/字典推导式(list,set,dict comprehension)**

![relations](http://img2.foofish.net/relationships.png)

# 容器(container)

容器是一种把多个元素组织在一起的==数据结构类型==。是一种通俗的叫法，不针对具体的一种数据结构。

## 特点：

1.容器中的元素可以逐个地==迭代获取==。
2.可以用in, not in关键字判断元素==是否包含==在容器中。
3.==通常==这类数据结构把所有的元素存储在内存中（也有一些特例，并不是所有的元素都放在内存，比如==迭代器和生成器==对象）

## 常见的容器对象有：

- list, deque, ....
- set, frozensets, ....
- dict, defaultdict, OrderedDict, Counter, ....
- tuple, namedtuple, …
- str

## 判断：

从技术角度来说，当它可以用来==询问某个元素是否包含在其中==时，那么这个对象就==可以认为是==一个容器。

```
assert 1 in [1, 2, 3]      # lists
assert 4 not in [1, 2, 3]
assert 1 in {1, 2, 3}      # sets
assert 4 not in {1, 2, 3}
assert 1 in (1, 2, 3)      # tuples
assert 4 not in (1, 2, 3)
```

询问某元素是否在dict中（是否作为dict的key）：

```
d = {1: 'foo', 2: 'bar', 3: 'qux'}
assert 1 in d
assert 'foo' not in d  # 'foo' 不是dict中的元素
```

询问某substring是否在string中：

```
s = 'foobar'
assert 'b' in s
assert 'x' not in s
assert 'foo' in s 
```

## 注意：

1.尽管绝大多数容器都提供了某种方式来获取其中的每一个元素，但这并不是容器本身提供的能力，而是==**可迭代对象**赋予了容器这种能力==
2.==不是所有的容器都是可迭代的==，比如：[Bloom filter](https://zh.wikipedia.org/wiki/布隆过滤器)，虽然Bloom filter可以用来检测某个元素是否包含在容器中，但是并不能从容器中获取其中的每一个值，因为Bloom filter压根就没把元素存储在容器中，而是通过一个==散列函数映射==成一个值保存在数组中。

# 迭代对象和迭代器

## 0.迭代（遍历、循环）

iteration是用==for...in...==的循环语法访问容器中元素的⼀种==方式==。

## 1.可迭代对象iterbale

1==可迭代对象（Iterable）可以通过for...in...这类语句迭代读取⼀条数据供我们使⽤==
2可迭代对象（Iterable）使用isinstance函数来判断

```python
from    collections    import    Iterable
isinstance([],Iterable)#list
True
isinstance({},Iterable)#set
True
isinstance('abc',Iterable)#string
True    
isinstance(100,Iterable)#整数
False
```

3==具备了  \_\_iter\_\_ ⽅法、可以返回一个**迭代器**的对象是⼀个可迭代对象==

```
x = [1, 2, 3]
y = iter(x)
z = iter(x)
next(y)
1
next(y)
2
next(z)
1
type(x)
<class 'list'>
type(y)
<class 'list_iterator'>
```

这里x是一个可迭代对象，y和z是两个独立的迭代器。迭代器==内部持有一个状态==，该状态用于==记录当前迭代所在的位置==，以方便下次迭代的时候获取正确的元素。==迭代器有一种具体的迭代器类型==，比如list_iterator，set_iterator。

4迭代⼀个可迭代对象的时候，实际上就是==先获取该对象提供的⼀个迭代器iterator，然后通过这个迭代器来依次读取对象中的每⼀个数据==。

当运行代码：

```
x = [1, 2, 3]
for elem in x:
    ...
```

实际执行情况是： 
![iterable-vs-iterator.png](http://img2.foofish.net/iterable-vs-iterator.png)

反编译该段代码，你可以看到解释器显示地调用GET_ITER指令，相当于调用iter(x)，FOR_ITER指令就是调用next()方法，不断地获取迭代器中的下一个元素，但是你没法直接从指令中看出来，因为他被解释器优化过了。

```
>>> import dis
>>> x = [1, 2, 3]
>>> dis.dis('for _ in x: pass')
  1           0 SETUP_LOOP              14 (to 17)
              3 LOAD_NAME                0 (x)
              6 GET_ITER
        >>    7 FOR_ITER                 6 (to 16)
             10 STORE_NAME               1 (_)
             13 JUMP_ABSOLUTE            7
        >>   16 POP_BLOCK
        >>   17 LOAD_CONST               0 (None)
             20 RETURN_VALUE
```

5常见的可迭代对象：很多容器（列表，集合，字典，元组，字符串）和很多对象（==处于打开状态的files，sockets==）

### 3.迭代器iterator

1.==迭代器iterator==是⼀个==可以记住遍历的位置的对象==。
==2.迭代器在调用next()方法的时候返回容器中的下一个值，只能往前不会后退==。
3.任何实现了__iter__和__next__()方法的对象都是迭代器，__iter__返回迭代器自身，__next__返回容器中的下一个值，如果容器中没有更多元素了，则抛出StopIteration异常。

## 关于迭代器的例子，

比如itertools函数返回的都是迭代器对象。

生成无限序列：

```
>>> from itertools import count
>>> counter = count(start=13)
>>> next(counter)
13
>>> next(counter)
14
```

从一个有限序列中生成无限序列：

```
>>> from itertools import cycle
>>> colors = cycle(['red', 'white', 'blue'])
>>> next(colors)
'red'
>>> next(colors)
'white'
>>> next(colors)
'blue'
>>> next(colors)
'red'
```

从无限的序列中生成有限序列：

```
>>> from itertools import islice
>>> colors = cycle(['red', 'white', 'blue'])  # infinite
>>> limited = islice(colors, 0, 4)            # finite
>>> for x in limited:                         
...     print(x)
red
white
blue
red
```

## 自定义迭代器：

为了更直观地感受迭代器内部的执行过程，我们自定义一个迭代器，以斐波那契数列为例：

```
class Fib:
    def __init__(self):
        self.prev = 0
        self.curr = 1

    def __iter__(self):
        return self

    def __next__(self):
        value = self.curr
        self.curr += self.prev
        self.prev = value
        return value

f = Fib(10)
for num in f:
	print(num)
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

Fib既是一个可迭代对象（因为它实现了__iter__方法），又是一个迭代器（因为实现了__next__方法）。实例变量prev和curr用户维护迭代器内部的状态。每次调用next()方法的时候做两件事：

1. 为==下一次==调用next()方法==修改状态==
2. 为==当前这次==调用生成返回结果

==迭代器只能往前不会后退==。

# 生成器——“惰性计算”

生成器一定是迭代器（反之不成立），因此任何生成器也是以一种懒加载的模式生成值。

## ==创建一个generator==，有2种方法。

1.第一种方法很简单，只要把一个列表生成式的[]改成()，就创建了一个generator：

```
L = [x * x for x in range(10)]
L
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
g = (x * x for x in range(10))
g
<generator object <genexpr> at 0x1022ef630>
```

创建L和g的区别仅在于最外层的[]和()，L是一个list，而g是一个generator。

2.如果推算的算法比较复杂，还可以==用函数==来实现。

## 案例：斐波拉契数列（Fibonacci）

```
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        a, b = b, a + b
        print(b) => yild b
        n = n + 1
    return 'done'
```

如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator：

## 打印出generator的每一个元素

1.可以通过next()函数获得generator的下一个返回值：

```
f = Fibonacci(5)
for i in range(6):
    print(next(f))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

2.使用for循环，因为generator也是迭代器(iterator)：

```
f = Fibonacci(5)
for num in f:
	print(num)
```

​		我们创建了一个generator后，==基本上永远不会调用==next()，而是通过for循环来迭代它，并且不需要关心StopIteration的错误。

## 区别：

函数是顺序执行，遇到return语句或者最后一行函数语句就返回。
generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从==上次返回的yield语句处==继续执行。

generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。

