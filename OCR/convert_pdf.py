import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import json

#V2:
import asyncio
import ironpdf
import aiopytesseract

with open('config.json') as config_file:
    paths = json.load(config_file)

pytesseract.pytesseract.tesseract_cmd = paths['tesseract_path']

def get_text(pdf_path):
    images = convert_from_path(pdf_path, poppler_path=paths['poppler_path'])
    
    text = ""
    for page_number, page_data in enumerate(images):
        txt = pytesseract.image_to_string(page_data,lang='por').encode("utf-8")
        text = "{}{}{}".format(text, chr(10), txt)
    return text

def get_text2(pdf_path):
    images = convert_from_path(pdf_path, poppler_path=paths['poppler_path'])
    
    text = ""
    for page_number, page_data in enumerate(images):
        txt = pytesseract.image_to_string(page_data,lang='por').encode("utf-8")
        text = "{}{}{}".format(text, chr(10), txt)
    return text

if __name__ == "__main__":
    print(get_text(r"Files\4119905\1-2020-9\18049.pdf"))

#############################
    
import os
import asyncio
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import json

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
        image_path = f'temp_image_{i}.png'
        image.save(image_path, 'PNG')
        image_paths.append(image_path)

    text_list = await process_pages(image_paths)

    # Remove temporary image files
    for image_path in image_paths:
        os.remove(image_path)

    return b'\n'.join(text_list).decode('utf-8')

async def process_files(pdf_paths):
    tasks = [get_text_async(pdf_path) for pdf_path in pdf_paths]
    return await asyncio.gather(*tasks)

async def main():
    pdf_paths = [
        r"Files\4119905\1-2020-9\18049.pdf",
        # Add more file paths as needed
    ]

    results = await process_files(pdf_paths)

    for pdf_path, result in zip(pdf_paths, results):
        print(f"Text extracted from {pdf_path}:\n{result}\n")

if __name__ == "__main__":
    asyncio.run(main())
