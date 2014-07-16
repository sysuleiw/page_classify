#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Implementation of Charikar simhashes in Python
# See: http://dsrg.mff.cuni.cz/~holub/sw/shash/#a1

import math
import multiprocessing
import time
import re
import os
from common import *


class Simhash():

    '''
    simhash 算法流程
    1、选择simhash的位数，请综合考虑存储成本以及数据集的大小，比如说32位
    2、将simhash的各位初始化为0
    3、提取原始文本中的特征，一般采用各种分词的方式。比如对于"the cat sat on the mat"，采用两两分词的方式得到如下结果：{"th", "he", "e ", " c", "ca", "at", "t ", " s", "sa", " o", "on", "n ", " t", " m", "ma"}
    4、使用传统的32位hash函数计算各个word的hashcode，比如："th".hash = -502157718 ,"he".hash = -369049682
    5、对各word和hashcode的每一位进行与操作，如果该位为1，则simhash相应位的值加1；否则减1
    6、对最后得到的32位的simhash，转换成实际的十进制数据
    '''

    def __init__(self, tokens='', hashbits=128):
        self.hashbits = hashbits
        self.hash = self.simhash(tokens)

    def __str__(self):
        return str(self.hash)

    def __trunc__(self):
        return math.trunc(self.hash)

    def __float__(self):
        return float(self.hash)

    def simhash(self, tokens):
        # 某些url是一个出错或者跳转js
        if not len(tokens):
            return 1
        else:
            v = [0] * self.hashbits
            string_hash = [self._string_hash(x) for x in tokens]
            for t in string_hash:
                bitmask = 0
                for i in range(self.hashbits):
                    bitmask = 1 << i
                    if t & bitmask:
                        # 查看当前bit位是否为1，是的话则将该位+1
                        v[i] += 1
                    else:
                        v[i] += -1  # 否则得话，该位减1
            # 将数组中为整数的项加到一起
            fingerprint = 0
            for i in range(self.hashbits):
                if v[i] >= 0:
                    fingerprint += 1 << i
            return fingerprint

    def _string_hash(self, v):
        if v == "":
            return 0
        else:
            x = ord(v[0]) << 7
            m = 1000003
            mask = 2 ** self.hashbits - 1
            for c in v:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(v)
            if x == -1:
                x = -2
            return x


def hamming_distance(hash1, hash2):
    # 汉明距离
    x = (int(hash1) ^ int(hash2))
    tot = 0
    # 获取1的个数
    while x:
        tot += 1
        x &= x - 1
    return tot


def similarity(hash1, hash2):
    a = float(hash1)
    b = float(hash2)
    if a > b:
        return b / a
    return a / b


def participle(content):
    '''网页源码分词方法
    通常来说相似的网站id和class都是相同的
    1.获取原网页所有的id和class
    2.统计每个单词的词频 暂时没有考虑词频


    相似度完全相同: 627类  4913个白名单
    相似度98%: 120类,最多的是55ttvv 2583  有些不太相似 例如15yiren和55ttvv
    相似度90%:64类,最多的一类2763个站点,有些不太相似

    未排重
    大家不要被样式吓坏了  比如11bbff和
    相似度完全相同: 627类  4913个白名单
    相似度98%: 105类,最多的是55ttvv 2583  有些不太相似 例如15yiren和55ttvv
    相似度90%:64类,最多的一类2763个站点,有些不太相似


    过滤掉了有iframe的站点 78个

    相似度完全相同: 608类  4913个白名单
    相似度98%: 120类,最多的是55ttvv 2583  有些不太相似 例如15yiren和55ttvv
    相似度90%:64类,最多的一类2763个站点,有些不太相
    '''
    r_id_class = re.compile(r'(?:id|class)=[\"\'](\w+)[\"\']', re.IGNORECASE)
    id_class_set = list(set(r_id_class.findall(content)))
    return id_class_set  # 暂时不考虑词频


def get_page_cont(url):
    ''' 根据url列表获取对应的url文件内容
    '''
    file = FileOper()
    filepath = Config.pages + 'www.' + url + '.html'
    filepath2 = Config.pages + url + '.html'
    if os.path.exists(filepath):
        content = file.file_read(filepath)
    elif os.path.exists(filepath2):
        content = file.file_read(filepath2)
    else:
        # print url + ' not exists'
        content = ''
    if content:
        if content.find('gb2312') > -1 or content.find('gbk') > -1:
            content = content.decode('gbk', 'ignore')
        else:
            content = content.decode('utf8', 'ignore')
        content = Config.filter_head.sub('', content)  # 过滤head之间的内容
        # 过滤掉所有的a链接,考虑到效率和准确度问题先干掉a链接
        content = Config.filter_anchor.sub('', content)
        # todo iframe 需要继续检测宽度高度,从而判断iframe是否是内容iframe,暂时注释掉
        # if content.find('iframe') == -1:  # 过滤掉有iframe的站点
        myhash = Simhash(participle(content))
        Config.ipc_simhash_list.append(
            url + ': ' + str(myhash.hash) + '\n')


def main():
    '''
        1.首先统计白名单所有域名的simhash值
    '''
    start = time.time()
    file = FileOper()
    url_list = file.file_readlines(Config.white_list)
    pool = multiprocessing.Pool(2)
    pool.map(get_page_cont, url_list)
    file.file_writelines('./hash.txt', Config.ipc_simhash_list)
    print time.time() - start  # 4100个网址耗时100秒


def main_classify():
    '''
    2.循环白名单,从第一个url遍历,寻找相似率较高的网页集合,删除此集合继续重复此过程
    '''
    start = time.time()
    file = FileOper()
    hash_list = file.file_readlines('./hash.txt')
    while len(hash_list):
        first_hash = hash_list[-1].split(':')
        result = []
        for hash in hash_list[:: -1]:
            other_hash = hash.split(':')
            simi = similarity(first_hash[1].strip(), other_hash[1].strip())
            #simi = hamming_distance(first_hash[1].strip(), other_hash[1].strip())
            if simi == 1:
                result.append(other_hash[0].strip() + '  ' + str(simi) + '\n')
                hash_list.remove(hash)
        file.file_writelines(
            Config.simhash_file + first_hash[0] + '.txt', result)
    print time.time() - start

if __name__ == '__main__':
    # 计算各个页面的hash值
    main()
    # 计算相似度
    main_classify()
