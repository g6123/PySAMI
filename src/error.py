# -*- coding: utf-8 -*- #

messages = [
	'원본 자막 파일이 존재하지 않습니다.',

	'원본 자막 파일의 인코딩을 감지할 수 없습니다.',

	"""원본 자막 파일은 올바른 SMI 파일이 아닙니다.
verbose 옵션은 오류의 발생 위치를 확인하는 데 도움을 줄 수 있습니다.""",

	"""지정한 파일 형식으로는 변환할 수 없습니다.
(지원 목록 : vtt)""",

	'알 수 없는 오류가 발생했습니다.'
]

# 변환 오류 클래스
class ConversionError(Exception):
	def __init__(self, code):
		self.code = code
		self.msg = error_msg[-(code+1)]

	def __str__(self):
		return self.msg+' ('+str(self.code)+')'