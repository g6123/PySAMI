# -*- coding: utf-8 -*- #

# 변환 오류 클래스
class ConversionError(Exception):
	messages = (
		'Cannot access to the input file.',
		'Cannot find correct encoding for the input file.',
		'Cannot parse the input file. It seems not to be a valid SAMI file.\n(Verbose option may show you the position the error occured in)',
		'Cannot convert into the specified type. (Suppored types : vtt)',
		'Cannot convert the input file before parsing it.',
		'Unknown error occured.'
	)

	def __init__(self, code):
		self.code = code
		self.msg = self.messages[-(code+1)]

	def __str__(self):
		return self.msg+' ('+str(self.code)+')'
