from Scraping import *

db = data.Database()

# Create the database
db.create_tabeles()

# Feed table for existing crawlers (systems)
db.feed_main_tabeles()

# Create city in the databse
city_list = []
city_list.append(crawlers.CrawlerMaster(1, 'cmpg.oxy.elotech.com.br', 4119905, 'Ponta Grossa', 'PR'))
city_list.append(crawlers.CrawlerMaster(1, 'venus.maringa.pr.gov.br:8090', 4115200, 'Maringá', 'PR'))
city_list.append(crawlers.CrawlerMaster(1, 'servicos.umuarama.pr.gov.br', 4128104, 'Umuarama', 'PR'))
city_list.append(crawlers.CrawlerMaster(1, 'teresopolis.eloweb.net', 3305802, 'Teresópolis', 'RJ'))
city_list.append(crawlers.CrawlerMaster(1, 'engenheirobeltrao.oxy.elotech.com.br', 4107504, 'Engenheiro Beltrão', 'PR'))


for city in city_list:
    # Obtain Procurements (and save in the databae)
    city.get_procurements()

    #Get a list of all files for each Procurement (and save in the databae)
    city.get_file_list()

    #download all files and save in the "Files" folder
    city.get_all_files()

    # Annotate in the database all files that are empty (0 size)
    city.mark_empty_files()

    # Extract the text using OCR (and save in the database)
    city.extract_text_all_files()

    # example of ingore Files that won't ne used
    #city.manual_update_file("2/2020/7", 22483, "<Ignore>")