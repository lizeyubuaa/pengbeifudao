# Python NetworkX/Community包进行网络划分和可视化

## networkx 提供画图的函数有：

draw（G，[pos,ax,hold]）
draw_networkx(G，[pos,with_labels])
draw_networkx_nodes(G,pos,[nodelist]) 绘制网络G的节点图
draw_networkx_edges(G,pos[edgelist]) 绘制网络G的边图
draw_networkx_edge_labels(G, pos[, …]) 绘制网络G的边图，边有label
—有layout 布局画图函数的分界线—
draw_circular(G, \*\*kwargs) Draw the graph G with a circular layout.
draw_random(G, \*\*kwargs) Draw the graph G with a random layout.
draw_spectral(G, \*\*kwargs) Draw the graph G with a spectral layout.
draw_spring(G, \*\*kwargs) Draw the graph G with a spring layout.
draw_shell(G, \*\*kwargs) Draw networkx graph with shell layout.
draw_graphviz(G[, prog]) Draw networkx graph with graphviz layout.

## networkx 画图参数：

- node_size: 指定节点的尺寸大小(默认是300，单位未知，就是上图中那么大的点)
- node_color: 指定节点的颜色 (默认是红色，可以用字符串简单标识颜色，例如’r’为红色，’b’为绿色等，具体可查看手册)，用==“数据字典”赋值==的时候必须对字典取值（.values()）后再赋值
- node_shape: 节点的形状（默认是圆形，用字符串’o’标识，具体可查看手册）
- alpha: 透明度 (默认是1.0，不透明，0为完全透明)
- width: 边的宽度 (默认为1.0)
- edge_color: 边的颜色(默认为黑色)
- style: 边的样式(默认为实现，可选： solid|dashed|dotted,dashdot)
- with_labels: 节点是否带标签（默认为True）
- font_size: 节点标签字体大小 (默认为12)
- font_color: 节点标签字体颜色（默认为黑色）
e.g. nx.draw(G,node_size = 30, with_label = False)
绘制节点的尺寸为30，不带标签的网络图。

## 布局指定节点排列形式

pos = nx.spring_layout
建立布局，对图进行布局美化，networkx 提供的布局方式有：

- circular_layout：节点在一个==圆环上==均匀分布
- random_layout：节点==随机分布==
- shell_layout：节点在同心圆上分布
- spring_layout： 用Fruchterman-Reingold算法排列节点（这个算法我不了解，样子类似多中心放射状）
- spectral_layout：根据图的拉普拉斯特征向量排列布局也可==用pos参数指定==，例如，nx.draw(G, pos = spring_layout(G)) 这样指定了networkx上以中心放射状分布.

## DEMO

```
values = [part.get(node) for node in Graph.nodes()]
nx.draw_spring(Graph, cmap=plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
plt.show()
```

## **加入权重**的图

```python3
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

G.add_edge('a', 'b', weight=0.6)
G.add_edge('a', 'c', weight=0.2)
G.add_edge('c', 'd', weight=0.1)
G.add_edge('c', 'e', weight=0.7)
G.add_edge('c', 'f', weight=0.9)
G.add_edge('a', 'd', weight=0.3)

elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

pos = nx.spring_layout(G)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge,
                       width=6)
nx.draw_networkx_edges(G, pos, edgelist=esmall,
                       width=6, alpha=0.5, edge_color='b', style='dashed')

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

plt.axis('off')
plt.show()
```



![img](https://pic2.zhimg.com/80/v2-555987df498a485cc45ef8fd522b7161_hd.jpg)