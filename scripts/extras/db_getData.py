import pymysql
import csv
import sys
import codecs
import os



sys.stdout = codecs.getwriter('utf8')(sys.stdout)


db_opts = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'dogodki20201112',
    'charset': 'utf8'
}

db = pymysql.connect(**db_opts)
cur = db.cursor()

sql_old = """SELECT FEVE_NAZ naziv, FEVE_OPI opis, FEVE_DOD datum_od, FEVE_STU stevilo, FEVE.FPRI_SIF sifra_prizorisca
FROM FABEVE FEVE
LEFT OUTER JOIN FABMES FMES
ON FMES.FMES_SIF = FEVE.FMES_SIF
LEFT OUTER JOIN FABPRI FPRI
ON FPRI.FPRI_SIF = FEVE.FPRI_SIF
LEFT OUTER JOIN FABGEO FGEO
ON FGEO.FGEO_SIF = (CASE WHEN FEVE.FEVE_GEO IS NOT NULL THEN FEVE.FEVE_GEO ELSE 
						CASE WHEN FPRI_GEO IS NOT NULL THEN FPRI_GEO ELSE 
							FMES_GEO 
						END END)
WHERE FEVE_DOD < '2020-06-04'
AND FGEO.FDRZ_SIF = 197
AND FEVE_STU > 100"""

sql = """
SELECT FEVE_NAZ naziv, FEVE_OPI opis, FEVE_DOD datum_od, FEVE_STU stevilo, FEVE.FPRI_SIF sifra_prizorisca,
   GROUP_CONCAT(FCOE.FCAT_SIF SEPARATOR ',') as kategorije_sifre, GROUP_CONCAT(FCAT_NAZ SEPARATOR ',') as kategorije_nazivi,
   VESELICA veselica
FROM FABEVE FEVE
LEFT OUTER JOIN FABMES FMES
ON FMES.FMES_SIF = FEVE.FMES_SIF
LEFT OUTER JOIN FABPRI FPRI
ON FPRI.FPRI_SIF = FEVE.FPRI_SIF
LEFT OUTER JOIN FABGEO FGEO
ON FGEO.FGEO_SIF = (CASE WHEN FEVE.FEVE_GEO IS NOT NULL THEN FEVE.FEVE_GEO ELSE 
						CASE WHEN FPRI_GEO IS NOT NULL THEN FPRI_GEO ELSE 
							FMES_GEO 
						END END)
JOIN FABCOE FCOE -- dodaj LEFT, če hočeš da ti vrne tudi brez kategorij
ON FCOE.FEVE_SIF = FEVE.FEVE_SIF
LEFT JOIN FABCAT FCAT
ON FCOE.FCAT_SIF = FCAT.FCAT_SIF
WHERE FEVE_DOD < '2020-06-04'
AND FGEO.FDRZ_SIF = 197 -- drzava slovenija
AND FEVE_STU > 50 -- st udelezencev
AND FEVE_SIFP IS NULL -- je parent
GROUP BY FEVE.FEVE_SIF -- grupiranje rabimo za kategorije"""




dirname = os.path.dirname(__file__)
csv_file_path = os.path.join(dirname, '../data/dogodki50.csv')

try:
    cur.execute(sql)
    rows = cur.fetchall()
finally:
    db.close()

# Continue only if there are rows returned.
if rows:
    # New empty list called 'result'. This will be written to a file.
    result = list()

    # The row name is the first entry for each entity in the description tuple.
    column_names = list()
    for i in cur.description:
        column_names.append(i[0])

    result.append(column_names)
    for row in rows:
        result.append(row)

    # Write result to file.
    with open(csv_file_path, 'w', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in result:
            csvwriter.writerow(row)
else:
    sys.exit("No rows found for query: {}".format(sql))




