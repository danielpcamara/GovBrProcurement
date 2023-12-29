import sqlite3


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


class Licitacao:
    def __init__ (self, idcity, numeroLicitacao, dt_publicacao, dt_abertura):
        self.municipio = idcity
        self.numeroLicitacao = numeroLicitacao
        self.dt_publicacao = dt_publicacao
        self.dt_abertura = dt_abertura

if __name__ == '__main__':
    print('base main')