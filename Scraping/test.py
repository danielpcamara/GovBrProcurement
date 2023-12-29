import crawlers as c


cw = c.CrawlerMaster(1, 'cmpg.oxy.elotech.com.br', 4119905, 'Ponta Grossa/PR')
rows = cw.query_produrements(5)

for row in rows:
    print(row)