# coding:utf8
import time
import multiprocessing
import keywords
from Levenshtein import jaro
from common import *


def get_page_cont(file, url_list):
    ''' 根据url列表获取对应的url文件内容
    '''
    page_content = []
    for url in url_list:
        filepath = Config.pages + url + '.html'
        content = file.file_read(filepath)
        if content:
            if content.find('gb2312') > -1 or content.find('gbk') > -1:
                content = content.decode('gbk', 'ignore')
            else:
                content = content.decode('utf8', 'ignore')
            content = Config.filter_head.sub('', content)  # 过滤head之间的内容
            content = Config.filter_anchor.sub('', content)  # 过滤掉所有的a链接
            page_content.append((content, url))
    return page_content


def get_classify(tuple_cont):
    '''判断当前站点所属类别,该函数为进程池目标函数
    '''
    try:
        if jaro(Config.ipc_r_kw.value[0], tuple_cont[0]) > Config.edit_dist_benchmark:
            Config.ipc_list_url.append(tuple_cont[1] + '\n')
    except:
        print '#############################################'
        print Config.ipc_r_kw.value[1]


def main():
    '''通过编辑距离分类入口函数
    1. 首先取出每一个类别站点内容,过滤掉head部分
    2. 利用3000个白名单站点几次计算相似度
    3. 相似度超过80%的放入一个类别
    '''
    file = FileOper()

    # 获取编辑距离参照物文件
    url_list = keywords.kv.values()
    page_distance_contrasted = get_page_cont(file, url_list)

    # 获取白名单文件,防止重复进行I/O操作
    url_list = file.file_readlines(Config.white_list)
    page_content = get_page_cont(file, url_list)

    # 初始化进程池
    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    start = time.time()

    for idx, tuple_cont in enumerate(page_distance_contrasted):
        # 每一个被比较的url被比较前需要清空共享对象
        while len(Config.ipc_list_url):
            Config.ipc_list_url.pop()

        Config.ipc_r_kw.set(tuple_cont)
        pool.map(get_classify, page_content)
        write_file = Config.edit_dist + tuple_cont[1] + '.txt'
        file.file_writelines(write_file, Config.ipc_list_url)
        print 'idx:' + str(idx)

    print time.time() - start


if __name__ == "__main__":
    main()
