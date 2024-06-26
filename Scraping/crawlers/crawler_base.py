#print(f"## Starting {__name__} ##")
from abc import ABC, abstractmethod
import sqlite3
import os
import asyncio
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import json
import time
import math
import docx

class CrawlerBase(ABC):
    @abstractmethod
    def get_procurements(self):
        pass

    @abstractmethod
    def get_file_list(self):
        pass
    
    @abstractmethod
    def get_all_files(self):
        pass

    def __init__(self, crawlerid, url, idcity, city, uf):
        self._url = url
        self._id = crawlerid
        self._id_ibge = idcity
        self._cityhall = city
        self._uf = uf
        #print('base inti was call')

        if not(self.city_exists()):
            self.create_city()

    def __str__(self):
        return f"I'm the crawler of %s from the %s operating in the city ​​hall %s." % (self.name.upper(), self.company.upper(), self._cityhall.upper())

    def __eq__(self, other):
        try:
            x = self._id_ibge == other
        except:
             x = self._id_ibge == other._id_ibge
        return x

    def create_city(self):
        insert = f"INSERT INTO CITYS (ibge,uf,city_name,url_base,solution_id) VALUES( {self._id_ibge}, '{self._uf}' , '{self._cityhall}', '{self._url}', {self._id} );"
        con = sqlite3.connect("scraped.db", timeout=50)
        cursor = con.cursor()
        cursor.execute(insert)
        con.commit()
        con.close()

    def city_exists(self):
        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        cur.execute(f"SELECT COUNT(*) FROM CITYS WHERE ibge=?", ([self._id_ibge]))

        exists = cur.fetchall()[0][0] > 0
        return exists

    def query_produrements(self, limit=99999999):
        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        cur.execute("SELECT ibge, procurement_id, year, procurement_type, procurement FROM PROCUREMENTS WHERE ibge=? LIMIT ?", (self._id_ibge, limit))

        rows = cur.fetchall()

        return rows

    def query_produrements_empty_field(self, field_name, limit=99999999):
        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        cur.execute(f"SELECT ibge, procurement_id, year, procurement_type, procurement, goal FROM PROCUREMENTS WHERE ibge=? and {field_name} is null LIMIT ?", (self._id_ibge, limit))

        rows = cur.fetchall()

        return rows
    

    def query_produrements_goal(self, limit=99999999, fields='', filter=''):
        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        if filter != '':
            filter = ' and ' + filter
        if fields != '':
            fields = ', ' + fields
        select = f"SELECT ibge, procurement_id, year, procurement_type, procurement, goal {fields} FROM PROCUREMENTS WHERE ibge=? {filter} LIMIT ?"
        cur.execute(select, (self._id_ibge, limit))

        rows = cur.fetchall()

        return rows

    def query_folders(self, limit=99999999):
        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        cur.execute("SELECT Distinct path FROM FILES WHERE ibge=? LIMIT ?", (self._id_ibge, limit))

        rows = cur.fetchall()

        return rows

    def query_files(self, limit=99999999):
        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        cur.execute("SELECT ibge, procurement_id, file_id, path, new_name FROM FILES WHERE ibge=? LIMIT ?", (self._id_ibge, limit))

        rows = cur.fetchall()

        return rows

    def query_files_to_do(self, filetype, limit=99999999):
        if filetype.upper() == "PDF":
            filter = "and UPPER(substr(new_name, -3)) = 'PDF'"
        elif filetype.upper() == "DOC":
            filter = "and (UPPER(substr(new_name, -3)) = 'DOC' or UPPER(substr(new_name, -4)) = 'DOCX')"
        elif filetype.upper() == "IMG":
            filter = "and (UPPER(substr(new_name, -3)) = 'PNG' or UPPER(substr(new_name, -3)) = 'JPG')"
        elif filetype.upper() == "ALL":
            filter = ""
        else:
            filter = f"and UPPER(substr(new_name, -3)) = '{filetype.upper()}'"

        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        cur.execute(f"SELECT ibge, procurement_id, file_id, path, new_name FROM FILES WHERE ibge=? and (OCR_RAW = '' or OCR_RAW is null) {filter}  LIMIT ?", (self._id_ibge, limit))

        rows = cur.fetchall()

        return rows

    def query_qtd_files_to_do(self, filetype, limit=99999999):
        if filetype.upper() == "PDF":
            filter = "and UPPER(substr(new_name, -3)) = 'PDF'"
        elif filetype.upper() == "DOC":
            filter = "and (UPPER(substr(new_name, -3)) = 'DOC' or UPPER(substr(new_name, -4)) = 'DOCX')"
        elif filetype.upper() == "ALL":
            filter = ""
        else:
            filter = f"and UPPER(substr(new_name, -3)) = '{filetype.upper()}'"
            
        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        cur.execute(f"SELECT COUNT(*) FROM FILES WHERE ibge=? and (OCR_RAW = '' or OCR_RAW is null) {filter} LIMIT ?", (self._id_ibge, limit))

        rows = cur.fetchall()

        return rows

    def update_procurements_filed(self, field, list_id, list_new_value):

        update = f"UPDATE PROCUREMENTS set {field} = ? where ibge = ? and procurement_id = ?"
        con = sqlite3.connect("scraped.db")
        cursor = con.cursor()
        to_update = []
        for id, new_value in zip(list_id, list_new_value):
            to_update.append((new_value, self._id_ibge, id))
        cursor.executemany(update, to_update)
        con.commit()
        con.close()
        pass

    def manual_update_file(self, id, fileid, text):
        update = "UPDATE FILES set OCR_RAW = ? where ibge = ? and procurement_id = ? and file_id = ?"
        con = sqlite3.connect("scraped.db")
        cursor = con.cursor()
        cursor.executemany(update, [(text, self._id_ibge, id, fileid)])
        con.commit()
        con.close()
        pass
    
    def mark_empty_files(self):
        rows = self.query_files_to_do()
        # ibge=row[0], procurement_id=row[1], file_id=row[2], path=row[3], new_name=row[4]
        
        to_update = []
        for row in rows:
            p = os.path.join(row[3], row[4])
            if os.stat(p).st_size == 0:
                to_update.append(('<blank file>', row[0], row[1], row[2]))

        update = "UPDATE FILES set OCR_RAW = ? where ibge = ? and procurement_id = ? and file_id = ?"
        con = sqlite3.connect("scraped.db", timeout=50)
        cursor = con.cursor()
        cursor.executemany(update, to_update)
        con.commit()
        con.close()

        pass

    def do_ocr_pdf(self, limit=99999999):
        
        with open('config.json') as config_file:
            paths = json.load(config_file)

        pytesseract.pytesseract.tesseract_cmd = paths['tesseract_path']

        def process_page(image_path):
            page_data = Image.open(image_path)
            return pytesseract.image_to_string(page_data, lang='por').encode("utf-8")

        async def get_text_async(pdf_path):
            loop = asyncio.get_event_loop()

            def process_pages(images):
                return [process_page(image_path) for image_path in images]

            images = convert_from_path(pdf_path, poppler_path=paths['poppler_path'])
            
            # Save each image to a temporary file and get its path
            image_paths = []
            for i, image in enumerate(images):
                image_path = pdf_path + f'temp_image_{i}.png'
                image.save(image_path, 'PNG')
                image_paths.append(image_path)

            text_list = await loop.run_in_executor(None, process_pages, image_paths)

            # Remove temporary image files
            for image_path in image_paths:
                os.remove(image_path)

            return b'\n'.join(text_list).decode('utf-8')

        async def process_files(paths):
            tasks = [get_text_async(path) for path in paths]
            return await asyncio.gather(*tasks)

        async def main():
            rows = self.query_files_to_do("pdf", limit)
            # ibge=row[0], procurement_id=row[1], file_id=row[2], path=row[3], new_name=row[4]
            
            paths = [os.path.join(row[3], row[4]) for row in rows]
            to_update = []
            
            results = await process_files(paths)

            for row, result in zip(rows, results):
                to_update.append((result, row[0], row[1], row[2]))

            update = "UPDATE FILES set OCR_RAW = ? where ibge = ? and procurement_id = ? and file_id = ?"
            con = sqlite3.connect("scraped.db", timeout=50)
            cursor = con.cursor()
            cursor.executemany(update, to_update)
            con.commit()
            con.close()

        asyncio.run(main())

        pass
    
    def get_files_text_doc(self, limit=99999999):
        rows = self.query_files_to_do("doc", limit)

        def getText(filename):
            doc = docx.Document(filename)
            return '\n'.join([p.text for p in doc.paragraphs])
        
        results = [getText(os.path.join(row[3], row[4])) for row in rows]

        to_update = []
        for row, result in zip(rows, results):
            to_update.append((result, row[0], row[1], row[2]))

        update = "UPDATE FILES set OCR_RAW = ? where ibge = ? and procurement_id = ? and file_id = ?"
        con = sqlite3.connect("scraped.db", timeout=50)
        cursor = con.cursor()
        cursor.executemany(update, to_update)
        con.commit()
        con.close()
        pass

    def extract_text_all_files(self):

        #PDF
        packeges_size = 20
        total = self.query_qtd_files_to_do("pdf")[0][0]
        loops = math.ceil(total / packeges_size )
        print(f"PDF Blocks: {loops}, Size: {packeges_size}, Total: {total}")

        for l in range(loops):
            start_time = time.time()
            self.do_ocr_pdf(packeges_size)
            t = str(((time.time() - start_time)/60))
            print(f"--- The PDF block {str(l + 1)}, Doing {str(packeges_size)} files, took: {t} minutes ---")
        
        #DOC
        total = self.query_qtd_files_to_do("doc")[0][0]
        print(f"DOC Block: 1, Size: {total}, Total: {total}")
        start_time = time.time()
        self.get_files_text_doc()
        t = str(((time.time() - start_time)/60))
        print(f"--- The DOC block 1, Doing {str(total)} files, took: {t} minutes ---")

        #IMG

if __name__ == '__main__':
    print('base main')