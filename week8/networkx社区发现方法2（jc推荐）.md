# networkx社区发现

```
import community
import matplotlib.pyplot as plt
import networkx as nx

# 生成了一个随机网络
G = nx.erdos_renyi_graph(30, 0.05)

# 返回一个字典，值是某一个点所属的社区。自动确定合适的社区数。
partition = community.best_partition(G)

# drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()):
    count = count + 1.
    # 确定某一个区域的节点
    list_nodes = [nodes for nodes in partition.keys()
                  if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
                           node_color=str(count / size))

nx.draw_networkx_edges(G, pos, alpha=0.5, label=True)
plt.show()

```