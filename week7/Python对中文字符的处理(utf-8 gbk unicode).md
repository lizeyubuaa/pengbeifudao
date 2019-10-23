# Python对中文字符的处理(utf-8/ gbk/ unicode)

文件第一行永远默认

```python
# coding: utf-8
```

# 1.什么是utf-8/ gbk/ unicode编码

utf-8是Unix下的一种通用编码，可以对汉字编码，应该是Unix环境下能打开看到汉字的唯一编码

gbk是win环境下的一种汉字编码，其中GB2312编码也算是gbk编码，这种编码在Unix环境中打开是乱码，大概是这个样子：

![img](https://img-blog.csdn.net/20160629143249437?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

可以看到，英文正常显示，但是汉字呢就gg了，一般看到这种跟个蛋一样的字符就是gbk汉字（只在mac中试过，别的Unix不知道是不是个蛋）

unicode是一种==二进制编码==，所有的utf-8和gbk编码都得==通过unicode编码进行转译==，说的直白一点，utf-8和gbk编码之间不能之间转换，要在unicode之间过个场才能转换。下面我图解一下，方便理解：

![img](https://img-blog.csdn.net/20160629143925554?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)



# 2.如何查看文档、字符串编码格式

不废话，下面几行代码搞定：

```python
# coding:utf-8 
import chardet
s = '哈哈哈我就是一段测试的汉字呀'
print chardet.detect(s)
```


输出：{'confidence': 0.99, 'encoding': 'utf-8'}

# 3.各种编码之间如何转换

python中有两个很好用的函数 decode() 和 encode()

decode(‘utf-8’) 是从utf-8编码==转换成unicode编码==，当然括号里也可以写'gbk'

encode('gbk') 是将unicode编码==编译成gbk编码==，当然括号里也可以写'utf-8'

假如我知道一串编码是用utf-8编写的，怎么转成gbk呢

```python
s.decode('utf-8').encode('gbk')
```

像上面这样就可以了

图解一下:

![img](https://img-blog.csdn.net/20160629145559498?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

# 4.python str与bytes之间的转换



```python
# bytes object  
b = b"example"   
# str object  
s = "example"  
# str to bytes  
bytes(s, encoding = "utf8")   
# bytes to str  
str(b, encoding = "utf-8")   
# an alternative method  
# str to bytes  
str.encode(s)   
# bytes to str  
bytes.decode(b)
```