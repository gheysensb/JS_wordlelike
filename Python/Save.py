import sqlite3
import datetime
def sauvegarde(L,pseudo,mot):
    '''
    On considère que la liste L contient pour chacune de ses cases une liste a deux elts avec la tentative
    [[ tentative , si lettres mauvaise bonnes place ]]

    On veut en sortie un ajout a la db avec une chaine de caractere contenant les infos de la partie
    '''

    historique = L[0][0]
    analyse = L[0][1]
    for i in range(1,len(L)):
        historique = historique+","+L[i][0]
        analyse = analyse+","+L[i][1]
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    max_id = (cursor.execute('SELECT max(id) FROM historique')).fetchall()
    id = int(str(max_id[0]).strip('(').strip(')').strip(',')) + 1
    dateheure = str(datetime.now())[:-7]
    categorie = (cursor.execute("INSERT INTO historique VALUES(?,?,?,?,?,?)",(id,pseudo,mot,dateheure,historique,analyse))
    conn.commit()

def historique(pseudo):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    max_id = (cursor.execute('SELECT ')).fetchall()

