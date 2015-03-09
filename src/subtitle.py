# -*- coding: utf-8 -*- #

# 자막 데이터 클래스
class Subtitle:
	def __init__(self, start, end, content):
		self.start = start
		self.end = end
		self.content = content

	def vtt(self):
		result = self.ms_to_stamp(self.start)
		result += ' --> '
		result += self.ms_to_stamp(self.end)
		result += '\n'
		result += self.content
		return result

	@staticmethod
	def ms_to_stamp(ms):
		ms = ms/1000
		s = int(ms)
		ms = str(ms).split('.', 1)[1]

		if s > 59:
			m = int(s/60)
			s = s % 60

			if m > 59:
				h = int(m/60)
				m = (m % 60)
			else:
				h = 0

		else:
			m = 0
			h = 0

		ms = '{:<03}'.format(ms)

		return str(h).zfill(2)+':'+str(m).zfill(2)+':'+str(s).zfill(2)+'.'+ms
