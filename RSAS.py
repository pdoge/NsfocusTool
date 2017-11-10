#!/usr/bin/env python
#-*-coding:UTF-8-*-
import requests
import re
import datetime
from baseConfig import BASECONFIG

class RSAS:
	def __init__(self,USERNAME,PASSWD,IP):
		self.URL = "https://" + IP
		self.HOST = IP
		self.USERNAME = USERNAME
		self.PASSWD = PASSWD
		self.SESSION = ''
		self.CSRFTOKEN = ''
		self.RSAS_HEADER = self.login()
		self.RSASCONFIG = BASECONFIG()

	def getCSRFToken(self,HTML,n = 0):
		try:
			if n == 1:
				return re.findall(r"""name='csrfmiddlewaretoken' value="(.*?)">""",HTML)[0]
			if n == 0:
				return re.findall(r"""{'data':d_s,"(.*?)',"targets":targets}""",HTML)[0]
			if n == 3:
				return re.findall(r"""<input type='hidden' value='(.*?)' name='csrfmiddlewaretoken' />""",HTML)[0]
		except:
			raise SystemExit('[-] Get Token Fail, Exitting')

	def getCookie(self,HEADER,CSRF):
		setCookie = HEADER['set-cookie']
		session = re.findall(r'sessionid=(.*?);',setCookie)[0]
		return 'csrftoken={}; sessionid={}'.format(CSRF,session)

	def getsession(self,cookie):
		return re.findall(r'=(.*?);',cookie)[0]

	def init_session(self):
		headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
					'Accept-Encoding':' gzip, deflate, br',
					'DNT': '1',
					'Connection': 'close',
					'Upgrade-Insecure-Requests': '1'
		}
		res = requests.get(url = self.URL, verify = False, headers = headers, allow_redirects = False)
		return self.getsession(res.headers['set-cookie'])

	def second_session(self):
		Cookie = self.init_session()
		self.SESSION = Cookie
		headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
					'Accept-Encoding':' gzip, deflate, br',
					'DNT': '1',
					'Connection': 'close',
					'Upgrade-Insecure-Requests': '1',
					'Cookie': 'sessionid=' + Cookie
		}
		return headers

	def check_login(self,HEADER):
		if HEADER['location'] == self.URL + '/':
			print("[+] 登录成功....")

	def login(self):
		tmp_header = self.second_session()
		res = requests.get(url = self.URL + '/accounts/login/', verify = False, headers = tmp_header, allow_redirects = False)
		CSRFTOKEN = self.getCSRFToken(res.content,1)
		self.CSRFTOKEN = CSRFTOKEN
		data = {
		'username' : self.USERNAME,
		'password' : self.PASSWD,
		'csrfmiddlewaretoken' : CSRFTOKEN
		}
		tmp_cookie = 'csrftoken='+ CSRFTOKEN + '; sessionid=' + self.SESSION
		headers={
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
					'Host': self.HOST,
					'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
					'Connection': 'close',
					'Cookie': tmp_cookie,
					'Referer': self.URL + '/accounts/login/',
					'Upgrade-Insecure-Requests': '1',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Content-Length': '87'
		}
		cookie_html = requests.post(url = self.URL + '/accounts/login_view/',data = data, verify = False, headers=headers,allow_redirects = False)
		self.check_login(cookie_html.headers)
		Cookie = self.getCookie(cookie_html.headers, CSRFTOKEN)
		headers = {
					'Host': self.HOST,
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
					'Accept': '*/*',
					'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
					'Content-Type': 'application/x-www-form-urlencoded',
					'X-Requested-With': 'XMLHttpRequest',
					'Referer': 'https://120.197.234.141/task/',
					'Cookie': Cookie +'; left_menustatue_NSFOCUSRSAS=1|0|https://'+ self.HOST +'/task/',
					'DNT': '1',
					'Connection': 'close'
		}
		return headers

	def RSASTask(self,DATA,NAME):
		sub_res = requests.post(url=self.URL+'/task/vul/tasksubmit',data=DATA,headers=self.RSAS_HEADER, verify=False)
		if 'msg:suc' in sub_res.content:
			print("[+] 成功添加任务 {}".format(NAME))
		else:
			print("[-] 添加任务失败 {}".format(NAME))

	def getrealPass(self, Keyword, HTML):
		return re.findall("""<option value='(.*?)'>{}</option>""".format(Keyword),HTML)

	def getWeakPassConfig(self, n):
		URL = self.URL + '/task/vul/base/guess/{"pwd_smb":"yes","pwd_type_smb":"c","pwd_user_smb":"smb_user.default","pwd_pass_smb":"smb_pass.default","pwd_telnet":"yes","pwd_type_telnet":"c","pwd_user_telnet":"telnet_user.default","pwd_pass_telnet":"telnet_pass.default","pwd_ssh":"yes","pwd_type_ssh":"c","pwd_user_ssh":"ssh_user.default","pwd_pass_ssh":"ssh_pass.default","pwd_timeout":"5","pwd_timeout_time":"120","pwd_interval":"0","pwd_num":"0","pwd_threadnum":"5"}'
		WeakPassPage = requests.get(url = URL, verify = False, headers = self.RSAS_HEADER)
		passwd = self.RSASCONFIG.getWeakPasswdDict()
		try:
			realSSH = self.getrealPass(passwd.pop('SSH'),WeakPassPage.content)[0]
			realMySQL = self.getrealPass(passwd.pop('MySQL'),WeakPassPage.content)[0]
			realTelnet = self.getrealPass(passwd.pop('Telnet'),WeakPassPage.content)[0]
			realOracle= self.getrealPass(passwd.pop('Oracle'),WeakPassPage.content)[0]
			realFTP = self.getrealPass(passwd.pop('FTP'),WeakPassPage.content)[0]
			realMSSQL = self.getrealPass(passwd.pop('MSSQL'),WeakPassPage.content)[0]
			realSybase = self.getrealPass(passwd.pop('Sybase'),WeakPassPage.content)[0]
			if n == 1:
				return realSSH
			if n == 2:
				return realMySQL
			if n == 3:
				return realTelnet
			if n == 4:
				return realOracle
			if n == 5:
				return realFTP
			if n == 6:
				return realMSSQL
			if n == 7:
				return realSybase
		except:
			raise SystemExit("[-] 请检查配置文件中弱密码字典配置是否有误")

	def getSysTime(self,HTML):
		try:
			sysTime = re.findall(r'<span id ="sys_time">(.*?)</span></li>',HTML)[0]
			print("[information] RSAS 系统时间: {} 所有任务延时5分钟开始".format(sysTime))
			return sysTime
		except:
			raise SystemExit("[-] 获取绿盟扫描器系统时间失败，请检查用户名或密码，现在处于登录失败状态")

	def delayFiveMin(self,TIME):
		stime = datetime.datetime.strptime(TIME,"%H:%M %Y-%m-%d")
		delayTime = stime + datetime.timedelta(minutes=5)
		return delayTime.strftime('%Y-%m-%d %H:%M:%S')

	def getSysTimeAndDelyFiveMin(self):
		url = self.URL + '/'
		clock_page = requests.get(url=url, verify=False, headers=self.RSAS_HEADER)
		return self.delayFiveMin(self.getSysTime(clock_page.content))
