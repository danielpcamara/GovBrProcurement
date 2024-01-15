from Scraping import *

db = data.Database()

# Create the database
db.create_tabeles()

# Feed table for existing crawlers (systems)
db.feed_main_tabeles()

# Create city in the databse
cw_ponta_grossa = crawlers.CrawlerMaster(1, 'cmpg.oxy.elotech.com.br', 4119905, 'Ponta Grossa', 'PR')

# Obtain Procurements (and save in the databae)
cw_ponta_grossa.get_procurements()

#Get a list of all files for each Procurement (and save in the databae)
cw_ponta_grossa.get_file_list()

#download all files and save in the "Files" folder
cw_ponta_grossa.get_all_files()

# Annotate in the database all files that are empty (0 size)
cw_ponta_grossa.mark_empty_files()

# Extract the text using OCR (and save in the database)
cw_ponta_grossa.extract_text_all_files()

# example of ingore Files that won't ne used
cw_ponta_grossa.manual_update_file("2/2020/7", 22483, "<Ignore>")