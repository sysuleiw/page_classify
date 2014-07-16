# coding:utf8
import codecs
import traceback
import multiprocessing
import re


class Config(object):

    '''存放相关配置项
    '''
    # 白名单
    white_list = '/home/apache/htdocs/wml/foxyserver/analy/data/maxcms_mode_sites.txt'

    # 网页文件目录
    pages = '/home/apache/htdocs/wml/foxyserver/analy/page/'
    #pages = './test/'

    # 存放通过分类关键字识别出来的类别域名列表
    classify = './keywords_classify/'

    # 存放通过计算编辑距离识别出来的类别域名列表
    edit_dist = './distance/'

    # 编辑距离相似度
    edit_dist_benchmark = 0.9

    ipc_list_url = multiprocessing.Manager().list()
    ipc_r_kw = multiprocessing.Manager().Value('', '')

    filter_head = re.compile(r'(<head>[\s\S]*</head>)|\s+')  # 过滤head中的内容,降低差异度
    # 过滤掉body中的a链接,降低差异度
    filter_anchor = re.compile(r'<a[\s\S]*?>[\s\S]*?</a>')

    # 计算白名单所有网页的hash值使用
    ipc_simhash_list = multiprocessing.Manager().list()

    # 存放simhash计算结果
    simhash_file = './simhash/'


class FileOper(object):

    '''文件操作类
    文件操作,读取文件,写入文件,根据值写入,根据数组写入等等
    '''

    def file_read(self, file_path):
        '''读取文件内容,返回一个字符串
        '''
        try:
            with open(file_path, 'r') as f:
                # 首先过滤字符串前后空格
                return f.read().replace('\n', '').strip().lower()
        except:
            pass

    def file_readlines(self, file_path):
        '''读取文件内容,返回一个数组
        '''
        result = []
        with open(file_path, 'r') as f:
            for line in f.readlines():
                # 首先过滤字符串前后空格
                result.append(line.replace('\n', '').strip().lower())
        return result

    def file_writelines(self, file_path, lines):
        '''写入内容到某个文件中,此时的内容是一个数组
        '''
        try:
            fw = codecs.open(file_path, 'w', 'utf-8')
            fw.writelines(lines)
            fw.close()
        except:
            print 'error!:'
            print traceback.format_stack()
            fw.close()
