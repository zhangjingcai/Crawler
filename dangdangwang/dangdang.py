#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import io
import re 
import os
import time
import codecs
import urllib
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
from collections import Iterator
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

class Urlmanager(object):

	def __init__(self):
		self.old_urls = set()
		self.new_linkss = set()
		self.new_links = {}#网页内容中每一类的链接
		self.title_links = set()#网页内容中每一类下每一本书的链接
		self.new_urls = set()

	def has_new_urls(self):
		return len(self.new_urls) != 0

	def get_new_url(self):
		# print('删除前:',self.new_urls)
		new_url = self.new_urls.pop()
		# print('删除了:',new_url)
		self.old_urls.add(new_url)
		return new_url

	def add_new_url(self,url):
		# print(url)
		if url is None:
			return
		if url not in self.new_urls or url not in self.old_urls:
			self.new_urls.add(url)

	#next()迭代每一个链接,然后调用add_new_url()方法把链接添加到集合
	def add_new_urls(self,urls):
		if urls is None or len(urls) == 0:
			return
		urls_ = iter(urls)
		while True:
			try:
				self.add_new_url(next(urls_))
				if count == 15:
					break
				count += 1
			except StopIteration:
				break
	# v	为每一类书的链接	
	def add_new_links(self,new_links):
		count = 1
		for (k,v) in self.new_links.items():
			for vv in v:
				if count == 3:
					break
				count += 1
				self.url_get2(vv)
	#获取网页内容中每一类的页面内容
	def url_get(self,url):
		headers = {'User-Agent':'Mozilla/4.0 (Windows NT 10.0; Win64; x64) + AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393','Connection':'keep-alive'}		
		proxies = {
		'http':'http://127.0.0.1:1080'
		}
		req = urllib.request.Request(url,headers=headers)
		url_response = urllib.request.urlopen(req)
		soup = BeautifulSoup(url_response,'lxml')
		self.url_get_linkone(soup,url)
	#获取网页内容中每一类下每一本书的的页面内容
	def url_get2(self,url):
		driver = webdriver.Chrome("D:/Users/Rosefinch/AppData/Local/Programs/Python/Python36-32/chromedriver_win32/chromedriver")
		driver.get(url)
		soup = driver.page_source
		soup2 = BeautifulSoup(soup,'lxml')
		driver.close()
		self.url_get_linktwo(soup2)
	##获取网页内容中每一类书的链接，返回网页中所有链接
	def url_get_linkone(self,soup,url):		
		links = (soup.find_all('a',href=re.compile(r'cp01.\d{1}[1-9]{1}.00.00.00.00.html')))
		for link in links:
			link_ = link['href']
			new_full_url = urllib.parse.urljoin(url,link_)
			self.new_linkss.add(new_full_url)
		self.new_links[url] = self.new_linkss
		self.add_new_links(self.new_links)

	#获取每一类下的每一本书链接，返回一个无序字典
	def url_get_linktwo(self,soup2):		
		title_links_ = soup2.find_all('a',href=re.compile(r'http://product.dangdang.com/.*\.html$'))
		for title_link_ in title_links_:
			title_link = title_link_['href'] 
			self.title_links.add(title_link)
		self.add_new_urls(self.title_links)	
