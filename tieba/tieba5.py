#!coding:utf8-*-

import ssl
from urllib import request,parse
from lxml import  etree
from urllib.parse import urlencode
import os,time

#写一个解析url并返回相应的内容,再使用HTML()方法解析文档
def url_read(url):
    req = request.Request(url)
    Context = ssl._create_unverified_context()
    reponse = request.urlopen(req,context = Context)
    # html = reponse.read().decode('utf8')
    html = reponse.read()
    return html

#找帖子链接
def loadPage(url,page,tieba_name):
    html = url_read(url)
    content = etree.HTML(html)
    link_list = content.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
    for tiezi_num,tiezi_link in enumerate(link_list):
        link = "https://tieba.baidu.com" + tiezi_link				
        print("正在下载%s吧第%s页,第%d个帖子链接:%s" % (tieba_name,page, tiezi_num + 1,link))
        download_image(link,tieba_name,tiezi_num + 1,page)


#进入帖子页面获取帖子图片链接
def loadImage(url):
    html = url_read(url)
    content = etree.HTML(html)
    link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    return link_list


#通过图片链接下载图片
def download_image(url,tieba_name,tiezi_num,page):
    try:
        path = create_file_folder(tieba_name,tiezi_num,page)
        num = 1
        html = url_read(url)
        link_list = loadImage(url)
        for link in link_list:
            with open(path + str(num) + ".jpg",'wb') as fa:
                image = url_read(link)
                fa.write(image)
            print("第%d张图" % (num))    
            #print(link)
            num += 1
    except Exception as e:
        print("该帖子连接超时; ",e)
#获取页数页面
def tiebaSpider(url,beginPage,endPage,tieba_name):
    for page in range(beginPage,endPage + 1):
        pn = 50 * (page - 1)
        url = url +  "&pn=" + str(pn)
        print("正在加载:\n" + "第" + str(page) + "页.html") 
        loadPage(url,page,tieba_name)	
#创建文件夹		
def create_file_folder(name,number,page):
    path = "./" + name + "/" + "/" + "第%s页" % (page) + "/" + str(number) + "/"
    if os.path.exists(path) == False:
        os.makedirs(path)
    return path

if __name__ == "__main__":
    start = time.clock()
    url = "https://tieba.baidu.com/f?"
    tieba_name = input("请输入查找的贴吧名：")
    begin = int(input("请输入查找开始页数: "))
    end = int(input("请输入查找结束页数: "))
    encode_tieba_name = urlencode({"kw":tieba_name})
    url = url + encode_tieba_name
    tiebaSpider(url,begin,end,tieba_name)
    used_time = time.clock() - start
    print("used time:%.5f" % used_time)