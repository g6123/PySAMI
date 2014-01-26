# -*- coding: utf-8 -*- #

from sys import argv, stderr
from pysami import Converter, ConversionError

def error(code):
	error_msg = [
		'원본 자막 파일이 존재하지 않습니다.',
		'원본 자막 파일의 인코딩을 감지할 수 없습니다.',
		'원본 자막 파일은 올바른 SMI 파일이 아닙니다.',
		'변환한 자막 파일을 저장할 수 없습니다.'
	]

	print(error_msg[-(code+1)], file=stderr)
	exit(code)

try:
	smi_filepath = argv[1].rsplit('.', 1)
except IndexError:
	error(-1)

if len(smi_filepath) < 2:
	vtt_filepath = argv[1]+'.vtt'
else:
	vtt_filepath = smi_filepath[0]+'.vtt'

smi_filepath = argv[1]

try:
	converter = Converter()
	vtt = converter.convert(smi_filepath, 'vtt')
except ConversionError as e:
	error(e.code)
except:
	error(-3)

try:
	vtt_file = open(vtt_filepath, 'w')
	vtt_file.write(vtt)
	vtt_file.close()
except:
	error(-4)

exit(1)