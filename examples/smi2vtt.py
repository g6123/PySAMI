# -*- coding: utf-8 -*- #

from sys import argv, stderr
from pysami import Converter, ConversionError

def throw(code):
	error = ConversionError(code)
	print(error.msg, file=stderr)
	exit(error.code)

print('변환을 시작합니다.')

try:
	smi_filepath = argv[1].rsplit('.', 1)
except IndexError:
	throw(-1)

if len(smi_filepath) < 2:
	vtt_filepath = argv[1]+'.vtt'
else:
	vtt_filepath = smi_filepath[0]+'.vtt'

smi_filepath = argv[1]

try:
	converter = Converter(smi_filepath)
	vtt = converter.convert('vtt')
except ConversionError as e:
	throw(e.code)
except:
	throw(-5)

try:
	vtt_file = open(vtt_filepath, 'w')
	vtt_file.write(vtt)
	vtt_file.close()
except:
	print('변환한 자막 파일을 저장할 수 없습니다.', file=stderr)
	exit(-5)

print('성공적으로 변환했습니다.')
print('  WebVTT 파일 : '+vtt_filepath)
exit(1)