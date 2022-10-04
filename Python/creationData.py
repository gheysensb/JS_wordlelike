import sqlite3
import random as rd

conn = sqlite3.connect("../database.db")
cursor = conn.cursor()
def ajoutdata(n):
    for i in range(100,100+n):
        win=rd.randint(0,1000)#
        los=rd.randint(0,1000)#
        tmoy=rd.randint(30,600)#
        tmin=rd.randint(10,300)
        trymoy=rd.randint(1,6)#
        bestperf=rd.randint(1,3)
        niceperf=rd.randint(0,50)#
        streak=rd.randint(0,25)
        streakmax=rd.randint(0,27)
        ranking=rd.randint(0,900)
        scoreend=rd.randint(0,13)
        cursor.execute("INSERT INTO statistiques VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(i,win,los,tmoy,tmin,trymoy,bestperf,niceperf,streak,streakmax,ranking,scoreend))
        conn.commit()

ajoutdata(100)