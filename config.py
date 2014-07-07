#coding:utf8
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

  ipc_list_url = multiprocessing.Manager().list()
  ipc_r_kw = multiprocessing.Manager().Value('','')

  filter = re.compile(r'(<head>[\s\S]*</head>)|\s+')  # 过滤head中的内容,降低差异度
# 分类关键字
  keywords = ['/images/css.{1,2}css"rel="styleshee',
    '如果浏览器版本过老访问本站可能会较卡',
    '哥哥射提供最新最快的自拍偷拍',
    'href="/jss/style.css">',
    '<SCRIPT src="/js/index.js" type=text/javascript>',
    'src="/js/layout.js"',
    'href="/templets/.{2,20}/s.css">',
    'document.writeln\(tongji\)',
    '奇米影视成人社区',
    'id="css" href="/css/style..css">',
    '<div class=.center margintop border clear menu',
    '/templets/css/styles.css',
    '/templets/.{3,20}/css/style.css',
    '/templets/temsys/css.css',
    '/css/menu.js',
    '<div style="display:none"><script type="text/javascript" src="/js/count.js"></script></div>',
    'href="/css/acss.css"/>',
    '<link href="/css/dy.css"',
    'src="/sxgg/tj.js">',
    '<link href="/css/..css"',
    '/css/css/style.css',
    'rc="imageabc/index.js"',
    'name=GENERATOR content="MSHTML 8.00.6001.19258"',
    '/template/.{3,20}/images/index.css',
    'imageabc/style..css',
    'class=wrap><DIV class=gonggao><DIV id=toubiao>',
    '.headerArea{height:25%;background',
    '/template/.{3,20}/images/css..css',
    '<META name=GENERATOR content="MSHTML 8.00.6001.23486">',
    'href="/imageabc/css.css"',
    'ref="/css/list.css"typ',
    'href="/template/.{3,20}/images/list.css"',
    'href="/skins/index.css"',
    'images/dy.css"rel="sty',
    '/template/.{3,20}/images/css.css',
    '/images/.{0,5}sex/style.css',
    '/template/.{3,20}/images/style.css',
    'href="/css/new.css"rel',
    '.headerArea{background',
    'centerdh margintop border cleardh adspic top',
    '/skins/.{2,4}/images/index.css',
    'template/.{3,20}/images/style...css',
    'template/.{3,20}/images/style..css',
    '<META content="MSHTML 6.00.2900.5512" name=GENERATOR>',
    'bgcolor="#DBF1D4">',
    'href="/css/style.css"rel="styleshe',
    'href="/static/css/base.css"',
    '/templets/.{3,12}/images/index.css',
    '/templets/.{2,12}/images/astyle.css',
    '/skin/images/style.css',
    '禁止中国人士请勿进入',
    '<META name=GENERATOR content="MSHTML 9.00.8112.16447">',
    '/styles/c..css',
    '<link href="/images/list.css" type=text/css rel=stylesheet>',
    '/templets/.{3,12}/images/list.css',
    'rel="stylesheet" type="text/css" id="css" href=""',
    'href="/imageabc/.{3,12}css"rel',
    '/theme/.{6,12}/css/style.css',
    '/Tpl/.{3,12}//images/index.css',
    'template/default/template.css',
    '/skins/.{2,6}/images/style.css',
    '"激情五月 色播五月 色五月 开心五月 丁香五月 五月婷婷 深爱五月"',
    'gemgsx.com/css/index.css"',
    '/template/.{5,10}/images/layout.css',
    '/template/default/images/css/style.css',
    '<div class="copyright">为了你的健康未成年人访问请自觉离开',
    '/templets/files/css.css',
    '.menu a{ float:left; width:80px; text-align:center; padding:8px 0px 6px 0px; font-size:14px;',
    'href="/template/se/images/list.css"',
    '"/template/index.css"',
    '/template/paody/css/style.css',
    '/template/.{5,10}/images/\w{8,}.css',
    'href="/template/../images/style.css"rel',
    '<body bgcolor="#C0C0C0">',
    '/templets/[2-9]{3,5}/images/style.css',
    '<td height="60" bgcolor="#DDF4CE"><font size="5"><strong>',
    'href="/Tpl/.{2,5}/images/list.css"',
    '<LINK id=css rel=stylesheet type=text/css href="/css/style1.css">',
    'href="/pic/dy.css"rel="stylesheet"', 
    ]

class FileOper(object):

  '''文件操作类
  文件操作,读取文件,写入文件,根据值写入,根据数组写入等等
  '''

  def file_read(self, file_path):
    '''读取文件内容,返回一个字符串
    '''
    try:
      with open(file_path, 'r') as f:
        return f.read().replace('\n', '').strip()  # 首先过滤字符串前后空格
    except :
      pass

  def file_readlines(self, file_path):
    '''读取文件内容,返回一个数组
    '''
    result = []
    with open(file_path, 'r') as f:
      for line in f.readlines():
        result.append(line.replace('\n', '').strip())  # 首先过滤字符串前后空格
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
