#coding:utf-8

import requests
import sys
import io
import re 
import os
import time,datetime
import codecs
import urllib
import urllib.request
import dangdang
from selenium import webdriver
from bs4 import BeautifulSoup
from collections import Iterator


class Htmlrequest(object):
	def download(self,url):
		if url is None:
			return None
		#模拟浏览器访问
		headers = {'User-Agent':'Mozilla/4.0 (Windows NT 10.0; Win64; x64) + AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393','Connection':'keep-alive'}
		# proxies = {'http':'http://127.0.0.1:1080'}
		#构造请求
		req = urllib.request.Request(url,headers=headers)
		#访问页面
		html_response = urllib.request.urlopen(req)
		return html_response.read()

class Htmlparser(object):
		
	def __init__(self):
		self.urlman = dangdang.Urlmanager()
		self.total_url = "http://category.dangdang.com/cp01.00.00.00.00.00.html"
		self.book_picture_list = []
		self.book_list = []
		self.book_dictionary = {}

	def html_analysis_link(self,html_response):	
		#获取页面内容
		self.soup = BeautifulSoup(html_response,"lxml")
		#获取书本图片链接
		book_picture = (self.soup.find('ul',id="main-img-slider")).select('img')
		for i in book_picture:
			link = i.get('src')
			link_ = (re.compile(r'\_[A-Za-z]{1}\_').sub("_w_",str(link)))
			self.book_picture_list.append(link_)
		return self.book_picture_list,self.soup
	#针对性获取页面某些信息（一旦远程页面信息改变，将出错）		
	def html_analysis_information(self,soup):
		#获取书名标题
		title_book = (re.compile(r'[\u4e00-\u9fa5]+\w')).search(str(self.soup.find("div",class_="sale_box clearfix").find('h1'))).group()
		#获取书本作者
		book_information_author = (self.soup.find(dd_name="作者")).text
		# print(book_information_author)
		#获取书本的出版社
		book_information_press = (self.soup.find(dd_name="出版社")).text
		#获取书本的价格
		book_information_price = (re.compile(r'\s¥?').sub("",(self.soup.find_all('p',id='dd-price')[0]).text))
		#获取书本所属的分类
		book_information_classify = (self.soup.find_all('span',class_="lie")[-1]).text
		# #获取书本的包装形式
		book_information_packing = ":".join(re.compile(r'：|:').split((re.compile('包 装：'+ r'[\u4e00-\u9fa5]{2,5}?')).search(str(self.soup.find_all('ul',class_='key clearfix',)[0])).group()))
		# #获取书本的出版时间		
		book_information_time = "".join((re.compile(r'出版时间\W?\w+')).findall(str(self.soup)))
		return title_book,book_information_author,book_information_press,book_information_price,book_information_classify ,book_information_packing,book_information_time

	#判断文件夹是否存在，不在则创建文件夹
	def creat_folder_path(self,folder_path):		
		if os.path.exists(folder_path) == False:
			return os.makedirs(folder_path)
	#下载图片
	def create_image_folder_path(self,book_picture_list,folder_path):
		for number,image_link in enumerate(self.book_picture_list):
			urllib.request.urlretrieve(image_link,folder_path + str(number) + '.jpg')
			print('Downloaded...' + str(number))
			time.sleep(10)
	#通过正则表达式再次优化需要的信息		
	def book_information_handle(self,book_information):
		for i in (list(book_information)):
			pattern = re.compile(r'[\u4e00-\u9fa5]{1,5}?\s?[\u4e00-\u9fa5]{1,5}?:')
			self.book_list.append(pattern.sub("",i))
		return self.book_list
	#以字典信息存放信息
	def book_information_dictionary(self,book_lists):
		self.book_dictionary["书本名字"] = book_lists[0]
		self.book_dictionary['书本信息'] = book_lists[1:]
		return self.book_dictionary
	#把书本信息写入一个文件	
	def create_book_information_file(self,folder_path,book_information_dictionarys):
		with open(str(folder_path),'w+') as f:
			f.write(str(book_information_dictionarys))

	#程序入口	
	def test(self):
		count = 1
		self.urlman.url_get(self.total_url)
		# self.urlman.test()
		while self.urlman.has_new_urls():
			try:
				url = self.urlman.get_new_url()

				htmlreq = Htmlrequest()
				html_response = htmlreq.download(url)
				htmlpar = Htmlparser()
				soup1 = htmlpar.html_analysis_link(html_response)
				book_information = htmlpar.html_analysis_information(soup1)
				# print((bytes(book_information)).decode('unicode-escape'))
				#在当前脚本路径创建一个文件夹，它以书名命名
				folder_path = './' + list(book_information)[0] + '/'
				#调用函数判断文件夹是否存在，不在则创建
				htmlpar.creat_folder_path(folder_path)
				#在当前脚本目录中，在书名文件夹下创建一个以书名命名的文件
				folder_path_file = folder_path + list(book_information)[0] + '.txt'
				#获取优化后的信息
				book_lists = htmlpar.book_information_handle(book_information)

				#调用以字典信息存放信息
				book_dictionarys = htmlpar.book_information_dictionary(book_lists)
			
				print('第',count,'本：','\n'+book_lists[0]+'\n',url)
				
				#调用函数把书本信息写入文件
				htmlpar.create_book_information_file(folder_path_file,book_dictionarys)

				#下载书名图片
				htmlpar.create_image_folder_path(self.book_picture_list,folder_path)

				if count == 5:
					break
				count += 1
			except Exception as e:
				pass

if __name__ == '__main__':
	htmlpar = Htmlparser()
	print('开始计时..............',"\n")
	start_time = datetime.datetime.now()
	htmlpar.test()
	end_time = datetime.datetime.now()
	print('总用时：%ds'% (end_time - start_time).seconds)