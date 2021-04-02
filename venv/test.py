import sqlite3
import csv
conn = sqlite3.connect('disease_details.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS disease_details')
conn.commit()
c.execute("""CREATE TABLE disease_info(
   Disease_Name         VARCHAR(65) NOT NULL PRIMARY KEY
  ,Overview             VARCHAR(9836) NOT NULL
  ,Symptoms             VARCHAR(10832) NOT NULL
  ,When_to_see_a_doctor VARCHAR(7287) NOT NULL
  ,Causes               VARCHAR(11456)
  ,Risk_Factors         VARCHAR(12056)
  ,Complications        VARCHAR(10124)
); """)

fname='details1.csv'
with open(fname) as csv_file:
    csvr=csv.reader(csv_file,delimiter=',')
    for row in csvr:
        if not row :
            continue
        print(row)
        c.execute('INSERT INTO disease_info(Disease_Name,Overview,Symptoms,When_to_see_a_doctor,Causes,Risk_Factors,Complications) VALUES (?,?,?,?,?,?,?)',(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
        conn.commit()