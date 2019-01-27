#-*- coding:utf-8 -*-

class folder():
	def __init__(self,path):
		if path[-1] != '/':
			self.path = path + '/'
		else:
			self.path = path
		self.filenames = []

		self.get_filelist()

	def get_filelist(self):
		import os
		tmp = os.listdir(self.path)
		for test in tmp:
			if os.path.isfile(test):
				self.filenames.append(test)
		print 'There are %d files in "%s" folder.' %(len(self.filenames), self.path)

import re

class file():
	def __init__(self,filename):
		self.filename = filename
		with open(filename,'r') as f:
			self.raw_data = f.read().encode('hex')
		self.SOIMARKER = []

		self.get_SOIMARKER()

	def check_OI(self):
		len_SOI = len(re.findall('ffd8',self.raw_data))
		len_EOI = len(re.findall('ffd9',self.raw_data))
		print "=" * 0x30
		print "'%s' has %d SOIMARKER & %d EOIMARKER" %(self.filename, len_SOI, len_EOI)
		return len_SOI

	def get_SOIMARKER(self):
		SOIMARKER = re.finditer('ffd8', self.raw_data)
		# EOIMARKER = re.finditer('ffd9', raw_data)
		for i in SOIMARKER:
			self.SOIMARKER.append(i.start())

if __name__ == "__main__":
	filelist = folder('./').filenames
	markers = ['ffc','ffd','ffe','fff']
	for filename in filelist:
		pic1 = file(filename)
		if pic1.check_OI():
			fd = pic1.SOIMARKER[0]
			start, end = fd + 4, fd + 8

			while pic1.raw_data[start:end-1] in markers:
				start += 4
				end += 4
				index = int(pic1.raw_data[start:end],16)

				start += index * 2
				end += index * 2
				print hex(start/2), hex(end/2)
				print pic1.raw_data[start:end]
				print "==========="
			print "'%s' is jpeg"
'''
path = '.'
raw_data = []
file_list = file_search(path)
for filename in file_list:
	raw_data.append(file_read(path,filename))

print raw_data[2]
'''

