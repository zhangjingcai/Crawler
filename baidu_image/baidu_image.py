#!-*-coding:utf-8-*-

import requests,json,sys,io,os,time
from concurrent import futures
# from multiprocessing import Lock
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gbk') 

def get_urls(downloads_name,downloads_number):
	headers = {
	"Accept":"text/plain, */*; q=0.01",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
	# "Connection":"keep-alive",
	'cookie': "td_cookie=2373937907; BDqhfp=%E6%B5%B7%E8%BE%B9%26%260Lock-10-1undefined%26%260%26%261; BAIDUID=E26F8B2E16E037DF58FED1FDEAD8A636:FG=1; BIDUPSID=E26F8B2E16E037DF58FED1FDEAD8A636; PSTM=1506000312; pgv_pvi=229598208; td_cookie=2463294905; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; firstShowTip=1; indexPageSugList=%5B%22%E6%B5%B7%E8%BE%B9%22%2C%22%E6%B5%B7%E5%B2%B8%22%5D; cleanHistoryStatus=0; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=null",
	"Host":"image.baidu.com",
	"Referer":"https://image.baidu.com/search",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
	"X-Requested-With":"XMLHttpRequest"
	}
	pn = 0 #pn控制图片数量
	s = set()
	for pn in range(0,int(downloads_number)):
		try:
			url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=" + downloads_name + "&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&word=" + downloads_name + "&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&pn=" + str(pn) + "&rn=30"
			r = requests.get(url,headers = headers,timeout = 0.5).text.encode("utf-8")
		except Exception as err:
			print(err)
			print("链接请求超时或者链接不存在!!")
		try:
			seejson = json.loads(r)
			temp = seejson["data"][0]['thumbURL']
			s.add(str(temp) + "\n")
		except:
			print("请求发送失败重试！")
	with open("urls.txt","w") as f:
		for url in s:
			f.write(url)
	print ("完成获取 %d 张图片的链接" % len(s))

def read_pictures(SavaPath,downloads_name):
	m = 1
	with open('urls.txt','r') as fa:
		for url in fa:
			print("正在下载第 %s 张图片" % str(m))
			path = SavaPath + str(m) + '.jpg'
			with open(path,'wb') as fb:
				r = requests.get(url)
				fb.write(r.content)
			m += 1
	print('< %s > --- 总共下载了 %s 张图片!!!' % (downloads_name,str(m - 1)))

def create_folder_path(name):
	if os.path.exists(name) == False:
		return os.makedirs(name)

def main(downloads_name,downloads_number,*args,**kwargs):
	print("正在批量下载图片: <" + downloads_name + "> 请稍等片刻...")
	SavaPath = "./" + downloads_name + "/" + downloads_name + "_"
	get_urls(downloads_name,downloads_number)#获取图片链接
	create_folder_path(downloads_name)#判断文件夹是否存在，不在则创建文件夹
	read_pictures(SavaPath,downloads_name)#下载图片
	
#多线程
def download_many1(downloads_name):
	workers = 20
	with futures.ThreadPoolExecutor(workers) as executor:
		res = executor.map(main,sorted(downloads_name.split("|")))

def download_many2(downloads_name,*args,**kwargs):
	# print("cpu number: " + str(os.cpu_count()))
	objs = []
	for download_name in downloads_name.split("|"):
		with futures.ProcessPoolExecutor() as executor:
			res = executor.submit(main,download_name,downloads_number)#异步调用: 提交/调用一个任务，不在原地等着，直接执行下一行代码
			objs.append(res)
	for obj in objs:
		obj.result()
#多线程同步	
def download_many3(downloads_name,*args,**kwargs):
	# print("cpu number: " + str(os.cpu_count())
	for download_name in downloads_name.split("|"):
		with futures.ProcessPoolExecutor() as executor:
			res = executor.submit(main,download_name,downloads_number).result()#同步调用：提交/调用一个任务，然后就在原地等着，等到该任务执行完毕拿到结果，再执行下一行代码
			executor.shutdown(wait = True)#false是进程池内部的进程都执行完毕,才会关闭，true进程都执行完毕，在执行主进程的内容

if __name__ == "__main__":	
	downloads_name = input("请输入您下载图片的名字(输入多个用'|'分隔): ")
	downloads_number = input("请输入您下载图片的数量: ")
	print("=====================================================================")
	start = time.clock()
	# download_many1(downloads_name)#启用多线程下载图片 #调用多线程需要把main函数形参downloads_number去掉
	download_many2(downloads_name,downloads_number)#启用多进程异步下载图
	# download_many3(downloads_name,downloads_number)#启用多进程同步下载图片
	end = time.clock()
	print("used time: %.2fs" % end)


#tn=baiduimage 改为
#pn控制图片数量 rn为每一页显示多少图片 例如pn=30 rn=30 为第二页的第一张图片(亲测) pn=0 为第一张 pn=29为一页的最后一张
#objURL为原图，链接通过简单映射加密
#thumbURL为缩略
