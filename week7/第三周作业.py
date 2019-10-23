# import packages
import os
import jieba
from collections import defaultdict
import re
# import folium
# from folium.plugins import HeatMap
import math


# import weibo text
def weibo_im(weibo_path):
    with open(weibo_path, encoding='utf-8', mode='r') as fp:
        documents = fp.readlines()
    return documents


# import emotion dictionary
def emo_dict_im(base_path):
    emotions_dict = defaultdict(list)
    for dictionary_path in os.listdir(base_path):
        path = os.path.join(base_path, dictionary_path)
        jieba.load_userdict(path)
        with open(path, encoding='utf-8', mode='r') as fp:
            emotion = dictionary_path.rstrip('.txt')
            for line in fp.readlines():
                line = line.rstrip('\n')
                emotions_dict[emotion].append(line)
            emotions_dict[emotion][0] = emotions_dict[emotion][0].lstrip('\ufeff')
    return emotions_dict


# import degree dictionary
def degree_dict_im(degree_dict_path):
    degree_dict = {}
    with open(degree_dict_path, encoding='utf-8', mode='r') as fp:
        for line in fp.readlines():
            line = line.rstrip('\n')
            degree_word, weight = line.split(' ')
            degree_dict[degree_word] = eval(weight)

    return degree_dict


# import privative dictionary
def privative_dict_im(privative_dict_path):
    privative_dict = []
    with open(privative_dict_path, encoding='utf-8', mode='r') as fp:
        for line in fp.readlines():
            privative_dict.append(line.rstrip('\n'))

    return privative_dict


# unzip document
def unzip_docs(documents):
    weibo, longitude, latitude, time = zip(*[(document.split('\t')) for document in documents])
    longitude = [eval(ele) for ele in longitude]
    latitude = [eval(ele) for ele in latitude]
    location = list(zip(latitude, longitude))

    return weibo, longitude, latitude, time, location


# text preprocess
def text_preprocess(weibo):
    # remove website
    weibo = [re.sub(r'http.*', '', document) for document in weibo]
    # remove @
    weibo = [re.sub(r'@[\u4e00-\u9fa5a-zA-Z0-9_-]{2,30}', '', document) for document in weibo]
    # remove #---#
    weibo = [re.sub(r'#([^#]{1,40})#', '', document) for document in weibo]
    # output
    with open('weibo_processed.txt', encoding='utf-8', mode='w') as fp:
        for line in weibo:
            fp.write(line)
            fp.write('\n')

    return weibo


def jieba_cut(weibo):
    # jieba word cut
    weibo_cut = [jieba.lcut(document) for document in weibo]
    with open('weibo_cut.txt', encoding='utf-8', mode='w') as fp:
        for line in weibo_cut:
            fp.write(''.join(line))
            fp.write('\n')

    return weibo_cut


# word emotion classify
def word_emo_classify(word, emotions_dict):
    for emotion in emotions_dict.keys():
        if word in emotions_dict[emotion]:
            return emotion
    else:
        return 'unsure'


# degree word detect
def degree_word_detect(word, document, degree_dict):
    index = document.index(word)
    for word in document[index - 2: index]:
        if word in degree_dict.keys():
            return degree_dict[word]
    else:
        return 1


# privative word detect
def privative_word_detect(word, document, privative_dict):
    index = document.index(word)
    for word in document[index - 2: index]:
        if word in privative_dict:
            return True
    else:
        return False


# weibo emotion score
def weibo_emo_score(weibo_cut, emotions_dict, degree_dict, privative_dict):
    emotion_score = dict(sad=-4, scared=-3, angry=-2, disgusted=-1, unsure=0, happy=4)
    weibo_score = []
    for document in weibo_cut:
        document_score = 0
        for word in document:
            emotion = word_emo_classify(word, emotions_dict)
            word_score = emotion_score[emotion] * degree_word_detect(word, document, degree_dict)
            if privative_dict:
                word_score = -1 * word_score
            document_score += word_score
        weibo_score.append(document_score)
    print("--------------------------------------------------------------------------")
    print("微博情绪分析结果为:", weibo_score)
    print("未检出情绪的微博数为", weibo_score.count(0))
    print("--------------------------------------------------------------------------")

    return weibo_score


# coord transform
def gcj02_to_bd09(lat, lng):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lat, bd_lng]


def coord_transform(location, weibo_score):
    """
    :param location: tuple, float, 经纬度
    :param weibo_score:
    :return:
    """
    location_trans = [tuple(gcj02_to_bd09(ele[0], ele[1])) for ele in location]
    latitude_trans, longitude_trans = list(zip(*location_trans))
    # html document output
    location_index = list(zip(latitude_trans, longitude_trans, weibo_score))
    out_lis = [
        {"lng": tup[1], "lat": tup[0], "count": tup[2]} for tup in location_index
    ]
    with open(r'D:\李泽宇的DESKTOP\大三上\Python现代程序设计技术\作业\第三次资料\html_out.txt', encoding='utf-8', mode='w') as fp:
        for ele in out_lis:
            fp.write(str(ele))
            fp.write(',\n')


def __main__():
    weibo_path = r'D:\李泽宇的DESKTOP\大三上\Python现代程序设计技术\作业\第三次资料\weibo_test.txt'
    base_path = r'D:\李泽宇的DESKTOP\大三上\Python现代程序设计技术\作业\第三次资料\emotion dictionary'
    degree_dict_path = r'D:\李泽宇的DESKTOP\大三上\Python现代程序设计技术\作业\第三次资料\degree dictionary.txt'
    privative_dict_path = r'D:\李泽宇的DESKTOP\大三上\Python现代程序设计技术\作业\第三次资料\privative dictionary.txt'
    documents = weibo_im(weibo_path)
    emotions_dict = emo_dict_im(base_path)
    degree_dict = degree_dict_im(degree_dict_path)
    privative_dict = privative_dict_im(privative_dict_path)
    weibo, longitude, latitude, time, location = unzip_docs(documents)
    weibo = text_preprocess(weibo)
    weibo_cut = jieba_cut(weibo)
    weibo_score = weibo_emo_score(weibo_cut, emotions_dict, degree_dict, privative_dict)
    coord_transform(location, weibo_score)


if __name__ == '__main__':
    __main__()
