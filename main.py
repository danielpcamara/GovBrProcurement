from Scraping import *

cw = crawlers.CrawlerMaster(1, 'cmpg.oxy.elotech.com.br', 4119905, 'Ponta Grossa/PR')

# Obtain Procurements (and save in the databae)
cw.get_procurements()

#Get a list of all files for each Procurement (and save in the databae)
cw.get_file_list()

#download all files and save in the "Files" folder
cw.get_all_files()

# Annotate in the database all files that are empty (0 size)
cw.mark_empty_files()

# Extract the text using OCR (and save in the database)
cw.extract_text_all_files()

# ingore Files that won't ne used
cw.manual_update_file("2/2020/7", 22483, "<Ignore>")