# k_clique_communities

- ```
k_clique_communities(G, k, cliques=None)
  ```

  | Parameters:  | G (NetworkX graph) <br />k ([int]) – Size of smallest clique<br />cliques (list or generator) – Precomputed cliques (use networkx.find_cliques(G)) |
  | :----------- | ------------------------------------------------------------ |
  | Return type: | Yields sets of nodes, one for each k-clique community.       |
  
  定义： 对于一个图G而言，如果其中有一个==完全子图==（任意两个节点之间均存在边），节点数是k，那么这个完全子图就可称为一个==k-clique==。进而，==如果两个k-clique之间存在k-1个共同的节点==，那么就称这==两个clique是“相邻”的==。彼此相邻的这样一串clique构成==最大集合==，就可以称为==一个社区（而且这样的社区是可以重叠的，即所谓的overlapping community，就是说有些节点可以同时属于多个社区），且社区是可以重叠的==；
  
  ![img](https://img-blog.csdn.net/20160507102746403?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center) -->  ![img](https://img-blog.csdn.net/20160507102814482?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)
  
  ![img](https://img-blog.csdn.net/20160507102834414?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)
  
  ```
  import networkx as nx
  import matplotlib.pyplot as plt
  G = nx.complete_graph(5) #返回具有N个节点的完整图，节点标签是0~n-1
  K5 = nx.convert_node_labels_to_integers(G,first_label=2)
  #G为复杂网络图，指定编号节点中的起始偏移量，新的整数标签编号为first_label，...，n-1 + first_label。
  G.add_edges_from(K5.edges())#对地图中添加边
  c = list(nx.k_clique_communities(G, 4))#查找具有社团结构的网络：地图，最小团块大小 ：完全连接K个节点的子图
  print(c)
  nx.draw(G)
  plt.show()
  ```
  
  