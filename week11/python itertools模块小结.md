# Python-进阶-itertools模块小结

itertools用于高效循环的迭代函数集合

## 第一部分

### itertools.count(start=0, step=1)

创建一个迭代器，==生成从start开始的连续整数（无限序列）==，如果忽略start，则从0开始计算（注意：此迭代器不支持长整数，==支持浮点数==）。

使用

```
from itertools import *

# 和zip函数返回的结果相同
for i in izip(count(1), ['a', 'b', 'c']):
    print i

(1, 'a')
(2, 'b')
(3, 'c')
```

### itertools.cycle(iterable)

创建一个迭代器，==对iterable中的元素反复执行循环操作==，内部会生成iterable中的元素的一个副本，此==副本用于返回循环中的重复项==。

使用

```
from itertools import *

i = 0
for item in cycle(['a', 'b', 'c']):
    i += 1
    if i == 10:
        break
    print (i, item)

(1, 'a')
(2, 'b')
(3, 'c')
(4, 'a')
(5, 'b')
(6, 'c')
(7, 'a')
(8, 'b')
(9, 'c')
```

### itertools.repeat(object[, times])

创建一个迭代器，==重复生成object==，times（如果已提供）指定重复计数，如果未提供times，将==无止尽返回该对象==。

使用

```
from itertools import *

for i in repeat('over-and-over', 5):
    print i

over-and-over
over-and-over
over-and-over
over-and-over
over-and-over
```

## 第二部分

### itertools.chain(*iterables)

==将多个迭代器作为参数, 但只返回单个迭代器==, 它==产生所有参数迭代器的内容==, 就好像他们是来自于一个单一的序列.

注意：可以只传入一个迭代器

使用

```
from itertools import *

for i in chain([1, 2, 3], ['a', 'b', 'c']):
    print i
1
2
3
a
b
c


from itertools import chain, imap
# f是函数，items是参数列表
def flatmap(f, items):
	# 只传入了一个迭代器
    return chain.from_iterable(imap(f, items))
>>> list(flatmap(os.listdir, dirs))
>>> ['settings.py', 'wsgi.py', 'templates', 'app.py',
     'templates', 'index.html, 'config.json']
```

### itertools.compress(data, selectors)

提供一个==选择列表selectors==，==对原始数据进行筛选==

```
def compress(data, selectors):
    # compress('ABCDEF', [1,0,1,0,1,1]) --> A C E F
    return (d for d, s in izip(data, selectors) if s)
```

### itertools.dropwhile(predicate, iterable)

创建一个迭代器，==只要函数predicate(item)为True，就丢弃iterable中的项，如果predicate返回False，就会生成iterable中的项和所有后续项。==

即：在条件为false之后的第一次, 返回迭代器中剩下来的项.

使用

```
from itertools import *

def should_drop(x):
    print 'Testing:', x
    return (x<1)

for i in dropwhile(should_drop, [ -1, 0, 1, 2, 3, 4, 1, -2 ]):
    print 'Yielding:', i

Testing: -1
Testing: 0
Testing: 1
Yielding: 1
Yielding: 2
Yielding: 3
Yielding: 4
Yielding: 1
Yielding: -2
```

### itertools.groupby(iterable[, key])

返回一个产生==按照key进行分组后的值集合==的迭代器.

此函数返回的迭代器生成元素(key, group)，其中key是分组的键值，group是迭代器，生成组成该组的所有项。即：按照keyfunc函数对序列每个元素执行后的结果分组(每个分组是一个迭代器), 返回这些分组的迭代器.

注意：iterable==必须按照key函数升序排列==。

应用

```
from itertools import *
qs = [{'date' : 1},{'date' : 2}]
[(name, list(group)) for name, group in groupby(qs, lambda p:p['date'])]

[(1, [{'date': 1}]), (2, [{'date': 2}])]


>>> from itertools import *
>>> a = ['aa', 'ab', 'abc', 'bcd', 'abcde']
>>> for i, k in groupby(a, len):
...     print i, list(k)
...
2 ['aa', 'ab']
3 ['abc', 'bcd']
5 ['abcde']
```

另一个例子

```
from itertools import *
from operator import itemgetter

d = dict(a=1, b=2, c=1, d=2, e=1, f=2, g=3)
# 前提是传入的di按照排序标准key是有序的
di = sorted(d.iteritems(), key=itemgetter(1))
for k, g in groupby(di, key=itemgetter(1)):
    print k, map(itemgetter(0), g)


1 ['a', 'c', 'e']
2 ['b', 'd', 'f']
3 ['g']
```

### itertools.ifilter(predicate, iterable)

返回的是迭代器。==类似于针对列表的内置函数 filter()== , 它==只包括当测试函数返回true时的项==. 它不同于 dropwhile()

使用

```
from itertools import *

def check_item(x):
    print 'Testing:', x
    return (x<1)

for i in ifilter(check_item, [ -1, 0, 1, 2, 3, 4, 1, -2 ]):
    print 'Yielding:', i

Testing: -1
Yielding: -1
Testing: 0
Yielding: 0
Testing: 1
Testing: 2
Testing: 3
Testing: 4
Testing: 1
Testing: -2
Yielding: -2
```

### itertools.ifilterfalse(predicate, iterable)

和ifilter(函数相反 ， 返回一个包含那些测试函数返回false的项的迭代器)

使用

```
from itertools import *

def check_item(x):
    print 'Testing:', x
    return (x<1)

for i in ifilterfalse(check_item, [ -1, 0, 1, 2, 3, 4, 1, -2 ]):
    print 'Yielding:', i

Testing: -1
Testing: 0
Testing: 1
Yielding: 1
Testing: 2
Yielding: 2
Testing: 3
Yielding: 3
Testing: 4
Yielding: 4
Testing: 1
Yielding: 1
Testing: -2
```

### itertools.islice(iterable, start, stop[, step])

返回的迭代器是返回了==输入迭代器根据索引来选取的项==

创建一个迭代器，==生成项的方式类似于切片返回值==： iterable[start : stop : step]。==与切片不同==，==负值==不会用于任何start，stop和step。

使用

```
from itertools import *

print 'Stop at 5:'
for i in islice(count(), 5):
    print i

print 'Start at 5, Stop at 10:'
for i in islice(count(), 5, 10):
    print i

print 'By tens to 100:'
for i in islice(count(), 0, 100, 10):
    print i

Stop at 5:
0
1
2
3
4
Start at 5, Stop at 10:
5
6
7
8
9
By tens to 100:
0
10
20
30
40
50
60
70
80
90
```

### itertools.imap(function, *iterables)

创建一个迭代器，==生成项function(i1, i2, …, iN)==，其中==i1，i2…iN分别来自迭代器iter1，iter2 … iterN==，==如果function为None，则返回(i1, i2, …, iN)形式的元组==，==只要提供的一个迭代器不再生成值，迭代就会停止==。

即：返回一个迭代器, 它是==调用了一个其值在输入迭代器上的函数==, 返回结果. 它类似于内置函数 map() , 只是前者在任意输入迭代器结束后就停止(而map函数是插入None值来补全所有的输入).

使用

```
from itertools import *

print 'Doubles:'
for i in imap(lambda x:2*x, xrange(5)):
    print i

print 'Multiples:'
for item in imap(lambda x,y:(x, y, x*y), xrange(5), xrange(5,10)):
    print '%d * %d = %d' % item

Doubles:
0
2
4
6
8
Multiples:
0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 8 = 24
4 * 9 = 36
```

### itertools.starmap(function, iterable)

创建一个迭代器，生成值func(*item),其中item来自iterable，只有当==iterable生成的项适用于这种调用函数的方式==时，此函数才有效。

注意：只可以有一个iterable

使用

```
from itertools import *

values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
for i in starmap(lambda x,y:(x, y, x*y), values):
    print '%d * %d = %d' % i

0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 8 = 24
4 * 9 = 36
```

### itertools.tee(iterable[, n=2])

==把一个迭代器分为n个迭代器（默认是两个）, 返回一个元组.==

为了克隆原始迭代器，生成的项会被缓存，并在所有新创建的迭代器中使用，一定要注意，==不要在调用tee()之后使用原始迭代器iterable==，否则==缓存机制==可能无法正确工作。

使用

```
from itertools import *

r = islice(count(), 5)
i1, i2 = tee(r)

for i in i1:
    print 'i1:', i
for i in i2:
    print 'i2:', i

i1: 0
i1: 1
i1: 2
i1: 3
i1: 4
i2: 0
i2: 1
i2: 2
i2: 3
i2: 4
```

### itertools.takewhile(predicate, iterable)

==和dropwhile相反==

创建一个迭代器，==生成iterable中predicate(item)为True的项==，==只要predicate计算为False，迭代就会立即停止。==

即：从序列的头开始, 直到执行函数func失败.

使用

```
from itertools import *

def should_take(x):
    print 'Testing:', x
    return (x<2)

for i in takewhile(should_take, [ -1, 0, 1, 2, 3, 4, 1, -2 ]):
    print 'Yielding:', i

Testing: -1
Yielding: -1
Testing: 0
Yielding: 0
Testing: 1
Yielding: 1
Testing: 2
```

### itertools.izip(*iterables)

返回一个==合并了多个迭代器或者可迭代对象==为一个==元组的迭代器.== 它类似于内置函数zip(), ==只是它返回的是一个迭代器而不是一个zip对象。==

创建一个迭代器，==生成元组(i1, i2, … iN)==，其中i1，i2 … iN 分别来自迭代器iter1，iter2 … iterN，==只要提供的某个迭代器不再生成值，迭代就会停止==，此函数生成的值与内置的zip()函数相同。

使用

```
from itertools import *

for i in izip([1, 2, 3], ['a', 'b', 'c']):
    print i
(1, 'a')
(2, 'b')
(3, 'c')
```

### itertools.izip_longest(*iterables[, fillvalue])

与izip()相同，但是迭代过程会==持续到所有输入迭代变量iter1,iter2等都耗尽为止==，==如果没有使用fillvalue关键字参数指定不同的值，则使用None来填充已经使用的迭代变量的值。==

## 第三部分

### itertools.product(*iterables[, repeat])

笛卡尔积

创建一个迭代器，生成表示item1，item2等中的项目的==笛卡尔积的元组==，repeat是一个关键字参数，==指定重复生成序列的次数==。

例子

```
import itertools
a = (1, 2, 3)
b = ('A', 'B', 'C')
c = itertools.product(a,b)
for elem in c:
    print elem

(1, 'A')
(1, 'B')
(1, 'C')
(2, 'A')
(2, 'B')
(2, 'C')
(3, 'A')
(3, 'B')
(3, 'C')
```

### itertools.permutations(iterable[, r])

创建一个迭代器，返回iterable中所有长度为r的项目序列，如果省略了r，那么==序列的长度与iterable中的项目数量相同==： 返回p中任意取r个元素做排列的元组的迭代器

### itertools.combinations(iterable, r)

创建一个迭代器，返回iterable中所有长度为r的子序列，返回的子序列中的项==按输入iterable中的顺序排序== ==(不带重复)==

### itertools.combinations_with_replacement(iterable, r)

创建一个迭代器，返回iterable中所有长度为r的子序列，返回的子序列中的项按输入iterable中的顺序排序 ==(带重复)==
