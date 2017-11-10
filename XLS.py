#!/usr/bin/env python
#-*-coding:UTF-8-*-
try:
	import xlrd
except:
	raise SystemExit('[Error] Please install "xlrd": e.g. pip install xlrd')
import re

class BalanceSheet:
	def __init__(self,PATH):
		self.PATH = PATH
		self.DATA = self.openXls(PATH)

	def IPTable(self,n):
		list_content = self.getAllValue(self.xlsSheet(self.DATA,n))
		if list_content != 0:
			return self.cleanAndRmDup(list_content)

	def openXls(self,PATH):
		try:
			data = xlrd.open_workbook(self.PATH)
		except:
			raise SystemExit('[Error] 打开文件失败，请把Excel文件另存为Excel 97-2003 工作薄后重试！')
		return data

	def xlsSheet(self,data,num):
		return data.sheets()[num]

	def getNrows(self,sheet):
		return sheet.nrows

	def getNcols(self,sheet):
		return sheet.ncols

	def getValue(self,sheet,row,col):
		return sheet.cell(row,col).value

	def getAllValue(self,sheet):
		if self.getNcols(sheet) == 0 or self.getNrows(sheet) == 0:
			print '[-]   Sheet为空......'
			return 0
		else:
			ValueList=[]
			for i in range(self.getNrows(sheet)):
				for j in range(self.getNcols(sheet)):
					ValueList.append(self.getValue(sheet,i,j))
			return ValueList

	def cleanAndRmDup(self,list):
		cleanList=[]
		for i in list:
			if i != '' and isinstance(i,(str,unicode)):
				foundItem =  re.findall(r'(\d+\.\d+\.\d+\.\d+/?\d*)',i)# 究竟'/'是不是表示一个网段
				if len(foundItem) > 0:
					cleanList.append(foundItem[0].strip())
		return set(cleanList)

	def sheetName(self,n):
		return self.DATA.sheets()[n].name

	def len(self):
		return len(self.DATA.sheets())
