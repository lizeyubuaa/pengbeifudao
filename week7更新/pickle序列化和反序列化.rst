
序列化Python对象
==============================

问题
----------
你需要将一个Python对象序列化为一个字节流，以便将它==保存到一个文件、存储到数据库或者通过网络传输它==。

解决方案
----------

```
pickle.dump(obj, file, [,protocol])
```

注解：将对象obj保存到文件file中去。
protocol为序列化使用的协议版本，0：ASCII协议，所序列化的对象使用可打印的ASCII码表示；1：老式的二进制协议；2：2.3版本引入的新二进制协议，较以前的更高效。其中协议0和1兼容老版本的python。protocol默认值为3。
file：对象保存到的类文件对象。file==必须有write()接口==， file可以是一个以'w'方式打开的文件或者一个StringIO对象或者其他任何实现write()接口的对象。文件对象==需要是二进制模式打开的==。

```
pickle.load(file)
```

　　注解：从file中读取一个字符串，并将它重构为原来的python对象。
　　file:类文件对象，有==read()和readline()接口==。

举例：

    import pickle
    
    data = ... # Some Python object
    f = open('somefile', 'wb')
    pickle.dump(data, f)

为了将一个对象转储为==一个字符串==，可以使用 ``pickle.dumps()`` ：

    s = pickle.dumps(data)

为了从字节流中恢复一个对象，使用 ``pickle.load()`` 或 ``pickle.loads()`` 函数。比如：

    # Restore from a file
    f = open('somefile', 'rb')
    data = pickle.load(f)
    
    # Restore from a string
    data = pickle.loads(s)

讨论
----------
对于大多数应用程序来讲，``dump()`` 和 ``load()`` 函数的使用就是你有效使用 ``pickle`` 模块所需的全部了。它可适用于绝大部分Python数据类型和用户自定义类的对象实例。

``pickle`` 是一种Python==特有的自描述的==数据编码。通过自描述，被序列化后的数据==包含每个对象开始和结束以及它的类型信息==。因此，你无需担心对象记录的定义，它总是能工作。举个例子，如果要处理多个对象，你可以这样做：

    >>> import pickle
    >>> f = open('somedata', 'wb')
    >>> pickle.dump([1, 2, 3, 4], f)
    >>> pickle.dump('hello', f)
    >>> pickle.dump({'Apple', 'Pear', 'Banana'}, f)
    >>> f.close()
    >>> f = open('somedata', 'rb')
    >>> pickle.load(f)
    [1, 2, 3, 4]
    >>> pickle.load(f)
    'hello'
    >>> pickle.load(f)
    {'Apple', 'Pear', 'Banana'}
    >>>

你还能序列化函数，类，还有接口，但是结果数据仅仅将它们的==名称==编码成对应的代码对象。例如：

    >>> import math
    >>> import pickle.
    >>> pickle.dumps(math.cos)
    b'\x80\x03cmath\ncos\nq\x00.'
    >>>

当数据反序列化回来的时候，会先==假定所有的源数据时可用的==。模块、类和函数会自动按需导入进来。对于Python数据被不同机器上的解析器所共享的应用程序而言，数据的保存可能会有问题，因为所有的机器都必须访问同一个源代码。


