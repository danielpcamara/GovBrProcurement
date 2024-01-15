# Machine Learning on Government Procurement Audit
## Requierments
.\Scripts\activate
* Install Python
* Install venv on python

## Deploy

Using Power shell, Create vev
```
python -m venv  '\venv'
```

Start venv from power Shell or...
```
.\venv\Scripts\activate
```

...Start from VS Code, by selecting the interpreter:
```
Ctrl+Shift+P
Python: Create Environment 
```

Instalation requierments
```
#test
pip install jupyter
#Scraping
pip install aiohttp
pip install asyncio
pip install aiofile
#OCR and text extraction
Install tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki ("Additional language data (download) > portuguese" and "Additional script data (download) > Latin script" is requierd)
Then add to PATH
pip install opencv-python
pip install pytesseract
pip install pdf2image
pip install python-dateutil
Install tesserocr from https://github.com/sirfz/tesserocr/blob/master/Windows.build.md
#v2:
pip install ironpdf 
pip install aiopytesseract
install https://cmake.org/download
.NET SDK
pip install python-docx 
#BERT
✔ pip install transformers torch
```
Install Poppler from https://github.com/oschwartz10612/poppler-windows/releases/ OR if you have chocolatey: choco install poppler
set Poppler as system variable


## Goal
 This repository will extract data from Brazilian municipal hall transparency Portals, and use the data to make a government procurement audit.
