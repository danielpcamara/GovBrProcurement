#print(f"## Starting {__name__} ##")
if __name__ == '__main__':
    from crawler_oxy import CrawlerOxy
    from crawler_base import CrawlerBase
else:
    from .crawler_oxy import CrawlerOxy
    from .crawler_base import CrawlerBase


class CrawlerMaster(CrawlerBase):

    def __init__(self, crawlerid, url, idcity, city, uf):
        vars(self).clear()
        if crawlerid == 1:
            new_crawler = CrawlerOxy(crawlerid, url, idcity, city, uf)
            vars(self).update(vars(new_crawler))
            self.__class__ = new_crawler.__class__
        else:
            raise Exception('System not suported yet.')
    
    def get_procurements(self):
        pass

    def get_file_list(self):
        pass
    
    def get_all_files(self):
        pass