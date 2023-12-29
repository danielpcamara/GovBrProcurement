import sqlite3

def create_tabeles():
    con = sqlite3.connect("scraped.db")
    cursor = con.cursor()
    
    # Creating table
    table = """ CREATE TABLE SYSTEMS (
                solution_id integer primary key,
                solution_name VARCHAR(10) NOT NULL,
                company_name VARCHAR(10) NOT NULL,
                company_url VARCHAR(10) NOT NULL,
                crawler_name VARCHAR(10) NOT NULL,
                sample_url VARCHAR(10)
            );"""
    
    try:
        cursor.execute(table)
    except Exception:
        pass

    table = """ CREATE TABLE CITYS (
                ibge integer primary key,
                uf VARCHAR(2) NOT NULL,
                city_name VARCHAR(10) NOT NULL,
                url_base VARCHAR(10) NOT NULL,
                solution_id integer NOT NULL,
                    FOREIGN KEY(solution_id) REFERENCES SYSTEMS(solution_id)
            );"""

    try:
        cursor.execute(table)
    except Exception:
        pass
    
    table = """ CREATE TABLE PROCUREMENTS (
                ibge integer,
                procurement_id TEXT,

                year int,
                procurement_type int,
                procurement int,
                Description VARCHAR(10),
                procurement_num int,
                published_date datetime,
                opening_date datetime,
                cancellation_type VARCHAR(10),
                kind VARCHAR(10),
                goal TEXT,
                protocol_num int,
                protocol_year int,
                protocol_id VARCHAR(10),
                max_value num,
                amount_due num,
                has_recourse BOOLEAN,
                obs TEXT,
                is_covid BOOLEAN,
                calculation_form VARCHAR(10),
                participation_type VARCHAR(10),
                Law14133 BOOLEAN,
                Adm_Process VARCHAR(10),
                Adm_Process_id VARCHAR(10),
                show_notice_law BOOLEAN,
                show_notice_minutes BOOLEAN,
                show_notice_contract BOOLEAN,
                extra1 VARCHAR(10),
                extra2 VARCHAR(10),
                extra3 VARCHAR(10),
                extra4 VARCHAR(10),
                extra5 VARCHAR(10),
                extra6 VARCHAR(10),
                extra7 VARCHAR(10),
                extra8 VARCHAR(10),
                extra9 VARCHAR(10),

                FOREIGN KEY(ibge) REFERENCES CITYS(ibge),
                PRIMARY KEY (ibge, procurement_id)
            );"""

    try:
        cursor.execute(table)
    except Exception:
        pass
    
    table = """ CREATE TABLE FILES (
                ibge integer,
                procurement_id TEXT,
                file_id integer,

                path TEXT,
                OCR_RAW TEXT,
                name VARCHAR(10),
                new_name VARCHAR(10),
                date datetime,

                FOREIGN KEY(ibge, procurement_id) REFERENCES PROCUREMENTS(ibge, procurement_id),
                PRIMARY KEY (ibge, procurement_id, file_id)
            );"""

    try:
        cursor.execute(table)
    except Exception:
        pass

    con.close()
    pass

def feed_main_tabeles():
    con = sqlite3.connect("scraped.db")
    cursor = con.cursor()
    
    # Creating table
    data = """ INSERT INTO SYSTEMS (solution_id,solution_name,company_name,company_url,crawler_name,sample_url)
            VALUES(
                1,	'Oxy' , 'Elotech', 'https://www.elotech.com.br/', 'crawler_oxy.py',
                'https://cmpg.oxy.elotech.com.br/portaltransparencia-api/api/licitacoes?entidade=1&page=0&size=100'
            );"""
    cursor.execute(data)
    con.commit()

    data = """ INSERT INTO CITYS (ibge,uf,city_name,url_base,solution_id)
            VALUES(
                4119905, 'PR' , 'Ponta Grossa', 'cmpg.oxy.elotech.com.br', 1
            );"""

    cursor.execute(data)
    con.commit()
    
    con.close()
    pass

def kill_table(tb):
    con = sqlite3.connect("scraped.db")
    cursor = con.cursor()
    command = f"DROP TABLE IF EXISTS {tb};"
    cursor.execute(command)
    con.close()

def runcmd(command):
    con = sqlite3.connect("scraped.db")
    cursor = con.cursor()
    x = cursor.execute(command)
    con.commit()
    con.close()
    print ('Linhas afetadas: {0}'.format(x.rowcount))
    print ('Descrição: {0}'.format(x.description))
    print ('Comando executados: {0}'.format(x.arraysize))
if __name__ == '__main__':
    #kill_table("FILESS")
    create_tabeles()
    #runcmd("INSERT INTO FILES (ibge, procurement_id, file_id, OCR_RAW, name, date) Select ibge, procurement_id, file_id, OCR_RAW, name, date from FILESS")
    #runcmd("UPDATE FILES set path = REPLACE(path, 'Data', 'Files')")
    #feed_main_tabeles()