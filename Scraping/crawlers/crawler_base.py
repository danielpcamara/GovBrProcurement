print(f"## Starting {__name__} ##")
import sqlite3
import os
import asyncio
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import json

class CrawlerBase:
    def __init__(self, crawlerid, url, idcity, city):
        self._url = url
        self._id = crawlerid
        self._id_ibge = idcity
        self._cityhall = city
        #print('base inti was call')
    def __str__(self):
        return f"I'm the crawler of %s from the %s operating in the city ​​hall %s." % (self.name.upper(), self.company.upper(), self._cityhall.upper())

    def query_produrements(self, limit=99999999):
        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        cur.execute("SELECT ibge, procurement_id, year, procurement_type, procurement FROM PROCUREMENTS WHERE ibge=? LIMIT ?", (self._id_ibge, limit))

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
    
    def query_files_to_do(self, limit=99999999):
        con = sqlite3.connect("scraped.db", timeout=50)
        cur = con.cursor()
        cur.execute("SELECT ibge, procurement_id, file_id, path, new_name FROM FILES WHERE ibge=? and (OCR_RAW = '' or OCR_RAW is null)  LIMIT ?", (self._id_ibge, limit))

        rows = cur.fetchall()

        return rows

    def do_ocr(self, limit=99999999):
        
        with open('config.json') as config_file:
            paths = json.load(config_file)

        pytesseract.pytesseract.tesseract_cmd = paths['tesseract_path']

        def process_page(image_path):
            page_data = Image.open(image_path)
            return pytesseract.image_to_string(page_data, lang='por').encode("utf-8")

        async def get_text_async(pdf_path):
            loop = asyncio.get_event_loop()
            executor = ProcessPoolExecutor()

            async def process_pages(images):
                tasks = [loop.run_in_executor(executor, process_page, image_path) for image_path in images]
                return await asyncio.gather(*tasks)

            images = convert_from_path(pdf_path, poppler_path=paths['poppler_path'])
            
            # Save each image to a temporary file and get its path
            image_paths = []
            for i, image in enumerate(images):
                image_path = os.path.join(pdf_path,f'temp_image_{i}.png')
                image.save(image_path, 'PNG')
                image_paths.append(image_path)

            text_list = await process_pages(image_paths)

            # Remove temporary image files
            for image_path in image_paths:
                os.remove(image_path)

            return b'\n'.join(text_list).decode('utf-8')

        async def process_files(rows):
            tasks = [get_text_async(os.path.join(row[3], row[4])) for row in rows]
            return await asyncio.gather(*tasks)

        async def main():
            rows = self.query_files_to_do(limit)
            # ibge=row[0], procurement_id=row[1], file_id=row[2], path=row[3], new_name=row[4]

            results = await process_files(rows)

            to_update = []
            for row, result in zip(rows, results):
                to_update.append(result, row[0], row[1], row[2])

            update = "UPDATE FILES set OCR_RAW = ? where ibge = ? and procurement_id = ? and file_id = ?"
            con = sqlite3.connect("scraped.db", timeout=50)
            cursor = con.cursor()
            cursor.executemany(update, to_update)
            con.commit()
            con.close()

        asyncio.run(main())

        pass

if __name__ == '__main__':
    print('base main')