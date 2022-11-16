# -*- coding: utf-8 -*-
# @Author    : Eurkon
# @Date      : 2021/6/5 10:16

import json
from bs4 import BeautifulSoup
import requests

HOT_URL = "https://i-lq.snssdk.com/api/feed/hotboard_online/v1/"
DOUYIN = 'https://aweme.snssdk.com/aweme/v1/hot/search/list/'

def get_weibo():
    """微博热搜
    Args:
        params (dict): {}
    Returns:
        json: {title: 标题, url: 地址, num: 热度数值, hot: 热搜等级}
    """
    data = []
    response = requests.get("https://weibo.com/ajax/side/hotSearch")
    data_json = response.json()['data']['realtime']
    jyzy = {
        '电影': '影',
        '剧集': '剧',
        '综艺': '综',
        '音乐': '音'
    }
    for data_item in data_json:
        hot = ''
        # 如果是广告，则不添加
        if 'is_ad' in data_item:
            continue
        if 'flag_desc' in data_item:
            hot = jyzy.get(data_item['flag_desc'])
        if 'is_boom' in data_item:
            hot = '爆'
        if 'is_hot' in data_item:
            hot = '热'
        if 'is_fei' in data_item:
            hot = '沸'
        if 'is_new' in data_item:
            hot = '新'
        dic = {
            'title': data_item['note'],
            'url': 'https://s.weibo.com/weibo?q=%23' + data_item['word'] + '%23',
            'num': data_item['num'],
            'hot': hot
        }
        data.append(dic)
    list = []
    for i in range(10):
        title = data[i]['title']
        list.append(title)
    return list


def get_toutiao():
    params = {'category': 'hotboard_online',
              'count': '50'}
    response = requests.get(HOT_URL, params)
    # data = response.json()['data']
    data = json.loads(response.text)['data']
    list = []
    for i in range(10):
        title = json.loads(data[i]['content'])['raw_data']['title']
        # print(item.keys())
        # print('title' in item.keys())
        list.append(title)
    return list


def get_douyin():
    resp = requests.get(DOUYIN)
    obj = json.loads(resp.text)
    word_list = obj['data']['word_list']
    list = []
    for i in range(10):
        title = word_list[i]['word']
        # print(item.keys())
        # print('title' in item.keys())
        list.append(title)
    return list


def get_baidu(board='realtime'):
    response = requests.get('https://top.baidu.com/board?tab={}'.format(board))
    soup = BeautifulSoup(response.text, 'html.parser')
    record_tags = soup.find_all('div', {'class': 'category-wrap_iQLoo'})
    titles, hot_indices = [], []
    for item in record_tags:
        title_tag = item.find('div', {'class': 'c-single-text-ellipsis'})
        hot_index_tag = item.find('div', {'class': 'hot-index_1Bl1a'})
        if (title_tag is not None) and (hot_index_tag is not None):
            titles.append(title_tag.text.strip())
            hot_indices.append(hot_index_tag.text.strip())
    list = []
    for i in range(10):
        title = titles[i]
        list.append(title)
    return list


if __name__ == '__main__':
    dict = {}
    dy = get_douyin()
    tt = get_toutiao()
    wb = get_weibo()
    bd = get_baidu()
    dict["抖音热搜"] = dy
    dict["头条热搜"] = tt
    dict["微博热搜"] = wb
    dict["百度热搜"] = bd
    with open("output.txt", 'w') as f:
        for key in dict.keys():
            f.write(key + "\n")
            for i, title in enumerate(dict[key]):
                f.write(str(i + 1) + ": " + title + "\n")
            f.write("\n--------------------------\n")

