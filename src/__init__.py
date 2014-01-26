# -*- coding: utf-8 -*- #

# 변환 작업 클래스
class Converter:
	def __init__(self, detector=['/usr/bin/env', 'uchardet']):
		self.detector = detector

	def convert(self, file, target, lang='KRCC'):
		smi_file = SmiFile(file, self.detector)
		smi_file.parse()
		return smi_file.convert(target, lang)

# SAMI 파일 파싱 클래스
from os.path import basename, isfile
from pysami.error import ConversionError

from subprocess import check_output

import re
from pysami.subtitle import Subtitle

class SmiFile:
	def __init__(self, path, detector):
		self.data = None
		self.filename = basename(path)

		if not isfile(path):
			raise ConversionError(-1)

		charset_auto = check_output(detector+[path]).decode('utf-8').strip().lower()
		try:
			file = open(path, encoding=charset_auto)
			self.raw = file.read()
		except:
			if charset_auto == 'euc-kr':
				try:
					file = open(path, encoding='cp949')
					self.raw = file.read()
				except:
					raise ConversionError(-2)
			else:
				raise ConversionError(-2)

		file.close()

	def parse(self):
		def split_content(string, tag):
			result = []
			last = False

			get_first_start = lambda string, tag: string.lower().find('<'+tag)
			def get_second_start(string, tag):
				offset = len(tag)+1
				result = get_first_start(
					string[get_first_start(string, tag)+offset:], tag
				)+offset

				if result < len(tag)+1:
					return -1
				else:
					return result

			while not last:
				first_start = get_first_start(string, tag)
				second_start = get_second_start(string, tag)

				if second_start < 0:
					first = string[first_start:]
					last = True
				else:
					first = string[first_start:second_start]
					string = string[second_start:]

				result.append(first.strip())

			return result

		def parse_p(item):
			lang = search(item, '<p(.+)class=([a-z]+)').group(2)
			content = item[search(item, '<p(.+)>').end():]
			return [lang, content.strip()]

		self.data = []
		search = lambda string, pattern: re.search(pattern, string, flags=re.I)
		data = self.raw[
			search(self.raw, '<body>').end() : search(self.raw, '</body>').start()
		]

		for item in split_content(data, 'sync'):
			timecode = search(item, '<sync start=([0-9]+)').group(1)
			content = dict(map(parse_p, split_content(item, 'p')))
			self.data.append([timecode, content])

	def convert(self, target, lang):
		if self.data == None:
			self.parse()

		result = ''

		if target == 'vtt':
			result += 'WEBVTT FILE'

			loop_index = 0
			sub_index = 1

			while loop_index < len(self.data):
				if self.data[loop_index][1][lang] == '&nbsp;':
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
			raise TypeError('Unsupported format: '+target)

		return result