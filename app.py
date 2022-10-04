'''from crypt import methods
from operator import methodcaller quand vous l'utiliserez'''
from tkinter import N
from flask import Flask, session, redirect, render_template, request
import sqlite3
from datetime import datetime
from Python import tiragemot
from Python import stats
import hashlib as ha

app = Flask(__name__)
app.secret_key = 'laclé'
app.config["SESSION_TYPE"]="filesystem"

#Mettre ci-dessous successivement nom de la ressource, lien, et contribution
bibliographie = [
    ('W3 Schools','https://www.w3schools.com/css/','Toutes les pages'),
    ('mdn','https://developer.mozilla.org/fr/docs/Web/CSS','Toutes les pages'),
    ('France TV','https://www.france.tv/france-2/motus/',"Image page d'accueil"),
    ('Lexicon','http://www.lexique.org/',"Base de données du dictionnaire"),
    ('Wordle','https://www.nytimes.com/games/wordle/index.html','Le jeu Wordle')
    ]


@app.route('/')
def main():
        return render_template("main.html")

@app.route("/wordle/<int:nblettres>/<int:nbessais>")
def jeu(nblettres,nbessais):
        lemot = tiragemot.tiragemot(nblettres)
        dicofr=tiragemot.dico(nblettres)
        return render_template("worlde.html",taillemot = len(lemot), nbessai = nbessais,motatrouve=lemot,dico=dicofr)

@app.route("/endlesswordle")
def jeumode():
        dicofr=tiragemot.dico(5)
        return render_template("endlesswordle.html",taillemot = 5, nbessai = 8,dico=dicofr)

@app.route('/personnalisation',methods=['POST'])
def personalisation():
    nblettres=request.form.get('nblettres')
    nbessais=request.form.get('nbessais')
    url="/wordle/"+nblettres+"/"+nbessais
    return redirect(url)

@app.route('/jeu_pers')
def jeu_pers():
    return render_template("personnalisation.html")

@app.route('/bibliographie')
def biblio():
    return render_template("bibliographie.html", bibliographie = bibliographie)

@app.route('/register',methods=["GET","POST"])
def register():
    if session.get("identifiant"):
        return redirect("/")
    else:
        if request.method == "POST":
            conn = sqlite3.connect("database.db")

            cursor = conn.cursor()
            ident = request.form.get("Identifiant")
            motdepasse = request.form.get("password")
            doublon = (cursor.execute("SELECT * FROM utilisateurs WHERE identifiant = ? ",(ident,))).fetchall()

            max_id = (cursor.execute('SELECT max(id) FROM utilisateurs')).fetchall()
            id = str(max_id[0]).strip('(').strip(')').strip(',')
            if id == "None":
                id = 0
            else:
                id = int(id) + 1

            if len(doublon) == 0:
                session["identifiant"] = ident
                mdpc=motdepasse.encode() #preencodage
                h = ha.sha3_256(mdpc).hexdigest() #hashage
                cursor.execute("INSERT INTO utilisateurs VALUES(?,?,?)", (ident,h,id))
                cursor.execute("INSERT INTO statistiques VALUES((?),0,0,0,0,0,0,0,0,0,0,0)",(id,))
                conn.commit()
                return redirect("/")
            else:
                return render_template("register.html",prob = True)

    return render_template("register.html",prob = False)


@app.route('/login',methods=["GET","POST"])
def login():
        if session.get("identifiant"):
            return redirect("/")
        else:
            if request.method == "POST":
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                ident = request.form.get("Identifiant")
                motdepasse = request.form.get("password")
                mdpc = motdepasse.encode()  #preencodage pour le hash
                h = ha.sha3_256(mdpc).hexdigest() #hashage du mdp
                doublon = (cursor.execute("SELECT * FROM utilisateurs WHERE identifiant = ? AND motdepasse = ? ", (ident,h))).fetchall()
                if len(doublon) == 1 :
                    session["identifiant"]=ident
                    return redirect("/")
                else:
                    return render_template("login.html",prob =True)
            return render_template("login.html",prob=False)

@app.route('/save',methods=["GET","POST"])
def save():

        print(request.get_json())
        L = request.get_json()
        mot = L[-4]
        etat = L[-2]
        chrono = L[-1]
        historique = ''
        analyse = ''
        for j in range(len(L)-4):
            historique = historique +'/'
            analyse = analyse + '/'
            for i in range(len(L[j])):
                historique = historique + L[j][i][0]
                analyse = analyse + L[j][i][1]

        dateheure = str(datetime.now())[:-8]
        pseudo = session.get("identifiant")
        nbessai = L[-3]
        connecteur = sqlite3.connect("database.db")

        cursor = connecteur.cursor()
        max_id = (cursor.execute('SELECT id FROM utilisateurs WHERE identifiant = ?',(pseudo,))).fetchall()
        idu = str(max_id[0]).strip('(').strip(')').strip(',')
        if idu == "None":
            idu = 0
        max_id = (cursor.execute('SELECT max(id) FROM historique')).fetchall()
        id = str(max_id[0]).strip('(').strip(')').strip(',')
        if id == "None":
            id = 0
        else:
            id = int(id)+1
        


        categorie = (cursor.execute("INSERT INTO historique VALUES(?,?,?,?,?,?,?,?,?,?)",(id, pseudo, mot, dateheure, historique, analyse,nbessai,etat,idu,chrono)))
        connecteur.commit()


        ranking=(cursor.execute("SELECT ranking FROM statistiques where id=(?)",(idu,))).fetchall()[0][0]
        trymoy=(cursor.execute("SELECT trymoy FROM statistiques where id=(?)",(idu,))).fetchall()[0][0]
        
        if trymoy==0:
            trymoy=nbessai
        else :
            trymoy=(trymoy+nbessai)/2
        if etat=="Victoire":
            tmin=(cursor.execute("SELECT tmin FROM statistiques where id=(?)",(idu,))).fetchall()[0][0]
            tmoy=(cursor.execute("SELECT tmoy FROM statistiques where id=(?)",(idu,))).fetchall()[0][0]
            if chrono<tmin or tmin==0:
                tmin=chrono
            if tmoy==0:
                tmoy=chrono
            else:
                tmoy=(tmoy+chrono)/2
            best = (cursor.execute("SELECT best FROM statistiques where id=(?)",(idu,))).fetchall()[0][0]
            niceperf = (cursor.execute("SELECT niceperf FROM statistiques where id=(?)",(idu,))).fetchall()[0][0]
            maxstreak = (cursor.execute("SELECT maxstreak FROM statistiques where id=(?)",(idu,))).fetchall()[0][0]
            streak = (cursor.execute("SELECT streak FROM statistiques where id=(?)",(idu,))).fetchall()[0][0]
            streak+=1
            ranking+=1
            if maxstreak<streak:
                maxstreak=streak
            if nbessai<best or best==0:
                best=nbessai
            if nbessai<=3:
                niceperf+=1
            cursor.execute("UPDATE statistiques SET wins=wins+1, trymoy=(?),best=(?),niceperf=(?),streak=(?),maxstreak=(?),tmin=(?),tmoy=(?),ranking=(?) WHERE id=(?)",(trymoy,best,niceperf,streak,maxstreak,tmin,tmoy,ranking,idu))
            connecteur.commit()
        else : 
            if ranking<1:
                ranking=0
            else:
                ranking=ranking-1
            cursor.execute("UPDATE statistiques SET looses=looses+1, trymoy=(?), streak=0,ranking=(?) WHERE id=(?)",(trymoy,ranking,idu))
            connecteur.commit()

        return redirect("/")

@app.route('/historique')
def histo():
    if not(session.get("identifiant")):
        return redirect("/")
    ident = session["identifiant"]
    print(ident)
    connecteur = sqlite3.connect("database.db")
    cursor = connecteur.cursor()
    Listepartie = (cursor.execute('SELECT * FROM historique WHERE pseudo=?',(ident,))).fetchall()
    return render_template("historique.html",Lparty = Listepartie)

@app.route('/logout')
def logout():
        session["identifiant"] = None
        return render_template("main.html")

@app.route('/historique/détail/<id>',methods=["GET","POST"])
def histdét(id):
    id = int(id)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    latabledesinfos = (cursor.execute('SELECT * FROM historique WHERE id = ?',(id,))).fetchall()
    latabledesinfos = latabledesinfos[0]
    Lpartie = []

    mots = latabledesinfos[4].split('/')
    mots.pop(0)

    analyse = latabledesinfos[5].split('/')
    analyse.pop(0)
    for i in range(len(mots)):
        J = []
        for j in range(len(mots[i])):
            J.append((mots[i][j].upper(),analyse[i][j]))
        Lpartie.append(J)
    return render_template("détail_partie.html",Lpartie=Lpartie,latabledesinfos=latabledesinfos)

@app.route('/profile')
def profile():
    if not(session.get("identifiant")):
        return redirect("/")
    connecteur = sqlite3.connect("database.db")
    cursor = connecteur.cursor()
    ident = session["identifiant"]
    id=cursor.execute('SELECT id FROM utilisateurs WHERE identifiant=?',(ident,)).fetchall()[0][0]
    print(id)
    stat=cursor.execute('SELECT wins,looses,tmoy,tmin,trymoy,best,niceperf,streak,maxstreak,scoreend FROM statistiques WHERE id=?',(id,)).fetchall()
    connecteur.commit()
    stats.graph(1,id)
    print(cursor.execute('SELECT * FROM statistiques').fetchall())
    print(cursor.execute('SELECT * FROM historique').fetchall())
    print(cursor.execute('SELECT * FROM utilisateurs').fetchall())

    return render_template("profile.html",nbgames=stat[0][0]+stat[0][1], wins=stat[0][0],looses=stat[0][1],tmoy=stat[0][2],tmin=stat[0][3],trymoy=stat[0][4],best=stat[0][5],niceperf=stat[0][6],streak=stat[0][7],maxstreak=stat[0][8],scoreend=stat[0][9])

@app.route('/endlesssave',methods=['POST'])
def endlessave():
    L = request.get_json()
    score = L[0]
    score = int(score)
    pseudo = session.get("identifiant")
    connecteur = sqlite3.connect("database.db")
    cursor = connecteur.cursor()
    max_id = (cursor.execute('SELECT id FROM utilisateurs WHERE identifiant = ?',(pseudo,))).fetchall()
    idu = str(max_id[0]).strip('(').strip(')').strip(',')
    scoreend = (cursor.execute("SELECT scoreend FROM statistiques where id=(?)",(idu,))).fetchall()[0][0]
    if score > scoreend:
        scoreend = score
    cursor.execute("UPDATE statistiques SET scoreend=(?)  WHERE id=(?)",(scoreend,idu))
    connecteur.commit()
    return redirect('/')

@app.route('/TV')
def tv():
    return render_template("TVMotus.html")

if __name__ == '__main__':
    app.run()