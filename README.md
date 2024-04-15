# ELT and LLM in Public Procurement Audit

## Goal 🎯
 This repository will extract data from Brazilian municipal hall transparency Portals, to be use in government procurement audit.

 It uses Google Gemini to table data from a text field call "_objeto_" (object), this field contains the product or service to which the public procurement refers and can also have the "_secretaria_" (departament) who made the request.

 The ```main.py``` file uses the ```data.py```, ```crawler_base.py```, ```crawler_master.py``` and ```crawler_oxy.py``` to show how to implement the code and extract data from the city ​​halls.

 This project was born in a Final paper for my MBA in DSA (Data Science and Analytics), and for this reason, it contains notes and analyzes that are not part of the public data extraction project. If you plan to clone the repo, it is recommended that you ignore completely the notebook ```test_evaluation.ipynb``` and ignore the analysis part in the ```test.gemini.ipynb``` notebook.

 ## More about notebooks 📝

 The notebook ```text_scraping.ipynb``` was used to make test in the making of the cralwrs.py files.

 The ```test_gemini.ipynb``` file, was created to document trials and extractions obtained using Google BERT and Gemini 1.0 LLMs. It also records how the data obtained in the extraction phases by LLM and evaluation carried out by researchers were stored in the database created in the ETL stage.

 And the ```test_evaluation.ipynb``` notebook records the exploratory analyzes carried out in the created database.

## Deploying the code 👨‍💻

To implement the ETL code you'll need:

1. Create venv, using Power shell.
    ```
    python -m venv  '\venv'
    ```

2. Start venv from power Shell, or...
    ```
    .\venv\Scripts\activate
    ```

    ... start from VS Code, by selecting the interpreter, or...
    ```
    Ctrl+Shift+P
    Python: Create Environment 
    ```
    ... set venv as Interpreter

3. Instalation some apps in windows. Yes, Windows, not Linux 😋.
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
    pip install ironpdf 
    pip install aiopytesseract
    pip install python-docx 
    
    # BERT
    pip install transformers torch
    
    # GEMINI
    pip install -q -U google-generativeai
    
    # Evaluation
    pip install openpyxl
    pip install pandas
    pip install -U scikit-learn
    pip install seaborn
    pip install nltk
    ```

5. Create a ```config.json``` file similar to ```config_example.json```.