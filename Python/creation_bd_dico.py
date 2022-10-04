import sqlite3

d={'ù':'u','ç':'c','é':'e','à':'a','â':'a','û':'u','ü':'u','ö':'o','ô':'o','è':'e','î':'i','ï':'i','ë':'e','ê':'e'}
w=''
mot_liste=[]

with open("../Lexique.txt",'r',encoding='utf8') as file : 
    for line in file :
        line=line.lower()
        for k,v in d.items():
            line=line.replace(k,v)

        if not '-' in line:
            if not ' ' in line:
                if not "'" in line:
                    if not "." in line:
                        if not line in mot_liste :
                            w+=line
                            mot_liste.append(line)


with open("../dico_francais.txt",'w',encoding='utf8' ) as file :
    file.write(w)


connecteur = sqlite3.connect("../database.db")

cursor = connecteur.cursor()
table = cursor.execute("DROP TABLE IF EXISTS dico")
table1 = cursor.execute("CREATE TABLE dico(mot varchar PRIMARY KEY)")


with open("../dico_francais.txt",'r') as file:
    a=True
    while a:
        word=file.readline()
        if not word:
            a=False
            break
        word=word[:-1]
        cursor.execute("INSERT OR IGNORE INTO dico VALUES (?)",(word,))
        connecteur.commit()
        if not word:
            a=False
            break

connecteur.close()

# A été utilisé pour créer les dictionnaires par taille des mots
#i=1
#while i<=25:
#    w=''
#    with open("../dico_francais.txt",'r',encoding='utf8') as file :
#        for line in file :
#            if len(line)-1==i:
#                w+=line
#                
#
#    filename="../dico"+str(i)+".txt"
#    with open(filename,'w',encoding='utf8' ) as file :
#        file.write(w)
#   i+=1
