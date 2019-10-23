# node2vec

## node2vec.Node2Vec 总体流程：

![img](https://img-blog.csdnimg.cn/2019050520411066.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MTkyMzcz,size_16,color_FFFFFF,t_70)

## 作用

初始化 node2vec 对象，预先==计算 walk 概率并生成 walks==

## 函数原型和参数

node2vec.Node2Vec函数：

```
node2vec.Node2Vec(self, graph, dimensions=128, walk_length=80, num_walks=10, p=1, q=1, weight_key='weight', workers=1, sampling_strategy=None, quiet=False, temp_folder=None)
```

graph:  第1个位置的参数必须是 ==networkx 图==。节点名必须都是==整数或都是字符串==。在输出模型上，它们始终是==字符串==。
dimensions: 嵌入维度（默认值：128）
walk_length: 每个路径的节点数（默认值：80）
num_walks: 经过每个节点的次数（默认值：10）
p: 返回超参数（默认值：1）# p 和 q 是决定采用DFS或者BFS的关键参数
q: 输入输出参数（默认值：1）
weight_key: 在加权图上，这是 ==权重属性的关键字==（默认值：“weight”）。
workers: 并行执行的工作者数目（默认值：1）
sampling_strategy: 特定节点的采样策略, 支持设置节点特定的“q”、“p”、“num_walks”和“walk_length” 参数。请准确地使用这些关键字。如果未设置，将默认为对象初始化时传递的全局参数。
quiet: 控制==布尔值长度==。（默认值：false）
temp_folder: 指向==文件夹的字符串路径==，用于==保存图形的共享内存副本== - 在算法执行过程中处理过大而无法放入内存的图时提供。

Node2Vec.precompute_probabilities 函数：预先计算==每个节点的转换概率==。

Node2Vec.generate_walks 函数：==生成随机路径==，将用作 skip-gram 的输入。return：路径列表。每个路径都是一个节点列表。

Node2Vec.fit函数:  使用 gensim 的 word2vec ==创建嵌入对象==。(因为node2vec 是==基于 word2vec 的==)
   1. 参数 skip_gram_params: gensim.models.word2vec 的参数 - 不提供 “size”，它取自 node2vec 的 “dimensions” 参数

   2. skip_gram_params 的类型: dict 

   3. return: 一个 gensim word2vec 模型
