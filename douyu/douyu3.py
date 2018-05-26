from concurrent import futures
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re,time,io,sys,os
import shutil
#windows系统默认编码是gbk，为了编码出错，把系统编码方式改为utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 
start = time.clock()

foldth_name = input("欢迎您来到斗鱼直播间,输入一个保存直播间信息的文件夹名:")
def create_file_folder(name):
	try:
		path = "./" + foldth_name + "/"
		if os.path.exists(path) == False:
			os.makedirs(path)
			g = open(path + 'douyu.txt','w')
			g.close()
	finally:
		print("文件夹创建完成!")   
	return path
path = create_file_folder(foldth_name)

def driver_2(i):
	pattern1 = re.compile('\d*\.?\d+') #匹配观看人数
	pattern2 = re.compile('\n')# 匹配前一个列表返回的text，它们含有"\n"换行符，此表达式匹配一个换行符
	pattern3 = re.compile('万')
	num = 0 #有多少直播
	count = 0.0 #有多少观众
	page = 1 #有多少页
	with open(path + 'douyu.txt','a',encoding='utf8') as f:
			f.write(i.text + '\n\n\n\n')
		#watch_tv_list返回一个元素信息列表，遍历每个元素信息，使用get_attribute()获取属性。最后返回一个链接
	link = i.get_attribute("href")
	#此表达式经过正则匹配最后留下 直播间人数(带“万”或不带“万”都返回)
	watch_tv_list_all = pattern2.split(i.text)
	sys.stdout.flush()
	print("欢迎来到斗鱼直播间第%s页:\t" % str(page))
	print("该直播间链接是:\t" + link)
	print("该直播间类型是:\t" + watch_tv_list_all[1])
	print("该直播间标题是:\t" + watch_tv_list_all[0])
	print("该直播间主播是:\t" + watch_tv_list_all[2])
	print("该直播间人数是:\t" + watch_tv_list_all[3])
	print()
	watch_tv_people_or_wan = pattern2.split(i.text)[-1]
	#print(watch_tv_people_or_wan)
	#判断是否带“万”，配到到则返回一个match对象，若直到最后无法匹配，则返回None
	match = pattern3.search(watch_tv_people_or_wan)
	if match == None:
		watch_tv_people_no_wan = ''.join(pattern1.findall(watch_tv_people_or_wan))
		if watch_tv_people_no_wan == "" and isinstance(watch_tv_people_no_wan,(float,int)):
			pass
		else:
			count += int(watch_tv_people_no_wan)#总计不带”万“人数
	else:
		watch_tv_people_have_wan = ''.join(pattern1.findall(watch_tv_people_or_wan))
		if watch_tv_people_have_wan == "" and isinstance(watch_tv_people_no_wan,(float,int)):
			pass
		else:
			count += float(watch_tv_people_have_wan) * 10000 #总计带”万“人数
	
	print("观众人数：" + str(count//10000) + "万人")

def driver_():
	try:

		driver = webdriver.Chrome()
		driver.get("https://www.douyu.com/directory/all")
	except Exception as e:
		print(e)
		print('PnantomJS.exe环境变量或者指定的路径未设置成功')
	#此表达式可以匹配到每个直播间信息，包含直播间名称，直播间类型，备注，直播间主播，直播间人数
	watch_tv_list = driver.find_elements_by_xpath("//div[@id='live-list-content']/ul/li/a[@class='play-list-link']")
	return(watch_tv_list)

def test():#采用多线程
	workers = 20
	watch_tv_list = driver_()
	with futures.ThreadPoolExecutor(workers) as executor:
		res = executor.map(driver_2,watch_tv_list)
	return len(watch_tv_list)


end = time.clock() - start
print("当前直播数量：" + str(test()) + "个")
print("used time: %.2fs" % end)

