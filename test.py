# from Scraping import *

# cw = crawlers.CrawlerMaster(1, 'cmpg.oxy.elotech.com.br', 4119905, 'Ponta Grossa/PR')
# cw.do_ocr(2)
import aiopytesseract
from PIL import Image
import asyncio

async def process_image(image_path):
    image = Image.open(image_path)
    result = await aiopytesseract.image_to_string(image, lang='por')
    return result.encode("utf-8")

async def process_images(image_paths):
    tasks = [process_image(image_path) for image_path in image_paths]
    return await asyncio.gather(*tasks)

async def main():
    image_paths = [r"Files\4119905\2-2020-7\IMG-20210201-WA0001.jpg", r"Files\4119905\2-2020-7\IMG-20210201-WA0001.jpg", r"Files\4119905\2-2020-7\IMG-20210201-WA0001.jpg"]
    results = await process_images(image_paths)
    i = 0
    for image_path, result in zip(image_paths, results):
        i += 1
        x = aiopytesseract.image_to_string(image_path)
        print(f'loop {i}, TX: {x}')

if __name__ == "__main__":
    asyncio.run(main())