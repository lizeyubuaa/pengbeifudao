# DeepWalk、node2vec

## 图嵌入（Graph Embedding）

图嵌入，也叫==网络表示学习==，目的是为了学习到==网络节点或者边的低维稠密向量表示==，这样就能很方便地用于后续任务中。这里，我尽量避免加任何公式，用最浅显的语言解释图嵌入。图的最基本形式是邻接矩阵，比如下面左侧4个节点组成的图，经过编号后，我们可以获得右侧的邻接矩阵。

![img](https://pic3.zhimg.com/80/v2-b9ece8821b019b2bd5c87e445fa37b5a_hd.jpg)

问题就此展开。对于一个大一点的图（比如社交网络）可能有数以亿万计的节点，根本没法读入内存，在写算法题的时候N*N大小的二维数组当`N=10000`时，就会超内存。而社交网络动辄亿万，这谁顶得住啊...

对于维度较大的矩阵，数学上有着各种优美的==矩阵分解算法==。以==非负矩阵分解为例(NMF)==，给定矩阵 ![[公式]](https://www.zhihu.com/equation?tex=A_%7Bm%5Ctimes+m%7D) ，存在矩阵 ![[公式]](https://www.zhihu.com/equation?tex=B_%7Bm%5Ctimes+k%7D) 和 ![[公式]](https://www.zhihu.com/equation?tex=C_%7Bk%5Ctimes+m%7D) 满足 ![[公式]](https://www.zhihu.com/equation?tex=A%3DBC) . 我们可以粗略地认为，通过矩阵分解，我们将获得每个节点的==两种长度为k的向量表示，即矩阵B的第i行，矩阵c的第i列。==突然有种==word2vec==的既视感... 这种方法虽然不错，但是==矩阵维度过大的问题还是没解决==，对算法的推广也产生了限制。

## 2. DeepWalk

时间到了2014年，那是word2vec问世的第二年，Bryan Perozzi创造性地提出了==DeepWalk==，将词嵌入的方法引入图嵌入，将图嵌入引入了一个新的时代。DeepWalk提出了“随机游走”的思想，这个思想有点类似搜索算法中的DFS，从某一点出发，以深搜的方式获得一个节点序列。==这个序列即可以用来描述节点==。我们还是用图说话，这次来个稍微大一点的图。

![img](https://pic2.zhimg.com/80/v2-d27527d94ff1cbd4207db67bc6f85f91_hd.jpg)以节点1为开始节点，长度为4的随机游走示例

依照图中的连边关系，从节点1开始，可能依次经过节点2,6,1,3。==每个节点每次游走的概率为节点的出度分之一==，以节点1为例，将以等概率游走至节点2、3、4、6节点。这个过程非常容易理解，但是为什么游走出来的节点序列就可以描述一个节点，我这里给出一种==直观的解释是==：在有限步数的游走下，从1个节点出发，能到达的节点是所有节点的一个子集；==每个节点随机游走产生的子集是不同的，这些不同的子集就可以用于描述不同节点==。

DeepWalk论文代码里给出了一个参数 ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha) 可用于==实现带概率返回原点的游走策略==。即在游走长度未到达预定长度 ![[公式]](https://www.zhihu.com/equation?tex=L) 的情况下（假设游走了 ![[公式]](https://www.zhihu.com/equation?tex=k) 步， ![[公式]](https://www.zhihu.com/equation?tex=0+%5Cleq+k+%5Cleq+L) 表示可发生在游走的==任何时刻==），第 ![[公式]](https://www.zhihu.com/equation?tex=k%2B1) 步将有一定的概率 ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha) 返回原点。这样一来==有助于获得更多较短的序列==，如下图，红色连接线表示在该步的游走返回了原点。

![img](https://pic1.zhimg.com/80/v2-4d4fccfdcf437303f78bb966664aafb8_hd.jpg)多条带概率返回原点的游走序列

目前为止获得了节点序列，要==如何使用==是个问题，也是DeepWalk的创新之处。作者提出了==节点共现频率和词汇共现频率相似的统计结果==，并认为这种结果表明：**游走的序列可以类比语料库中的句子，序列中的节点可以类比句子中的单词，词汇的共现情况，类似于随机游走序列中节点的共现情况。**这个统计结果可能只是作者拍脑袋想出来的，但是确实work。

![img](https://pic1.zhimg.com/80/v2-9cf9787542f25792e2d83e7b8835addc_hd.jpg)节点共现和词汇共现同时满足==幂率==

通过**节点->单词、节点序列->句子**这个转化，就可以将图上的Embedding问题转化为==一系列节点在游走序列中共现==的问题，此时直接用gensim里的Word2Vec包就可以完成训练，得到的训练结果是**==id --> [0.2234 ... 0.4562]==** 是每个节点id及其对应的向量表示。这个过程非常之简单，唯一和Word Embedding不同的地方在于需要==构建游走序列==，而且随机游走的实现并不复杂，我们可以这样写：

```python3
node_adj_list = {} # 节点连边关系
nodes = []      # 所有节点
walk_sequences = []
# 对网络中每一个节点
for node in node_pairs:
    # 产生num_walks个游走
    for i in num_walks:
        walk_sequence = []
        # 每次游走walk_length步
        for j in walk_length:
            # random pick a selected_node in node_adj_list[node]
            walk_sequence.append(selected_node)
        walk_sequences.append(walk_sequence)
# 最终需要的是walk_sequences
# 可以将walk_sequences扔进word2vec训练
```

没错，nothing special直接上字典就好了，然后可以调用gensim的Word2Vec包，使用Skip-Gram训练得到结果。将游走的结果写入文件，可以像使用一个“语料”一样改变参数多次运行Word2vec从而==验证超参数对实验结果的影响==。

## node2vec

DeepWalk可以说给大家带来了全新的思路，其意义远不止实验结果那么简单。理论上，对于==任何图数据，或者是由关系型数据抽象出来的图数据，都可以利用DeepWalk得到Embedding==，而且算法简单，易于扩展到大规模数据上；更为重要的，这启发了后续的研究者进行了更加深入的研究。

node2vec的作者针对==DeepWalk不能用到带权图==上的问题，提出了==概率游走==的策略，并使用==AliasSampling进行采样==。

下面来说一下node2vec的不同之处，在一个图中，假设上一步走到的节点是 ![[公式]](https://www.zhihu.com/equation?tex=t) ，当前处于节点 ![[公式]](https://www.zhihu.com/equation?tex=v) ，则下一步游走的概率为 ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha) 满足：

![[公式]](https://www.zhihu.com/equation?tex=%5Calpha+%3D+%5Cleft%5C%7B%5Cbegin%7Bmatrix%7D+%5Cfrac%7B1%7D%7Bp%7D+%26+d%3D0+%5C%5C++1+%26+d%3D1+%5C%5C++%5Cfrac%7B1%7D%7Bq%7D+%26+d%3D2++%5Cend%7Bmatrix%7D%5Cright.+++%5C%5C)

结合下图，可以这么理解， ![[公式]](https://www.zhihu.com/equation?tex=d) 表示节点 ![[公式]](https://www.zhihu.com/equation?tex=x) 与节点 ![[公式]](https://www.zhihu.com/equation?tex=t) 的距离。d=0表示上一步走过的节点 ![[公式]](https://www.zhihu.com/equation?tex=t) ，d=1表示与节点 ![[公式]](https://www.zhihu.com/equation?tex=t) 和 ![[公式]](https://www.zhihu.com/equation?tex=v) 距离相同的节点（距离均为1），其他情况下为d=2.

![img](https://pic1.zhimg.com/80/v2-187ca11312745470ae7a3c0f692a6858_hd.jpg)node2vec算法概率游走策略

上述算法要求具备“上一步节点t”，那对于==第一步游走要怎么做呢？==node2vec论文算法中对第一步的游走采取了与DeepWalk相同的游走方式（==不包含超参数p和q==），直接按照边的权重进行概率游走。完成节点的游走之后，就可以将获得的节点序列扔进Word2Vec训练并得到节点向量了。

这种方法咋一听也有点拍脑袋的成分在里面，不过效果确实好，在我复现的一些embedding算法中，通过调节参数p和q，node2vec几乎都优于DeepWalk. 究其原因，是因为node2vec这种游走策略，==使用p和q控制了游走的宽度优先和深度优先==，例如 ![[公式]](https://www.zhihu.com/equation?tex=p%5Crightarrow+%5Cinfty) , ![[公式]](https://www.zhihu.com/equation?tex=q%3D1) 时候，将获得如下图左侧游走策略；当 ![[公式]](https://www.zhihu.com/equation?tex=p%5Crightarrow+%5Cinfty) 且 ![[公式]](https://www.zhihu.com/equation?tex=q+%5Crightarrow+%5Cinfty) 时将获得下图右侧游走策略：

![img](https://pic4.zhimg.com/80/v2-4c1ab7d0360457417b9d70063b605f5f_hd.jpg)不同大小的p和q产生游走策略的变化

从上图可以看出，p和q能够改变游走权重，从而调节游走策略偏向DFS或者BFS策略，更加充分地挖掘出节点在网络中的特征。

## metapath2vec

DeepWalk和node2vec虽然强大，但是仅适用于==同质网络==。所谓“同质”的意思就是，网络中所有节点的类型只有1种，比如用户关注关系网络、论文引用网络。这些==网络中只包含一种类型的节点，所传递的信息有限==。但是现实生活中存在众多异质网络，其包含多种类型的节点，比如==学术网络==，给出一个形式化的例子图如下：

![img](https://pic3.zhimg.com/80/v2-21ee7517471be8d9bd03d570fc62a29a_hd.jpg)学术网络的简单示例

异质网络比同质网络包含了更多的语义信息，如果仅仅使用DeepWalk和node2vec这类方法，只能将不同的节点进行不同编号，并进行随机游走。但是这种方式忽略了节点的类型信息，而将作者、论文、会议都视作同一类型的节点，丢失了大量语义信息。针对这个问题，metapath2vec的作者提出了==基于元路径的游走策略==，如下图。所谓**元路径**可以理解为==预定义的节点类型序列==，比如**APV**表示【作者（Author）-论文（Paper）-期刊（Venue）】，通过元路径的定义可以在异质网络中获得一系列的节点序列，比如APA在图中就可以获得( ![[公式]](https://www.zhihu.com/equation?tex=a_1+p_1+a_2) ， ![[公式]](https://www.zhihu.com/equation?tex=a_2+p_2+a_3) , ![[公式]](https://www.zhihu.com/equation?tex=a_2+p_2+a_4) 等节点序列)。

![img](https://pic4.zhimg.com/80/v2-18d7b80e6a1b1b0fcfdf7c8bb8f80b8b_hd.jpg)基于元路径的游走策略

通过设计==首尾类型相同的元路径==，我们可以不断地重复基于相同元路径的游走（例如基于元路径APA可以在图中获得节点序列 ![[公式]](https://www.zhihu.com/equation?tex=a_1+p_1+a_2+p_2+a_3+p_2+a_4+p_3+a_5) ）。可以看到此时可以获得基于元路径的游走序列。这样我们可以将获取到的这种序列使用Skip-Gram训练，从而获得节点的向量表示。

值得一提的是论文作者在文章中提到了==负采样的时候==考虑节点类型，即在训练Negative Sampling的时候对于节点的采样不再随机（比如对于节点对 ![[公式]](https://www.zhihu.com/equation?tex=a_1+a_3) ，我们要针对节点 ![[公式]](https://www.zhihu.com/equation?tex=a_3) 进行负采样。该方法要求只能采样同样类型节点，即此时只能采样作者节点，而不能采样论文、期刊节点）。**但是在论文复现的实际效果中，该方法的提升着实有限**。

异质网络不仅限于学术网络，==很多关系型数据都可以被扩展为异质网络==。比如下图，表示用户观看电影的异质网络。用户观看多个电影，然后电影的导演分别是不同的人，所以在图中存在元路径UMD，UMU，DMD等等，故可以对该网络进行Embedding。其他形式的异质网络还有很多，可以自行从关系型数据中挖掘。

![img](https://pic1.zhimg.com/80/v2-29a3219efcb523f1d7a8afdb362bc9e4_hd.jpg)用户观影的异质网络

## EGES

这篇文章（Billion-scale Commodity Embedding for E-commerce Recommendation in Alibaba）出自==阿里巴巴淘宝团队==，不得不说大厂的算法论文工程性上更加完善，不仅给出了算法，更给出了线上 ==A/B Test==，以及应用在推荐系统的==离线、在线功能部署图==。

这篇文章对我最大的启发是图的构造方式。对于淘宝的线上商品，怎么构建出商品之间的连边呢？我们可以使用==用户的点击行为作为关系构建==，该构建基于一个假设：==**用户在一段时间内浏览的商品存在相似性**==。例如用户连续看了DAB三种商品，则根据该假设认为，可以构建 ![[公式]](https://www.zhihu.com/equation?tex=D%5Crightarrow+A+%5Crightarrow+B) 这样的关系。但是当浏览的商品超过了一定时间，比如用户在早上浏览了BE，在晚上浏览了商品DEF，则商品E和商品D之间不能构造连边，因为它们之间相隔的时间太远。

![img](https://pic3.zhimg.com/80/v2-1034208a2df4c3b30542d54f68333706_hd.jpg)根据用户点击行为构建商品关联图

根据上述假设，可以从海量商品浏览记录中，挖掘出隐式连边关系。构建出商品之间的关联图之后，就可以使用DeepWalk算法获得一系列游走序列，并使用Skip-Gram训练从而获得商品的向量表示。

这个方法能够work的原因是该假设是一个用户浏览商品时广泛存在的行为习惯，其实可迁移性有待进一步考量（毕竟假设是否符合数据需要实验来验证的）。不过这确实给我们提供了一种非常好的，基于用户行为构建商品关联关系的方法。该论文中还提出了商品属性的Embedding，有兴趣的可以去看一下原文。

## DeepWalk算法

  DeepWalk算法是类比word2vec算法实现的，用到了其中的==Skip-Gram算法==（word2vec主要==有Skip-Gram和CBOW两种模型==，从直观上理解，Skip-Gram是==给定input word来预测上下文==。而CBOW是==给定上下文来预测input word==）。
  word2vec算法是实现单词的向量表示的算法，Skip-Gram算法的思想是建立一个神经网络，神经网络的训练集是由单词组成的句子。神经网络的输入是单词，输出是==各个单词出现在输入单词的上下文中的概率==。通过对训练集对神经网络进行训练，==得到神经网络中的一些参数==，根据参数可以得到输入的单词的向量表示。
  想要类比word2vec实现node的向量表示，必须要找到==在网络中，单词是什么，句子是什么==。DeepWalk中提出，==将node作为单词；通过随机游走，得到node的序列，将这个序列作为句子。这样就可以使用Skip-Gram算法==。
  为了提高Skip-Gram的训练过程的效率，DeepWalk采用==分层softmax==的方法来训练，即将node分配到二叉树的叶节点上。同时在==构造二叉树时，使用霍夫曼编码==，将使用频率高的节点放到较短的分支上。这样算法复杂度就从O(|V|)降到了O(log|V|)。

## node2vec算法

  node2vec算法与DeepWalk相同，也是类比word2vec模型实现的，用到了模型中的Skip-Gram算法，只是==在随机游走的算法与DeepWalk不同==。
  在随机游走的算法上，DeepWalk是完全随机的，而node2vec算法给出了一个公式，公式中主要起作用的是==p和q两个参数==。其中，==p是控制访问走过的node，即往回走；q是控制访问还没有走过的node，即向外走==。

## 5个算法的比较

  word2vec是Word Embedding的算法，其他四个算法都是==Node Embedding==，考虑其他4个算法。
  Node Embedding的目标是，==将node表示成向量，同时能够保存原网络的结构==，Laplacian Eigenmap、LINE、DeepWalk、node2vec算法的目的也都是如此。但是虽然四个算法都将node表示成了向量，但是四个算法对于==如何保证最大程度的保存原网络的结构的定义不同，即目标函数的定义不同==，我觉得这也是四个算法的本质不同。
  Laplacian Eigenmap用两个node之间边的权值表示原网络中的两个node的相似度，用向量表示的两个node之间距离表示向量空间中两个node的相似度，为了保存原网络的结构信息，node之间的相似关系应该保持一致，由此定义了目标函数。
  LINE中分别给出了网络中和向量表示中，两个node之间的一阶相似度和二阶相似度，共四个公式的定义。然后==综合一阶相似度保持一致和二阶相似度==保持一致，定义了目标函数。
  DeepWalk和node2vec算法是先在网络中随机游走，得到node的序列。==两个node同时出现在一个序列中的频率越高，两个node的相似度越高。==然后构建一个神经网络，神经网络的输入是node，输出是其他node与输入的node同时出现的概率。同时出现的概率越高，两个node的相似度越高。为了保持相似度一致，得到目标函数。
  从目标函数的定义上来看，Laplacian Eigenmap的定义最简单，但是表示网络结构的能力比较差。LINE为了更好的保存网络的结构信息，提出了一阶相似度和二阶相似度的概念，并在目标函数中结合了两者。DeepWalk是提出了一个新的思路，但是对于原网络中node的相似度的定义不能很好的反映网络的结构，node2vec则着重解决了这一问题。
  除了上面提到的区别外，几个算法肯定还有一些细节上的区别，需要仔细了解算法的实现；此外，几个算法应该有不同的针对性，有各自擅长解决的问题，这一点不同将在了解完算法的背景后再作分析。