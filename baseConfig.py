#!/usr/bin/env python
#-*-coding:UTF-8-*-
import ConfigParser



class BASECONFIG:
	def __init__(self):
		self.cfg = ConfigParser.ConfigParser()
		try:
			self.configFile = open('./RSASConfig.ini', 'r')
		except:
			raise SystemExit('[-] Open config-file Fail')
		self.cfg.readfp(self.configFile)

	def getUSERNAME(self):
		USERNAME = self.cfg.get('LOGIN','Username')
		return USERNAME
	def getPASSWD(self):
		PASSWD = self.cfg.get('LOGIN','Passwd')
		return PASSWD
	def getIP(self):
		IP = self.cfg.get('RSAS','IP')
		return IP
	def getWeakPasswdDict(self):
		SSH = self.cfg.get('WEAK-PASSWD-CONFIG', 'SSH')
		telnet = self.cfg.get('WEAK-PASSWD-CONFIG', 'Telnet')
		Oracle = self.cfg.get('WEAK-PASSWD-CONFIG', 'Oracle')
		FTP = self.cfg.get('WEAK-PASSWD-CONFIG', 'FTP')
		Sybase = self.cfg.get('WEAK-PASSWD-CONFIG', 'Sybase')
		MSSQL = self.cfg.get('WEAK-PASSWD-CONFIG','MSSQL')
		MySQL = self.cfg.get('WEAK-PASSWD-CONFIG','MySQL')
		WeakPass = {
			'SSH' : SSH,
			'Telnet' : telnet,
			'Oracle' : Oracle,
			'FTP'    : FTP,
			'Sybase' : Sybase,
			'MSSQL'  : MSSQL,
			'MySQL'  : MySQL
		}
		return WeakPass

	def getPort(self):
		port = self.cfg.get('SCANNER-CONFIG','port')
		return port
