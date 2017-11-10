#!/usr/bin/env python
#-*-coding:UTF-8-*-
import re
import time
from baseConfig import BASECONFIG


class POST:
	def __init__(self, CSRFTOKEN, ipList, NAME, IPARRAY,TIME ,RSAS):
		self.CSRFTOKEN = CSRFTOKEN
		self.ipList = ipList
		self.NAME = NAME
		self.iparray = IPARRAY
		self.post_BASECONFFIG = BASECONFIG()
		self.TIME = TIME
		self.RSAS = RSAS
		self.DATA   = {
				'csrfmiddlewaretoken': self.CSRFTOKEN,
				'vul_or_pwd':'vul',
				'target':'ip',
				'ipList': self.ipList,
				'domainList':'',
				'name':self.NAME,
				'exec':'timing',
				'exec_timing_date': self.TIME,
				'exec_everyday_time':'00:00',
				'exec_everyweek_day':'1',
				'exec_everyweek_time':'00:00',
				'exec_emonthdate_day':'1',
				'exec_emonthdate_time':'00:00',
				'exec_emonthweek_pre':'1',
				'exec_emonthweek_day':'1',
				'exec_emonthweek_time':'00:00',
				'tpl':'0',
				'login_ifuse':'yes',
				'isguesspwd':'yes',
				'exec_range':'',
				'scan_pri':'2',
				'taskdesc':'',
				'report_type_html':'html',
				'report_type_xls':'xls',
				'report_content_sum':'sum',
				'report_content_host':'host',
				'report_tpl_sum':'1',
				'report_tpl_host':'101',
				'report_ifcreate':'yes',
				'report_ifsent_type':'html',
				'report_ifsent_email':'',
				'port_strategy':'user',
				'port_strategy_userports': self.post_BASECONFFIG.getPort(),
				'port_speed':'3',
				'port_tcp':'T',
				'live':'on',
				'live_icmp':'on',
				'live_tcp':'on',
				'live_tcp_ports':'21,22,23,25,80,443,445,139,3389,6000',
				'scan_level':'3',
				'timeout_plugins':'40',
				'timeout_read':'5',
				'alert_msg':'远程安全评估系统将对您的主机进行安全评估。',
				'scan_oracle':'yes',
				'encoding':'GBK',
				'csrfmiddlewaretoken':self.CSRFTOKEN,
				'pwd_smb':'yes',
				'pwd_type_smb':'c',
				'pwd_user_smb':'smb_user.default',
				'pwd_pass_smb':'smb_pass.default',
				'pwd_userpass_smb':'smb_userpass.default',
				'pwd_rdp':'yes',
				'pwd_type_rdp':'c',
				'pwd_user_rdp':'tomcat_user.default',
				'pwd_pass_rdp':'tomcat_pass.default',
				'pwd_telnet':'yes',
				'pwd_type_telnet':'s',
				'pwd_userpass_telnet': self.RSAS.getWeakPassConfig(3),
				'pwd_ftp':'yes',
				'pwd_type_ftp':'s',
				'pwd_userpass_ftp':self.RSAS.getWeakPassConfig(5),
				'pwd_ssh':'yes',
				'pwd_type_ssh':'s',
				'pwd_userpass_ssh':self.RSAS.getWeakPassConfig(1),
				'pwd_tomcat':'yes',
				'pwd_type_tomcat':'c',
				'pwd_user_tomcat':'tomcat_user.default',
				'pwd_pass_tomcat':'tomcat_pass.default',
				'pwd_mssql':'yes',
				'pwd_type_mssql':'s',
				'pwd_userpass_mssql':self.RSAS.getWeakPassConfig(6),
				'pwd_mysql':'yes',
				'pwd_type_mysql':'s',
				'pwd_userpass_mysql':self.RSAS.getWeakPassConfig(2),
				'pwd_oracle':'yes',
				'pwd_type_oracle':'s',
				'pwd_userpass_oracle':self.RSAS.getWeakPassConfig(4),
				'pwd_sybase':'yes',
				'pwd_type_sybase':'s',
				'pwd_userpass_sybase':self.RSAS.getWeakPassConfig(7),
				'pwd_db2':'yes',
				'pwd_type_db2':'c',
				'pwd_user_db2':'db2_user.default',
				'pwd_pass_db2':'db2_pass.default',
				'pwd_snmp':'yes',
				'pwd_pass_snmp':'snmp_pass.default',
				'pwd_timeout':'5',
				'pwd_timeout_time':'120',
				'pwd_interval':'0',
				'pwd_num':'0',
				'pwd_threadnum':'5',
				'loginarray': self.iparray.replace('\'','"')
				}

	def getPostData(self):
		return self.DATA