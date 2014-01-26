# -*- coding: utf-8 -*- #

# 변환 오류 클래스
class ConversionError(Exception):
	def __init__(self, code):
		self.code = code

	def __str__(self):
		return str(self.code)