# -*- coding: utf-8 -*- #

from sys import argv, stderr
from pysami import SmiFile, ConversionError

def throw(code):
	error = ConversionError(code)
	print(error.msg, file=stderr)
	exit(-1*code)

try:
	smi_filepath = argv[1]
except IndexError:
	throw(-1)

vtt_filepath = smi_filepath.rsplit('.', 1)[0]+'.vtt'

try:
	smi = SmiFile(smi_filepath)
	smi.parse()
	vtt = smi.convert('vtt', 'KRCC')
except ConversionError as e:
	throw(e.code)
except:
	throw(-6)

try:
	vtt_file = open(vtt_filepath, 'w')
	vtt_file.write(vtt)
	vtt_file.close()
except:
	throw(-5)

print('Conversion successfully completed.')
exit(0)
