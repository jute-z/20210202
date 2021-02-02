from selenium import webdriver
from time import sleep
import win32gui
import win32con
import xlrd
import os
#加载小应用配置文件
try:
	#定义文件名
	file_name1 = '小应用'
	#获取当前路径
	global route
	route = os.getcwd()
	#获取route路径下的所有文件
	global files
	files= os.listdir(route)
	#检查每一个文件
	#判断是否是文件
	for item in files:
		if os.path.isfile(os.path.join(route,item)):
			if item.find(file_name1) != -1:
				appfilename = os.path.join(route,item)
	#打开文件
	appfile =xlrd.open_workbook(appfilename)
except:
	print("小应用文件有误")
#加载小应用发布范围文件
try:
	#定义文件名
	file_name2 = '应用发布范围'
	#判断是否是文件
	for item in files:
		if os.path.isfile(os.path.join(route,item)):
			if item.find(file_name2) != -1:
				appreleaserangename = os.path.join(route,item)
	#打开文件
	appreleaserange = xlrd.open_workbook(appreleaserangename)
except:
	print("应用范围文件有误")
#指定文件sheet页
sheet_appfile = appfile.sheet_by_index(0)
sheet_appreleaserange = appreleaserange.sheet_by_index(0)
#输入tcm地址、用户名、密码
# data_url = input("请输入tcm地址：")
# data_user = input("请输入tcm的用户名：")
# data_password = input("请输入tcm的用户密码：")
#禁止web页面弹窗之类的东西
options = webdriver.ChromeOptions()
#初始化webdriver.Chrome，赋值打开模式及驱动位置
driver = webdriver.Chrome(chrome_options=options,executable_path=(r'D:\python\chromedriver.exe'))
#打开的页面最大化
driver.maximize_window()
#打开tcm
driver.get(r'https://yqtpoc3.sinosun.com:19446/static/tcm/pages/login.html')
sleep(1)
#登陆
driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div[2]/div[1]/input").send_keys('yunwei001')
driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div[2]/div[2]/input").send_keys('Aaaa1111')
driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div[2]/div[4]/div").click()
sleep(2)
#打开应用管理
driver.get('https://yqtpoc3.sinosun.com:19446/static/appstore/appmgr/appmgr.html?type=7&from=app')#不同tcm版本需要更改
for i_1 in range(1,int(sheet_appfile.nrows)):
	sleep(1)
	#点击创建
	driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div").click()
	#点击上传logo按钮
	driver.find_element_by_xpath("//*[@id='logoUpload']").click()
	sleep(1)
	appinfo = sheet_appfile.row_values(rowx=i_1)
	filepath = appinfo[0] 
	#打开一级窗口
	dialog = win32gui.FindWindow('#32770','打开')
	#向下传递
	ComboBoxEx32 = win32gui.FindWindowEx(dialog,0,'ComboBoxEx32',None)
	comboBox = win32gui.FindWindowEx(ComboBoxEx32,0,'comboBox',None)
	#编辑按钮
	edit = win32gui.FindWindowEx(comboBox,0,'edit',None)
	#打开按钮
	button = win32gui.FindWindowEx(dialog,0,'Button','打开(&O)')
	#上传文件点击打开
	win32gui.SendMessage(edit,win32con.WM_SETTEXT,None,filepath)
	win32gui.SendMessage(dialog,win32con.WM_COMMAND,1,button)
	#输入小应用名称
	driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[1]/div[2]/div/input").send_keys(appinfo[1])
	#输入小应用id+授权码
	driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[2]/div[1]/div/input").send_keys(int(appinfo[2]))
	driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[2]/div[2]/div/input").send_keys(int(appinfo[3]))
	#是否登陆授权，默认选定否
	if appinfo[4] == 0:
		driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[2]/div[3]/div/label[2]/input").click()
	#输入小应用链接
	driver.find_element_by_xpath("//*[@id='homeAddr']").send_keys(appinfo[8])
	driver.find_element_by_xpath("//*[@id='pcHomeAddr']").send_keys(appinfo[9])
	#数据统计入口
	driver.find_element_by_xpath("//*[@id='backAddr']").send_keys(appinfo[10])
	#小应用标识，默认选定私有云
	if appinfo[11] == 0:
		driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[4]/div[4]/span[2]/div[1]/div/label[2]/input").click()
	#支持平台，默认全选
	if '1' not in appinfo[12]:
		driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[4]/div[4]/span[4]/div[1]/div/div[1]/label/input").click()
	if '2' not in appinfo[12]:
		driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[4]/div[4]/span[4]/div[1]/div/div[2]/label/input").click()
	if '3' not in appinfo[12]:
		driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[4]/div[4]/span[4]/div[1]/div/div[3]/label/input").click()
	#是否支持模板，默认不支持
	if appinfo[13] == 1:
		driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[4]/div[4]/span[4]/div[2]/div/label[2]/input").click()
	#是否需要身份验证，默认不需要
	if appinfo[14] == 0:
		driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div/form/span[4]/div[4]/span[4]/div[3]/div/label[2]/input").click()
	#免责声明
	driver.find_element_by_xpath("//*[@id='disclaimerContent']").send_keys(appinfo[15])
	sleep(1)
	#提交
	driver.find_element_by_xpath("//*[@id='submit']").click()
	sleep(2)
	#点击上架
	driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/table[3]/tbody/tr[1]/td[3]/span[1]").click()
	sleep(1)
	#点击确定
	driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/span[1]").click()
	sleep(1)
	#点击小应用中心
	driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/ul/span[1]/a[1]/li").click()
	sleep(1)
	#搜索小应用名称
	driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/span/input").send_keys(appinfo[1])
	driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/span/span").click()
	sleep(1)
	#点击开通
	driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/table[1]/tbody/tr/td[3]/span").click()
	sleep(2)
	#选择入口
	for i_2 in range(1,int(sheet_appreleaserange.nrows)):
		appreleaserangeinfo = sheet_appreleaserange.row_values(rowx=i_2)
		appname_releaserange = appreleaserangeinfo[0] 
		if appname_releaserange == appinfo[1]:
			entrance = appreleaserangeinfo[3]
			if "工作台" in entrance:
				driver.find_element_by_xpath("/html/body/div[11]/div/div[2]/div[2]/form/div[1]/div[1]/label[1]/input").click()
			if "我的" in entrance:
				driver.find_element_by_xpath("/html/body/div[11]/div/div[2]/div[2]/form/div[1]/div[1]/label[2]/input").click()
		else:
			pass
	#点击按规则
	driver.find_element_by_xpath("/html/body/div[11]/div/div[2]/div[2]/form/div[2]/div[2]/label/input").click()
	#选择服务规则
	driver.find_element_by_xpath("/html/body/div[11]/div/div[2]/div[2]/form/div[4]/div[2]/div[1]/input").click()
	driver.find_element_by_xpath("/html/body/div[12]/div/div[2]/div[6]/div[1]/label/input").click()
	sleep(1)
	#点击确定
	driver.find_element_by_xpath("/html/body/div[12]/div/div[2]/div[8]/span[1]").click()
	sleep(1)
	driver.find_element_by_xpath("/html/body/div[11]/div/div[2]/div[3]/span[1]").click()
	sleep(1)






	





