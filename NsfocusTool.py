#!/usr/bin/env python
#-*-coding:UTF-8-*-
from optparse import OptionParser
from XLS import BalanceSheet
from RSAS import RSAS
from POST import POST
from baseConfig import BASECONFIG


def dealIPArray(ipList):
	realIPlist = []
	for i in ipList:
		ipdict = {
				"ip_range": i.encode('utf-8'), 
				"admin_id": "",
				"protocol": "", 
				"port": "", 
				"os": "", 
				"user_name": "", 
				"user_pwd": "", 
				"ostpls": [], 
				"apptpls": [], 
				"dbtpls": [], 
				"virttpls": [], 
				"devtpls": [], 
				"statustpls": "", 
				"jhosts": [], 
				"tpltype": "", 
				"protect": "", 
				"protect_level": "", 
				"jump_ifuse": "", 
				"host_ifsave": "", 
				"oracle_ifuse": "", 
				"ora_username": "", 
				"ora_userpwd": "",
				"ora_port": "", 
				"ora_usersid": ""
		 }
		realIPlist.append(ipdict)
	return str(realIPlist)


banner = """
 mm   m          m""                             mmmmmmm               ""#   
 #"m  #  mmm   mm#mm   mmm    mmm   m   m   mmm     #     mmm    mmm     #   
 # #m # #   "    #    #" "#  #"  "  #   #  #   "    #    #" "#  #" "#    #   
 #  # #  \"""m    #    #   #  #      #   #   \"""m    #    #   #  #   #    #   
 #   ## "mmm"    #    "#m#"  "#mm"  "mm"#  "mmm"    #    "#m#"  "#m#"    "mm 
 """


if __name__ == '__main__':
 	print(banner)
	usage = "usage: %prog [options] arg" 
	parser = OptionParser(usage=usage)
	parser.add_option("-f", "--file", dest="filename",
						help="The Excel Documention You Need To Process", metavar="FILE")
	(options, args) = parser.parse_args()
	if options.filename == None:
		raise SystemExit("[-] 使用方法： python NsfocusTool.py -f xls-Filename")
	xls = BalanceSheet('./{}'.format(options.filename))
	mainConfig = BASECONFIG()
	RSAS_Obj = RSAS(USERNAME = mainConfig.getUSERNAME(), PASSWD = mainConfig.getPASSWD(), IP = mainConfig.getIP())
	SYS_TIME = RSAS_Obj.getSysTimeAndDelyFiveMin()
	for i in range(1,xls.len()):
		ipName = xls.sheetName(i).encode('utf-8')
		ipList = ''
		for j in xls.IPTable(i):
			j = j + '\n'
			ipList += j.encode('utf-8')
		IPARRAY = dealIPArray(xls.IPTable(i))
		POST_Obj = POST(CSRFTOKEN = RSAS_Obj.CSRFTOKEN, ipList= ipList, NAME= ipName,IPARRAY= IPARRAY, TIME = SYS_TIME,RSAS= RSAS_Obj)
		RSAS_Obj.RSASTask(POST_Obj.getPostData(), ipName)