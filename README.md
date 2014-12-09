PySAMI
======

This Python 3 library allows you to parse and convert [SAMI files](http://msdn.microsoft.com/en-us/library/ms971327.aspx).
Currently (v0.1.5) only conversion to WebVTT is supported.

Installation
--------------------
```sh
# PyPI easy_install is not supported yet.

git clone https://github.com/g6123/pysami.git
cd pysami
sudo python3 setup.py install

# To use auto charset detection, you should install uchardet.
sudo apt-get update
sudo apt-get install uchardet
```

Classes
--------------------
There are two importable classes : SmiFile and ConversionError.

#### SmiFile
This class makes an object that reads, parses and converts SAMI files.

```python
from pysami import SmiFile

smi = SmiFile('examples/sample1.smi')
smi.parse()
vtt = smi.convert('vtt', 'KRCC')
```

```plain
# SmiFile(input_file, encoding=None)
 input_file : Path to the SAMI file. (*.smi)
   encoding : Encoding of the file.
              If set to None or false, auto detection is tried.

# <SmiFile>.parse(verbose=False)
    verbose : If set to True, all parsed subtitles are displayed.

# <SmiFile>.convert(output_type, lang='ENCC')
output_type : Result file type of the conversion.
              Supported types : vtt
       lang : Target language code of the conversion.
```

#### ConversionError
This is an error class used when error occurs during the conversion.

```python
from sys import stderr
from pysami import SmiFile, ConversionError

try:
	smi = SmiFile('examples/sample2.smi')
	smi.parse()
	vtt = smi.convert('vtt')
except ConversionError as error:
	print(error.msg, file=stderr)
	exit(error.code)
```

```plain
# ConversionError(code)
       code : Error code that the object would have.
              Ranging from -1 to -6, each makes a message defined in <ConversionError>.messages from 0 to 5.

# <ConversionError>.messages
        [0] : Cannot access to the input file.
        [1] : Cannot find correct encoding for the input file.
        [2] : Cannot parse the input file. It seems not to be a valid SAMI file.
              (Verbose option may show you the position the error occured in)
        [3] : Cannot convert into the specified type. (Suppored types : vtt)
        [4] : Cannot convert the input file before parsing it.
        [5] : Unknown error occurred.

# <ConversionError>.code
# <ConversionError>.msg

* <ConversionError>.code and <ConversionError>.msg will be automatically set.
```
