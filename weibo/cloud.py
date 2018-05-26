#!coding:utf8
import os
import requests
import time
import hashlib
from selenium import webdriver
from PIL import Image
import win32api



'''
该程序实现登录微博
需要把webdriver.exe所在的目录添加到环境变量
selenium 模拟实现登录微博，如有验证码则会调用chrome.exe或者图片查看器打开验证码，以手工方式填写完成登录。 
弊端：1.登录等待时间过长。selenium加载页面过慢(网络卡等因素)会使得time.sleep()时间变长（可手动增大休眠时间)，否则会出现页面还没加载完成而执行会出错。
'''

class weibo_login(object):

    def __init__(self,username,password):
        self.username = username
        self.password = password
        # 进入浏览器设置
        self.options = webdriver.ChromeOptions()
        # 设置中文
        self.options.add_argument('lang=zh_CN.UTF-8')
        # ---------- Important ----------------
        # 设置为 headless 模式，调试的时候可以去掉
        # -------------------------------------
        # self.options.add_argument("headless")
        #--------------------------------------
        self.feeds_crawler = webdriver.Chrome(chrome_options = self.options)
        # self.feeds_crawler.set_window_size(1920,1080)
        #设置屏幕最大化
        self.feeds_crawler.maximize_window()
        self.url_login = 'https://weibo.com'
        self.localtion_code = ""
        self.input_code = ""

    def login(self):
        print('Login...')
        while(True):
            try:
                #请求登录网址
                self.feeds_crawler.get(self.url_login)
                #开始输入网址，页面在加载，这里休眠等待8s
                time.sleep(8)
                #模拟输入微博账号
                self.feeds_crawler.find_element_by_id('loginname').send_keys(self.username)
                #模拟输入微博密码
                self.feeds_crawler.find_element_by_xpath("//div[@class='info_list password']/div[@class='input_wrap']/input[@class='W_input']").send_keys(self.password)
                #输入完帐号密码后有时候会出现验证码，这里休眠等待2s验证码的出现
                time.sleep(2)
            except Exception as err:
                print("username and password output error:" + str(err))
            else:
                break
        #判断验证码存在可能性，存在则直到输入正确为止
        while(True):
            try:
                #定位验证码
                self.localtion_code = self.feeds_crawler.find_element_by_xpath("//a[@class='code W_fl']/img")
                #调用whether_heva_code()判断验证码是否存在
                if self.whether_heva_code():
                    '''
                    验证码使用比较传统的截图方法
                    '''
                    self.feeds_crawler.save_screenshot('screen.png')
                    #返回True
                    self.input_code = self.input_get_code()
                    try:
                        #模拟填写验证码
                        self.feeds_crawler.find_element_by_xpath("//div[@class='input_wrap W_fl']/input[@type='text']").send_keys(str(self.input_code))
                    except:
                        #点击页面文本框，class的值会改变
                        self.feeds_crawler.find_element_by_xpath("//div[@class='input_wrap W_fl W_input_focus']/input[@type='text']").send_keys(str(self.input_code))
                #点击登录
                self.feeds_crawler.find_element_by_xpath("//div[@class='info_list login_btn']/a[@href='javascript:void(0)']").click()
            except Exception as err:
                print("login err:" + str(err))
                print("Reconnect again")
            else:
                #判断验证码填写错误后再次刷新验证码
                try:
                    #这里2s休眠等待，加载跳转登录成功页面时间，如果2s后还没跳转，会出现意想不到的执行。
                    time.sleep(2)
                    if(self.whether_heva_code()):
                        print("信息输入错误！")
                except Exception as err:
                    print('login Success！')
                    break
    '''
    该方法判断是否存在某个属性，即验证码，存在则返回True.
    '''
    def whether_heva_code(self):
        if(self.localtion_code.get_attribute('src') == "about:blank"):
            return False
        return True 

    '''
    该方法通过前面的截图，再次截取指定范围区域(验证码区域)，然后使用resize方法把指定区域的图像素变大，最后调用chrome或者系统查看器后台打开验证码。
    '''
    def input_get_code(self):
        #获取验证码x,y坐标
        location = self.localtion_code.location
        #获取验证码的长宽
        size = self.localtion_code.size
        #写成我们需要截取的位置坐标
        rangle = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
        #打开截图
        i = Image.open('screen.png')
        #使用Image的crop函数，从截图中再次截取我们所需的区域
        screenshot_code = i.crop(rangle)
        #把截图保存到本地
        screenshot_code.save('screen_code.png')
        #再次打开截图
        im = Image.open('screen_code.png')
        #使用resize方法可以缩小扩大图片，Image.ANTIALIAS参数表达图片质量最高，
        im.resize((200,150),Image.ANTIALIAS).save('new_screen_code.png')

        #调用系统默认图片查看器打开
        # new_im = Image.open('new_screen_code.png')
        # new_im.show('new_screen_code.png')
      
        try:
            #调用win32api.ShellExecute函数以chrome打开方式验证码截图
            win32api.ShellExecute(0,'open','chromed.exe','new_screen_code.png','',0)
        except:
            #调用系统默认图片查看器打开
            os.system('new_screen_code.png')

        input_code = input("请输入验证码：")
        input_code = ''.join(input_code.split())
        return input_code

if __name__ == '__main__':
    start = time.clock()
    _login = weibo_login('14795555633','zJbV>!?3q7')
    _login.login()
    end = time.clock() - start
    print(u"花费了 %.2fs 时间" % end)





