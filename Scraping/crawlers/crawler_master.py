if __name__ == '__main__':
    from crawler_oxy import CrawlerOxy
    from crawler_base import CrawlerBase
else:
    from .crawler_oxy import CrawlerOxy
    from .crawler_base import CrawlerBase


class CrawlerMaster(CrawlerBase):
    def __init__(self, crawlerid, url, idcity, city):
        #print('master inti was call')
        vars(self).clear()
        if crawlerid == 1:
            new_crawler = CrawlerOxy(crawlerid, url, idcity, city)
            vars(self).update(vars(new_crawler))
            self.__class__ = new_crawler.__class__
        elif crawlerid == 2:
            vars(self).update(vars(CrawlerOxy))
            self.__class__ = CrawlerOxy
            super().__init__(crawlerid, url, idcity, city)