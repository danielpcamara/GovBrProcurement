print(f"## Starting {__name__} ##")
import asyncio
import aiohttp
import requests
import sqlite3
import json
import os
import aiofile
import nest_asyncio

if __name__ == '__main__':
    from crawler_base import CrawlerBase
else:
    from .crawler_base import CrawlerBase

        
class CrawlerOxy(CrawlerBase):
    name = "Oxy"
    company = "Elotech"
    def __int__(self, crawlerid, url, idcity, city, uf):
        #print('oxy inti was call')
        super().__init__(crawlerid, url, idcity, city, uf)
    
    def get_procurements(self):
        fullurl = 'https://{0}/portaltransparencia-api/api/licitacoes?page={1}&size=100'.format(self._url, '0')
        datas = [requests.get(fullurl).json()]
        loop = datas[0].get("totalPages")
        if loop > 0:
            for num in range(1, loop):
                fullurl = 'https://{0}/portaltransparencia-api/api/licitacoes?page={1}&size=100'.format(self._url, str(num))
                datas.append(requests.get(fullurl).json())

        to_insert = []
        i = 0
        for data in datas:
            i += 1
            print(str(i) + ' ' + str(data.get('number')))
            for procurement in data.get('content'):
                to_insert.append((self._id_ibge, procurement['displayLicitacao'] + '/' + str(procurement['tipoLicitacao']), procurement['exercicio'], procurement['tipoLicitacao'], procurement['licitacao'], procurement['descricao'], procurement['numeroLicitacao'], procurement['dataPublicacao'], procurement['dataAbertura'] + ' ' + procurement['horarioAbertura'], procurement['tipoCancelamento'], procurement['natureza'], procurement['objeto'], procurement['protocolo'], procurement['anoProtocolo'], procurement['displayProtocolo'], procurement['valorMaximo'], procurement['totalVencido'], procurement['hasRecurso'] == 'S', procurement['observacao'], procurement['isCovid'] == 'S', procurement['formaApuracao'], procurement['tipoParticipacao'], procurement['aplicaLei14133'] == 'S', procurement['displayProcessoAdm'], procurement['processoAdmId'], procurement['mostraLeiEdital'], procurement['mostraLeiAta'], procurement['mostraLeiContrato']))

        insert = "INSERT OR IGNORE INTO PROCUREMENTS (ibge, procurement_id, year, procurement_type, procurement, Description, procurement_num, published_date, opening_date, cancellation_type, kind, goal, protocol_num, protocol_year, protocol_id, max_value, amount_due, has_recourse,  obs, is_covid, calculation_form, participation_type, Law14133, Adm_Process, Adm_Process_id, show_notice_law, show_notice_minutes, show_notice_contract ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        con = sqlite3.connect("scraped.db", timeout=50)
        cursor = con.cursor()
        cursor.executemany(insert, to_insert)
        con.commit()
        con.close()

        pass

    def get_file_list(self):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/licitacoes/arquivos?entidade=1&exercicio=2023&tipoLicitacao=6&licitacao=9

        rows = self.query_produrements()

        urls = []
        for row in rows:
            url = 'https://{base}/portaltransparencia-api/api/licitacoes/arquivos?entidade=1&exercicio={year}&tipoLicitacao={type}&licitacao={num}'.format(
                base=self._url,
                year=row[2],
                type=row[3],
                num=row[4]
            )
            urls.append(url)

        responses = []
        async def fetch(client, url):
            async with client.get(url) as resp:
                assert resp.status == 200
                html = await resp.json()
                responses.append(html)


        async def main():
            async with aiohttp.ClientSession() as client:
                await asyncio.gather(*[
                    asyncio.ensure_future(fetch(client, url))
                    for url in urls
                ])


        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

        to_insert = []
        for response in responses:
            for item in response:
                id = item['licitacao'].__str__() + '/' + item['exercicio'].__str__() + '/' + item['tipoLicitacao'].__str__()
                new_name = item['arquivoCompras']['idArquivo'].__str__() + "." + item['arquivoCompras']['nomeArquivo'].split(".")[-1]
                to_insert.append((self._id_ibge, id, item['arquivoCompras']['idArquivo'], os.path.join("", "Files", self._id_ibge.__str__(), id.replace("/", "-")), item['arquivoCompras']['nomeArquivo'], item['arquivoCompras']['data'], new_name))

        insert = "INSERT OR IGNORE INTO FILES (ibge, procurement_id, file_id, path, OCR_RAW, name, date, new_name) VALUES (?, ?, ?, ?, '', ?, ?, ?)"
        con = sqlite3.connect("scraped.db", timeout=50)
        cursor = con.cursor()
        cursor.executemany(insert, to_insert)
        con.commit()
        con.close()

        pass
    

    def get_all_files(self):

        # Validate Folders
        pastas = self.query_folders()
        for pasta in pastas:
            if not os.path.exists(pasta[0]):
                os.makedirs(pasta[0])
        
        #List all Files
        files = self.query_files()
        files2 = [('https://{base}/portaltransparencia-api/api/files/arquivo/{file_id}'.format(
                        base=self._url,
                        file_id=x[2]
                    ), ) + x for x in files]
        print('there is {0} files in the database'.format(files2.__len__()))
        #Check if file exists
        files3 = [x for x in files2 if not os.path.isfile(os.path.join(x[4], x[5]))]
        print('there is {0} files to be downloaded'.format(files3.__len__()))
        print('the first file id is: {0}.'.format(files3[0][3]))

        #Download and save files

        nest_asyncio.apply()
        def download_files_from_report(files):

            sema = asyncio.BoundedSemaphore(5)

            async def fetch_file(session, file):
                
                url = file[0]
                folder = file[4]
                fname = file[5]

                async with sema:
                    async with session.get(url) as resp: #session.get(url,timeout=120)
                        assert resp.status == 200
                        data = await resp.read()

                async with aiofile.async_open(
                    os.path.join(folder, fname), "wb"
                ) as outfile:
                    await outfile.write(data)

            async def main():
                async with aiohttp.ClientSession() as session:
                    tasks = [fetch_file(session, file) for file in files]
                    await asyncio.gather(*tasks)

            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
            #loop.close()

        download_files_from_report(files3)

        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/files/arquivo/1003026
        pass

    def get_certidoes(self):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/licitacoes/certidoes?entidade=1&exercicio=2023&tipoLicitacao=6&licitacao=9
        pass
    
    def get_homologacoes(self):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/homologacoes?entidade=1&exercicio=2023&tipoLicitacao=6&licitacao=9
        pass

    def get_cotacoes(self):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/licitacoes/cotacoes?entidade=1&exercicio=2023&tipoLicitacao=6&licitacao=9
        pass

    def get_pareceres(self):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/licitacoes/pareceres?entidade=1&exercicio=2023&tipoLicitacao=6&licitacao=9
        pass

    def get_atas(slef):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/licitacoes/atas?entidade=1&exercicio=2023&tipoLicitacao=6&licitacao=9
        pass

    def get_precos(self):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/licitacoes/precos?entidade=1&exercicio=2023&tipoLicitacao=6&licitacao=9
        pass

    def get_adjucoes(self):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/adjudicacoes?entidade=1&exercicio=2023&tipoLicitacao=6&licitacao=9
        pass

    def get_licitacoes(self):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/contratos/licitacao?entidade=1&exercicioLicitacao=2023&tipoLicitacao=6&numeroLicitacao=9
        pass

    def get_recursos(self):
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/licitacoes/recursos?entidade=1&exercicio=2023&tipoLicitacao=6&licitacao=9
        pass

    def get_sei(self): #?
        # https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/licitacoes/sei?processoAdmId=93cf4b8c-7165-4abb-a909-38d47861f135
        pass


if __name__ == '__main__': 

    o = CrawlerOxy(1, "cmpg.oxy.elotech.com.br", 4119905, "Ponta Grossa (PR)")

    print(f'name: %s' % o.name)
    print(f'company: %s' % o.company)
    print(f'url: %s' % o.get_url())
    print(f'city: %s' % o._cityhall)
    print(f'id: %s' % o._id)
    print(o)