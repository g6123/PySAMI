# -*- coding: utf-8 -*- #

# SAMI 파일 파싱 클래스
from os.path import isfile
from pysami.error import ConversionError

from subprocess import check_output

import re
from pysami.subtitle import Subtitle

class SmiFile:
	def __init__(self, input_file, encoding=None):
		self.data = None

		if not isfile(input_file):
			raise ConversionError(-1)

		try:
			if encoding:
				file = open(input_file, encoding=encoding)
				self.raw = file.read()
			else:
				detector = ['/usr/bin/env', 'uchardet', input_file]
				encoding_detected = check_output(detector).decode('utf-8').strip().lower()

				try:
					file = open(input_file, encoding=encoding_detected)
					self.raw = file.read()			
				except:
					if encoding_detected == 'euc-kr':
						file = open(input_file, encoding='cp949')
						self.raw = file.read()
					else:
						raise
		except:
			raise ConversionError(-2)

		file.close()

	def parse(self, verbose=False):
		search = lambda string, pattern: re.search(pattern, string, flags=re.I)

		def split_content(string, tag):
			threshold = '<'+tag

			return list(map(
				lambda item: (threshold+item).strip(),
				re.split(threshold, string, flags=re.I)
			))[1:]

		def parse_p(item):
			lang = search(item, '<p(.+)class=([a-z]+)').group(2)

			content = item[search(item, '<p(.+)>').end():]
			content = content.replace('\n', '')
			content = re.sub('<br ?/?>', '\n', content, flags=re.I)
			content = re.sub('<.*?>','', content)
			content = content.strip()

			return [lang, content]

		self.data = []
		sub_index = 1

		try:
			for item in split_content(self.raw, 'sync'):
				if verbose:
					print(str(sub_index)+' ===\n'+item+'\n')

				timecode = search(item, '<sync start=([0-9]+)').group(1)
				content = dict(map(parse_p, split_content(item, 'p')))

				self.data.append([timecode, content])
				sub_index += 1
		except:
			raise ConversionError(-3)

	def convert(self, target, lang='ENCC'):
		if self.data == None:
			raise ConversionError(-5)

		result = ''

		if target == 'vtt':
			result += 'WEBVTT'

			loop_index = 0
			sub_index = 1

			while loop_index < len(self.data):
				try:
					if self.data[loop_index][1][lang] == '&nbsp;':
						loop_index += 1
						continue
				except KeyError:
					loop_index += 1
					continue

				if loop_index == len(self.data)-1:
					end = int(self.data[loop_index][0])+60000
				else:
					end = int(self.data[loop_index+1][0])

				sub = Subtitle(
					int(self.data[loop_index][0]), end,
					self.data[loop_index][1][lang]
				)
				result += '\n\n'+str(sub_index)+'\n'+sub.vtt()

				loop_index += 1
				sub_index += 1

		else:
			raise ConversionError(-4)

		return result