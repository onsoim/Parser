#-*- coding:utf-8 -*-

class folder():
	def __init__(self,path):
		if path[-1] != '/':
			self.path = path + '/'
		else:
			self.path = path
		self.filenames = self.get_filelist()

	def get_filelist(self):
		import os
		self.filenames = os.listdir(self.path)
		print 'There are %d files in "%s" folder.' %(len(self.filenames), self.path)
		return self.filenames

import re

class file():
	def __init__(self,filename):
		self.filename = filename

	def check_OI(self,raw_date):
		len_SOI = len(re.findall('ffd8',raw_data))
		len_EOI = len(re.findall('ffd9', raw_data))
		if len_SOI and len_EOI:
			print "There is %d SOIMARKER & %d EOIMARKER" %(len_SOI, len_EOI)

	def check_index_OI(self,raw_data):
		SOIMARKER = re.finditer('ffd8', raw_data)
		EOIMARKER = re.finditer('ffd9', raw_data)
		print "SOIMARKER: ",
		for i in SOIMARKER:
			print i.start(),
		print "\nEOIMAREKR: " ,
		for i in EOIMARKER:
			print i.start(),


if __name__ == "__main__":
	print folder('./').filenames

	with open('pic1.jpg','r') as f:
		raw_data = f.read().encode('hex')


	file('pic1.jpg').check_OI(raw_data)
	file('pic1.jpg').check_index_OI(raw_data)


'''
path = '.'
raw_data = []
file_list = file_search(path)
for filename in file_list:
	raw_data.append(file_read(path,filename))

print raw_data[2]
'''

