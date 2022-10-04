import sqlite3
connecteur = sqlite3.connect("../database.db")

cursor = connecteur.cursor()

dtable1 = cursor.execute("DROP TABLE IF EXISTS utilisateurs")
table1 = cursor.execute("CREATE TABLE utilisateurs(identifiant varchar, motdepasse varchar not null,id int, PRIMARY KEY(identifiant,id))")


dtable2 = cursor.execute("DROP TABLE IF EXISTS historique")
table2 = cursor.execute("CREATE TABLE historique(id int PRIMARY KEY, pseudo varchar ,mot varchar, dateheure "
                        "smalldatetime not null , partie varchar, analysepartie varchar,essaies int,etat varchar,idu int,chrono int,FOREIGN KEY(idu) REFERENCES utilisateurs(id))")

dtable3 = cursor.execute("DROP TABLE IF EXISTS statistiques")
table3 = cursor.execute("CREATE TABLE statistiques(id int PRIMARY KEY,wins int,looses int,tmoy int,tmin int,"
                        "trymoy int,best int,niceperf int,streak int,maxstreak int,ranking int,scoreend int, FOREIGN KEY(id) REFERENCES utilisateurs(id))")

dtable4 = cursor.execute("DROP TABLE IF EXISTS motpatterns")
table4 = cursor.execute("CREATE TABLE motpatterns(mot varchar,pattern int,motpattern varchar,nbl int,PRIMARY KEY(mot,pattern,motpattern")

connecteur.commit()
connecteur.close()
