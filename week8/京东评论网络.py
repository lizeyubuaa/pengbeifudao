import copy
import csv
import pickle
import random
import warnings
from collections import defaultdict

import jieba
import matplotlib.pyplot as plt
import networkx as nx
from node2vec import Node2Vec

plt.rcParams['font.sans-serif'] = ['SimHei']
warnings.filterwarnings("ignore", category=UserWarning)


class WordNetwork(nx.Graph):
    # 记录绘图的个数，防止图的重叠
    counter = 0

    def __init__(self, review_corpus, w, t, K, n, flag):
        """
        :param review_corpus: 语料(list)
        :param w: 滑动窗口大小
        :param t: 共现次数的阈值
        :param K: community中的元素个数
        :param n: 排名前n
        :param flag: 标识是积极网络还是消极网络,0-neg,1-pos
        """
        super().__init__()
        self.corpus = review_corpus
        self.w = w
        self.t = t
        self.K = K
        self.n = n
        self.edges_weight = defaultdict(list)
        self.flag = flag

    # 将新找到的邻接关系加入到edges_weight
    def update_edges_weight(self, word, connected_words):
        # connected_weight是connected_word到word的距离
        for connected_weight, connected_word in enumerate(connected_words):
            self.edges_weight[(word, connected_word)].append(connected_weight + 1)

    # 遍历每条评论，找到每一个词的邻接词(列表)
    def research_connections(self):
        for review in self.corpus:
            for word_index, word in enumerate(review):
                connected_words = review[word_index + 1:word_index + self.w + 1]
                self.update_edges_weight(word, connected_words)

    def generate_network(self):
        """
        绘制语义网络图
        """
        self.research_connections()
        # 滤去共现次数小于t的两个词(认为语义相关性不显著)
        edges = [tuple([edge[0], edge[1], {'weight': len(distance) / sum(distance), 'count': len(distance)}]) for
                 edge, distance in
                 self.edges_weight.items() if len(distance) > self.t]
        # 在网络中添加边
        self.add_edges_from(edges)
        # 序列化边的数据
        with open(file="edges{}.csv".format(self.flag), mode="w", newline='') as cf:
            writer = csv.writer(cf)
            writer.writerow(["Source", "Target", "Id", "Weight"])
            for Id, edge in enumerate(edges):
                writer.writerow([edge[0], edge[1], Id, edge[2]['weight']])
        plt.figure(WordNetwork.counter)
        WordNetwork.counter += 1
        nx.draw(self, pos=nx.random_layout(self), with_labels=True, font_weight='bold', node_size=20, font_size=3)
        plt.savefig("network{}".format(self.flag), dpi=500)

    def node_attribute(self):
        """
        :return: word的结构属性字典(degree, page_rank, hits)
        """
        node_attribute = defaultdict(dict)
        degree = dict(self.degree)
        page_rank = nx.pagerank(self)
        hubs, authorities = nx.hits(self, max_iter=500)
        for node in self.nodes:
            node_attribute[node] = {'degree': degree[node], 'page_rank': page_rank[node], 'hubs': hubs[node],
                                    'authorities': authorities[node]}
        with open(file="nodes{}.csv".format(self.flag), mode="w", newline='') as cf:
            writer = csv.writer(cf)
            writer.writerow(["Id", "Label"])
            for node in self.nodes:
                writer.writerow([node, node])
        return node_attribute

    # 社团发现
    def community_topic(self):
        other = copy.deepcopy(self)
        c = list(nx.algorithms.community.k_clique_communities(other, other.K))
        write_2_txt("community_nodes.txt", c)
        community_nodes = [node for community in c for node in community]
        community_edges = [edge for edge in other.edges for node in community_nodes if node in edge]
        community_nodes = [node for edge in community_edges for node in edge]
        # 设置默认"node_color"属性为蓝色
        for word in other.nodes:
            other._node[word].update({'node_color': '#1f78b4'})
        # 给属于同一个community的节点相同的颜色
        for community in c:
            color = other.random_color()
            for word in community:
                other._node[word].update({'node_color': color})
        # 写入文件，用gephi可视化
        with open(file="community_nodes{}.csv".format(self.flag), mode="w", newline='') as cf:
            writer = csv.writer(cf)
            writer.writerow(["Id", "Label", "color"])
            for node in other.nodes:
                writer.writerow([node, node, other._node[node]['node_color']])
        other.remove_nodes_from(other.nodes - set(community_nodes))
        node_color = [node_dict['node_color'] for node_dict in dict(other.nodes.data()).values()]
        plt.figure(WordNetwork.counter)
        WordNetwork.counter += 1
        nx.draw_networkx(other, with_labels=True, pos=nx.random_layout(other), node_size=20, font_size=3,
                         node_color=node_color)
        plt.savefig("community{}".format(other.flag), dpi=1000, figsize=(800, 600))

    # 生成随机颜色
    def random_color(self):
        color_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += color_arr[random.randint(0, 14)]
        return "#" + color

    # 查找top_n词
    def find_top_n_words(self, words_rank):
        words_rank = sorted(words_rank.items(), key=lambda x: x[1])
        top_n_words = [tup[0] for tup in words_rank[0:self.n]]
        write_2_txt("sharing_words{}.txt".format(self.flag), top_n_words)

        return top_n_words

    # 生成top_n网络或者共有词网络
    def part_word_network(self, word_list, word_type):
        part_word_network_edges = [edge for word in word_list for edge in self.edges if word in edge]
        part_word_network_nodes = [word for edge in part_word_network_edges for word in edge]
        other = copy.deepcopy(self)
        all_nodes = copy.deepcopy(other.nodes)
        # 去除多余的节点，调节节点颜色
        for word in all_nodes:
            if word in word_list:
                other._node[word].update({'node_color': 'r'})
            elif word in part_word_network_nodes:
                other._node[word].update({'node_color': 'b'})
            else:
                other.remove_node(word)
        # 给选定词设置单独属性
        node_color = [node_dict['node_color'] for node_dict in dict(other.nodes.data()).values()]
        plt.figure(WordNetwork.counter)
        WordNetwork.counter += 1
        nx.draw_networkx(other, edgelist=part_word_network_edges,
                         node_color=node_color, pos=nx.random_layout(other),
                         with_labels=True, node_size=20, font_size=3)
        plt.savefig("{}_network{}".format(word_type, other.flag), dpi=1000, figsize=(800, 600))

    # 图嵌入
    def node2vec(self):
        node2vec = Node2Vec(self, dimensions=64, walk_length=30, num_walks=200)
        model = node2vec.fit(window=self.w, min_count=self.t)
        for word in self.nodes:
            self._node[word]['vector'] = model[word]
        model.save("node2vec")
        with open(file="node2vec{}.csv".format(self.flag), mode="w", newline='') as cf:
            writer = csv.writer(cf)
            writer.writerow(["node", "vector"])
            for node in self.nodes:
                writer.writerow([node, self._node[node]['vector']])


def review_im_word_cut(review_path, stop_words_path):
    """
    :param review_path: 评论语料路径
    :param stop_words_path: 停用词字典路径
    :return:review_word_list_pos, review_word_list_neg积极语料和消极语料
    """
    # 元素是一条评论(list)
    review_word_list = []
    # 1-positive,0-negative
    review_flag = []
    with open(file=stop_words_path, encoding='utf8', mode='r') as fp:
        stop_list = [word.rstrip('\n') for word in fp.readlines()]
    with open(file=review_path, encoding='utf-8', mode='r') as fp:
        for line in fp.readlines():
            line = line.rstrip('\n')
            line, flag = line[:-1].rstrip('\t'), int(line[-1])
            review_word_list.append([word for word in jieba.lcut(line) if word not in stop_list])
            review_flag.append(flag)
        # 将好评和差评分开
        review_and_flag = sorted(zip(review_word_list, review_flag), key=lambda tup: tup[1], reverse=True)
        review_word_list, _ = zip(*review_and_flag)
        index = review_flag.count(1)
        review_word_list_pos, review_word_list_neg = review_word_list[:index], review_word_list[index:]
    return review_word_list_pos, review_word_list_neg


def word_rank_single(attribute_dict, key):
    """
    :param key: 指定的排序关键字,"degree" or "page_rank" or "hubs" or "authorities"
    :param attribute_dict: 节点的结构属性字典
    :return: 节点的单指标排序
    """
    attribute_rank_dict = {}
    value_sorted = sorted(attribute_dict.items(), key=lambda x: x[1][key], reverse=True)
    for word_rank, word in enumerate(dict(value_sorted).keys()):
        attribute_rank_dict[word] = word_rank + 1
    return attribute_rank_dict


def word_rank_composite(attribute_dict):
    """
     :param attribute_dict: 节点的结构属性字典
    :return:节点的综合指标排序
    """
    dg, pg, hubs, au = word_rank_single(attribute_dict, "degree"), word_rank_single(attribute_dict,
                                                                                    "page_rank"), word_rank_single(
        attribute_dict, "hubs"), word_rank_single(attribute_dict, "authorities")
    composite_dict = {}
    for word in attribute_dict.keys():
        composite_dict[word] = dg[word] + pg[word] + hubs[word] + au[word]
    rank = sorted(composite_dict.items(), key=lambda x: x[1])
    write_2_txt("sharing_words_diff.txt", rank)
    return dict(rank)


# 查找共有词
def find_sharing_words(pos_words, neg_words):
    sharing_words = [word for word in pos_words if word in neg_words]
    write_2_txt("sharing_words.txt", sharing_words)
    return sharing_words


# 序列化
def write_2_txt(filename, file):
    with open(filename, mode='wb') as fp:
        # 传入0解决乱码问题
        pickle.dump(file, fp, 0)


def __main__():
    w = 8
    t = 100
    K = 5
    n = 30
    max_sharing_words = 20
    review_path = r'D:\李泽宇的DESKTOP\大三上\Python现代程序设计技术\作业\第六周资料\1分和5分评论文本.txt'
    stop_words_path = r'D:\李泽宇的DESKTOP\大三上\Python现代程序设计技术\作业\第二次资料\stopwords_list.txt'
    # 导入语料
    review_word_list_pos, review_word_list_neg = review_im_word_cut(review_path, stop_words_path)
    # 实例化网络
    pos_network, neg_network = WordNetwork(review_word_list_pos, w, t, K, n, 1), WordNetwork(review_word_list_neg, w, t,
                                                                                             K, n, 0)
    # 生成网络
    pos_network.generate_network(), neg_network.generate_network()
    # 计算节点的degree, page_rank, hits结构属性
    pos_attribute, neg_attribute = pos_network.node_attribute(), neg_network.node_attribute()
    # 节点排序
    pos_rank, neg_rank = word_rank_composite(pos_attribute), word_rank_composite(neg_attribute)
    # 发现共有词
    sharing_words = find_sharing_words(pos_network.nodes, neg_network.nodes)
    sharing_word_diff = {}
    for word in sharing_words:
        sharing_word_diff[word] = abs(pos_rank[word] - neg_rank[word])
    # 社区发现
    pos_network.community_topic(), neg_network.community_topic()
    pos_network.part_word_network(sharing_words[:max_sharing_words], "sharing"), neg_network.part_word_network(
        sharing_words[:max_sharing_words], "sharing")
    # 查找top_n词
    pos_top_n_words, neg_top_n_words = pos_network.find_top_n_words(pos_rank), neg_network.find_top_n_words(neg_rank)
    pos_network.part_word_network(pos_top_n_words, "top_n"), neg_network.part_word_network(neg_top_n_words, "top_n")
    pos_network.node2vec(), neg_network.node2vec()


if __name__ == "__main__":
    __main__()
