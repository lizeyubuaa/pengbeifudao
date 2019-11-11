# NetworkX教程

networkx是Python的一个包，用于构建和操作复杂的图结构，提供分析图的算法。图是由顶点、边和可选的属性构成的数据结构，顶点表示数据，边是由两个顶点唯一确定的，表示两个顶点之间的关系。顶点和边也可以拥有更多的属性，以存储更多的信息。

对于networkx创建的==无向图==，==允许一条边的两个顶点是相同的==，即允许出现==自循环==，但是==不允许两个顶点之间存在多条边，即出现平行边==。边和顶点都可以有自定义的属性，==属性称作边和顶点的数据==，每一个属性都是一个Key:Value对。

## ==创建图==

在创建图之前，需要导入networkx模块，通常设置别名为nx；如果创建的图中，顶点之间的边没有方向，那么该图称作无向图。在创建图时，可以通过help(g)来获得图的帮助文档。

```
import networkx as nx

g=nx.Graph()#创建空的无向图
g=nx.DiGraph()#创建空的有向图
```

## ==**图的顶点**==

图中的每一个顶点Node都有一个关键的ID属性，用于唯一标识一个节点，==ID属性可以整数或字符类型==；顶点除了ID属性之外，还可以自定义其他的属性。

**1，向图中增加顶点**

在向图中增加顶点时，可以一次增加一个顶点，也可以一次性增加多个顶点，顶点的ID属性是必需的。在添加顶点之后，可以通过g.nodes()函数获得图的所有顶点的视图，返回的实际上==NodeView==对象；如果为g.nodes(data=True)的data参数设置为true，那么返回的是==NodeDataView==对象，该对象不仅包含每个顶点的ID属性，还包括顶点的其他属性。

```
g.add_node(1)
g.add_nodes_from([2,3,4])
g.nodes()
#NodeView((1, 2,3,4))
```

在向图中添加顶点时，除ID属性之外，也可以向顶点中增加自定义的属性，例如，名称属性，权重属性：

```
>>> g.add_node(1,name='n1',weight=1)
>>> g.add_node(2,name='n2',weight=1.2)
```

**2，查看顶点的属性**

通过属性\_node获得图的所有顶点和属性的信息，_node属性返回的是一个字典结构，字典的Key属性是顶点的==ID属性==，Value属性是==顶点的其他属性构成的一个字典==。

```
>>> g._node
{1: {'name': 'n1', 'weight': 1}, 2: {'name': 'n2', 'weight': 1.2}, 3: {}, 4: {}}
>>>g.nodes(data=True)
```

可以通过顶点的ID属性来查看顶点的其他属性：

```
>>> g.node[1]
{'name': 'n1', 'weight': 1}
>>> g.node[1]['name']
'n1 new'
```

通过g.nodes()，按照特定的条件来查看顶点：

```
 >>> list(g.nodes(data=True))
 [(1, {'time': '5pm'}), (3, {'time': '2pm'})]
```

**3，删除顶点**

通过remove函数删除图的顶点，由于顶点的ID属性能够唯一标识一个顶点，==通常删除顶点都需要通过传递ID属性作为参数==。

```
g.remove_node(node_ID)
g.remove_nodes_from(nodes_list)
```

**4，更新顶点**

更新图的顶点，有两种方式，第一种方式使用字典结构的==_update函数==，第二种方式是==通过索引来设置新值==：

```
>>> g._node[1].update({'name':'n1 new'})
>>> g.node[1]['name']='n1 new'
{1: {'name': 'n1 new', 'weight': 1}, 2: {'name': 'n2', 'weight': 1.2}, 3: {}, 4: {}}
```

**5，删除顶点的属性**

使用del命令删除顶点的属性

```
del g.nodes[1]['room'] 
```

**6，检查是否存在顶点**

检查一个顶点是否存在于图中，可以使用 n in g方式来判断，也可以使用函数：

```
g.has_node(n)
```

## ==图的边==

图的边用于表示两个顶点之间的关系，因此，边是由两个顶点唯一确定的。为了表示复杂的关系，通常会为边增加一个权重weight属性；为了表示关系的类型，也会设置为边设置一个关系属性。

**1，向图中增加边**

边是由对应顶点的名称构成的，例如，顶点2和3之间有一条边，记作e=(2,3)，通过add_edge(node1,node2)向图中添加一条边，也可以通过add_edges_from(list)向图中添加多条边；在添加边时，==如果顶点不存在，那么networkx会自动把相应的顶点加入到图中==。

```
g.add_edge(2,3)
g.add_edges_from([(1,2),(1,3)])
g.edges()
#EdgeView([(1, 2), (1, 3), (2, 3)])
```

可以向边中增加属性，例如，权重，关系等：

```
g.add_edge(1, 2, weight=4.7, relationship='renew')
```

由于在图中，边的权重weight是非常有用和常用的属性，因此，networkx模块内置以一个函数，==专门用于在添加边时设置边的权重==，==该函数的参数是三元组==，前两个字段是顶点的ID属性，用于标识一个边，第三个字段是边的权重：

```
g.add_weighted_edges_from([(1,2,0.125),(1,3,0.75),(2,4,1.2),(3,4,0.375)])
```

在增加边时，也可以一次增加多条边，为不同的边设置不同的属性：

```
g.add_edges_from([(1,2,{'color':'blue'}), (2,3,{'weight':8})])
```

**2，查看边的属性**

查看边的属性，就是查看边的数据(data)，查看所有边及其属性：

```
>>> g.edges(data=True)
EdgeDataView([(1, 2, {}), (1, 3, {}), (2, 3, {})])
```

查看特定的边的信息有两种方式：

```
>>> g[1][2]
>>> g.get_edge_data(1,2)
{'weight': 0.125, 'relationship': 'renew', 'color': 'blue'}
```

**3，删除边**

边是两个顶点的ID属性构成的元组，通过 edge=(node1,node2) 来标识边，进而从图中找到边：

```
g.remove_edge(edge)
g.remove_edges_from(edges_list)
```

**4，更新边的属性**

通过边来更新边的属性，有==两种方式==，一种是使用update函数，一种是通过属性赋值来实现：

```
g[1][2]['weight'] = 4.7
g.edge[1][2]['weight'] = 4
g[1][2].update({"weight": 4.7})
g.edges[1, 2].update({"weight": 4.7})   
```

**5，删除边的属性**

通过 del命令来删除边的属性

```
del g[1][2]['name']
```

**6，检查边是否存在**

检查一条边是否存在于图中

```
g.has_edge(1,2)
```

## 图的属性

图的属性主要是指==相邻数据，节点和边==。

**1，adj**

adj返回的是一个==AdjacencyView视图==，该视图是顶点的==相邻的顶点和顶点的属性==，用于显示用于存储与顶点相邻的顶点的数据，这是一个==只读的字典结构==，==Key是顶点，Value是顶点的属性数据==。

```
>>> g.adj[1][2]
{'weight': 0.125, 'relationship': 'renew', 'color': 'blue'}
>>> g.adj[1]
AtlasView({2: {'weight': 0.125, 'relationship': 'renew', 'color': 'blue'}, 3: {'weight': 0.75}})
```

**2，edges**

图的边是由边的两个顶点唯一确定的，边还有一定的属性，因此，边是由两个顶点和边的属性构成的：

```
>>> g.edges
EdgeView([(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)])
>>> g.edges.data()
EdgeDataView([(1, 2, {'weight': 0.125, 'relationship': 'renew', 'color': 'blue'}), (1, 3, {'weight': 0.75}), (2, 3, {'weight': 8}), (2, 4, {'weight': 1.2}), (3, 4, {'weight': 0.375})])
```

EdgeView仅仅提供==边的信息==，可以通过属性g.edges或函数g.edges()来获得图的边视图。

EdgeDataView==提供图的边和边的属性==，可以通过EdgeView对象来调用data()函数获得。

**3，nodes**

图的顶点是顶点和顶点的属性构成的

```
>>> g.nodes
NodeView((1, 2, 3, 4))
>>> g.nodes.data()
NodeDataView({1: {'name': 'n1 new', 'weight': 1}, 2: {'name': 'n2', 'weight': 1.2}, 3: {}, 4: {}})
```

NodeView 提供==属性==，通过g.nodes或函数g.nodes()来获得。

NodeDataView提供==图的边和边的属性==，可以通过NodeView对象来调用data()函数获得。

**4，degree**

对于无向图，顶点的度是指跟顶点相连的边的数量；对于有向图，顶点的图分为入度和出度，朝向顶点的边称作入度；背向顶点的边称作出度。

==通过g.degree 或g.degree()能够获得DegreeView对象==

## 图的遍历

 图的遍历是指按照图中各顶点之间的边，从图中的任一顶点出发，对图中的所有顶点访问一次且只访问一次。图的遍历按照优先顺序的不同，通常分为==深度优先搜索（DFS）和广度优先搜索（BFS）两种方式==。

**1，查看顶点的相邻顶点**

查看顶点的相邻顶点，有多种方式，例如，以下代码都用于返回顶点1的相邻顶点，g[n]表示图g中，与顶点n相邻的所有顶点：

```
g[n]
g.adj[n]
g.neighbors(n)
```

其中，g.neighbors(n)是g.adj[n]的==迭代器版本==。

**2，查看图的相邻**

该函数返回顶点n和相邻的节点信息：

```
>>> for n, nbrs in g.adjacency():
...     print(n)
...     print(nbrs)
```

**3，图的遍历**

深度优先遍历的算法：

- 首先以一个未被访问过的顶点作为起始顶点，沿当前顶点的边走到未访问过的相邻顶点；
- 当当前顶点没有未访问过的相邻顶点时，则回到上一个顶点，继续试探别的相邻顶点，直到所有的顶点都被访问过。

深度优先遍历算法的思想是：从一个顶点出发，一条路走到底；如果此路走不通，就返回上一个顶点，继续走其他路。

广度优先遍历的算法：

- 从顶点v出发，依次访问v的各个未访问过的相邻顶点；
- 分别从这些相邻顶点出发依次访问它们的相邻顶点；

广度优先遍历算法的思想是：以v为起点，按照路径的长度，由近至远，依次访问和v有路径相通且路径长度为1,2...，n的顶点。

在进行图遍历时，需要访问顶点的相邻顶点，这需要用到adjacency()函数，例如，g是一个无向图，n是顶点，nbrs是顶点n的相邻顶点，是一个字典结构

```
for n,nbrs in g.adjacency():     
	print (n, nbrs)
    for nbr,attr in nbrs.items():
        # nbr表示跟n连接的顶点，attr表示这两个点连边的属性集合
        print(nbr,attr）
```

## 绘制Graph

使用networkx模块draw()函数构造graph，使用matplotlib把图显示出来：

```
nx.draw(g)

import matplotlib.pyplot as plt
plt.show()
```

修改顶点和边的颜色：

```
g = nx.cubical_graph()
nx.draw(g, pos=nx.spectral_layout(g), nodecolor='r', edge_color='b')
plt.show()
```

完整的示例如下面的代码所示：

```
from matplotlib import pyplot as plt
import networkx as nx
g=nx.Graph()
g.add_nodes_from([1,2,3])
g.add_edges_from([(1,2),(1,3)])
nx.draw_networkx(g)
plt.show()
```

## 计算每个顶点的PageRank值

每个顶点的PageRank（简称PR）值，是访问顶点的概率，可以通过networkx.pagerank()函数来计算，该函数根据==顶点的入边和边的权重==来计算顶点的PR值，也就是说，PR值跟顶点的入边有关，跟入边的weight（权重）属性有关：

```
pagerank(g, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='weight', dangling=None)
```

常用参数注释：

- g：==无向图会被转换为有向图，一条无向边转换为两条有向边==；
- alpha：==阻尼参数==，默认值是0.85，取值范围为 0 到 1, 代表从图中某一特定点==指向其他任意点==的概率；
- weight：==默认值是weight==，表示使用edge的weight属性作为权重，如果没有指定，那么把edge的权重设置为1；

**1，举个例子**

例如，创建一个有向图，由三个顶点（A、B和C），两条边（A指向B，A指向C），边的权重都是0.5

```
g=nx.DiGraph()
g.add_weighted_edges_from([('A','B',0.5),('A','C',0.5)])
print( nx.pagerank(g))
#{'A': 0.259740259292235, 'C': 0.3701298703538825, 'B': 0.3701298703538825}
```

修改边的权重，并查看顶点的PR值：

```
g['A']['C']['weight']=1
print( nx.pagerank(g))    
# {'A': 0.259740259292235, 'C': 0.40692640737443164, 'B': 0.3333333333333333}
```

**2，查看各个顶点的PR值**

根据图来创建PageRank，并查看各个顶点的PageRank值

```
pr=nx.pagerank(g)
#page_rank_value=pr[node]
for node, pageRankValue in pr.items():
    print("%s,%.4f" %(node,pageRankValue))
```

## hits

- `hits`(*G*, *max_iter=100*, *tol=1e-08*, *nstart=None*, *normalized=True*)

Return HITS hubs and authorities values for nodes.

Parameters:

**G** (*graph*) – A NetworkX graph

**max_iter** (*interger, optional*) – Maximum number of iterations in power method.

**tol** (*float, optional*) – Error tolerance used to check convergence in power method iteration.

**nstart** (*dictionary, optional*) – Starting value of each node for power method iteration.

**normalized** (*bool (default=True)*) – Normalize results by the sum of all of the values.

Returns:	
(hubs,authorities) – ==Two dictionaries keyed== by node containing the hub and authority values.

Return type:	
two-tuple of dictionaries

Examples

```
>>> G=nx.path_graph(4)
>>> h,a=nx.hits(G)
```