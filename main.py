#coding:utf8
from config import *
import re
import time
import multiprocessing
import keywords
from  Levenshtein import jaro

def get_distance_contrasted(file):
  '''获取编辑距离参照物文件
  '''
  page_content = []
  for url in keywords.kv.values():
    filepath = Config.pages+url+'.html'
    content = file.file_read(filepath)
    if content:
      if content.find('gb2312')> -1 or content.find('gbk')> -1:
        content = content.decode('gbk','ignore')
      else:
        content = content.decode('utf8','ignore')
      content = Config.filter.sub('',content) #过滤head之间的内容
      page_content.append((content,url))
      break
  return page_content

def get_page_cont(file):
  '''首先获取所有网页内容,避免重复I/O
  '''
  page_content = []
  wl = file.file_readlines(Config.white_list)
  for url in wl:
    filepath = Config.pages+url+'.html'
    content = file.file_read(filepath)
    if content:
      if content.find('gb2312')> -1 or content.find('gbk')> -1:
        content = content.decode('gbk','ignore')
      else:
        content = content.decode('utf8','ignore')
      content = Config.filter.sub('',content) #过滤head之间的内容
      page_content.append((content,url))
  return page_content

def get_classify(cont):
  '''判断当前站点所属类别,该函数为进程池目标函数
  '''
  try:
    if jaro(Config.ipc_r_kw.value[0],cont[0]) > 0.9:
      Config.ipc_list_url.append(cont[1] + '\n')
  except:
    print '#############################################'
    print Config.ipc_r_kw.value[1]

def main_distance():
  '''通过编辑距离分类入口函数
  1. 首先取出每一个类别站点内容,过滤掉head部分
  2. 利用3000个白名单站点几次计算相似度
  3. 相似度超过80%的放入一个类别
  '''
  file = FileOper()
  page_distance_contrasted = get_distance_contrasted(file)
  page_content = get_page_cont(file)
  pool = multiprocessing.Pool(multiprocessing.cpu_count())
  start = time.time()
  for idx,cont in enumerate(page_distance_contrasted):
    while len(Config.ipc_list_url):
      Config.ipc_list_url.pop()
    Config.ipc_r_kw.set(cont)
    pool.map(get_classify,page_content)
    write_file = Config.edit_dist + cont[1] + '.txt'
    file.file_writelines(write_file,Config.ipc_list_url)
    print 'idx:' + str(idx)

  print time.time()-start

if __name__ == "__main__":

  main_distance()
