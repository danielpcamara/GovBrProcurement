# Machine Learning on Government Procurement Audit
## Goal
 This repository will extract data from Brazilian municipal hall transparency Portals, and use the data to make a government procurement audit.

## Deploy

1. Using Power shell, Create venv
    ```
    python -m venv  '\venv'
    ```

2. Start venv from power Shell, or...
    ```
    .\venv\Scripts\activate
    ```

    ...Start from VS Code, by selecting the interpreter, or...
    ```
    Ctrl+Shift+P
    Python: Create Environment 
    ```
    ...Set venv as Interpreter

3. Windows Instalation requierments
    * OCR and text extraction
        * Install tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki ("Additional language data (download) > portuguese" and "Additional script data (download) > Latin script" is requierd)
            
            Then add to PATH
        * Install tesserocr from https://github.com/sirfz/tesserocr/blob/master/Windows.build.md
        * Install https://cmake.org/download
        * Install .NET SDK
        * Install Poppler from https://github.com/oschwartz10612/poppler-windows/releases/, or...
            
            If you have chocolatey: ```choco install poppler```
            
            Then Set Poppler as system variable
4. Python Instalation requierments
    ```
    #test
    pip install jupyter
    #Scraping
    pip install aiohttp
    pip install asyncio
    pip install aiofile
    pip install opencv-python
    pip install pytesseract
    pip install pdf2image
    pip install python-dateutil
    #v2:
    pip install ironpdf 
    pip install aiopytesseract
    pip install python-docx 
    #BERT
    pip install transformers torch
    #GEMINI
    pip install -q -U google-generativeai
    #Evaluation
    pip install openpyxl
    pip install pandas
    ```

5. Create a ```config.json``` file similar to ```config_example.json```
6. Copy 'bert-base-portuguese-cased' from https://huggingface.co/neuralmind/bert-base-portuguese-cased and save in the projects folder