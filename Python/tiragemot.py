import sqlite3

def tiragemot(nblettres):
    connecteur = sqlite3.connect("database.db")
    cursor = connecteur.cursor()
    mot=(cursor.execute("SELECT mot from dico where length(mot) = (?) order by random() limit 1",(nblettres,))).fetchall()
    connecteur.close()
    return mot[0][0]

def dico(nblettres):
    connecteur = sqlite3.connect("database.db")
    cursor = connecteur.cursor()
    mot=(cursor.execute("SELECT mot from dico where length(mot) = (?)",(nblettres,))).fetchall()
    connecteur.close()
    liste_mot=[]
    for i in range(len(mot)):
        liste_mot.append(mot[i][0])
    return liste_mot

def motvalide(prop):
    connecteur = sqlite3.connect("database.db")
    cursor = connecteur.cursor()
    verif=(cursor.execute("SELECT mot from dico where mot=(?)",(prop,))).fetchall()
    if not verif:
        return False
    connecteur.close()
    return True

