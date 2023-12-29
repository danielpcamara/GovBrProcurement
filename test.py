# from Scraping import *

# cw = crawlers.CrawlerMaster(1, 'cmpg.oxy.elotech.com.br', 4119905, 'Ponta Grossa/PR')
# rows = cw.query_produrements(5)

# for row in rows:
#     print(row)

import pytesseract
from pytesseract import Output
from PIL import Image
import cv2

img_path = 'test.png'
text = pytesseract.image_to_string(img_path,lang='por')
print(text)

pip show pytesseract 