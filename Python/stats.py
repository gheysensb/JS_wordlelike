import sqlite3
import matplotlib.pyplot as plt
from math import pi



def ratio(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    data = cursor.execute("SELECT  wins,looses FROM statistiques WHERE id=?",(id,)).fetchall() #on prends le nombre de victoire et de defaite
    if data==[]:
        return 0
    win = data[0][0]
    los = data[0][1]
    if win==0 and los==0:
        return 0
    conn.commit()
    return  win / (win + los) * 100  #on calcul le poucentage de victoire

def rank(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    data=cursor.execute("SELECT ranking FROM statistiques").fetchall()
    nbu=cursor.execute("SELECT count(id) FROM statistiques").fetchall()[0][0]
    if data==[] or nbu==[]:
        return 0
    rang=data[id][0]
    top=((nbu-rang)/nbu)*100
    print(top)
    conn.commit()
    return (top)



def moy(column):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    sum = 0

    if column == "wins":    #si on veux la moyennne du nombre de victoire
        curs = cursor.execute("SELECT wins,looses FROM statistiques").fetchall()
        for i in range(len(curs)):  #somme puis division du nombre d'items
            sum += ratio(i)
        moyenne = sum / len(curs)
    else:                   #si on veux la moyennne des autres stats
        curs = cursor.execute("SELECT " + column + " FROM statistiques").fetchall()
        for i in range(len(curs)):  #somme puis division du nombre d'items
            sum += curs[i][0]
        moyenne = sum / len(curs)
    conn.commit()
    return moyenne


def scale(column, id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if column != "wins":    #on a deja les victoire et le rang sous forme de pourcentage
        curs = cursor.execute("SELECT " + column + " FROM statistiques WHERE id=?",(id,)).fetchall()[0][0]
        print(curs)
        conn.commit()
        if curs==[]:
            return 0

        if moy(column)==0:
            return 0

        return ( curs * 50) / moy(column)     #on se remene a un intervalle de 0 a 100 centre en 50


def graph(nbG, *args):
    if nbG == 1:
        id = args[0]

        wins = ratio(id)
        tmoy = scale("tmoy", id)
        trymoy = scale("trymoy", id)
        niceperf = scale("niceperf", id)
        ranking = scale("ranking",id)

        labels = ["ESSAIS", "REGULARITÉ", "RAPIDITÉ", "RANG", "PERFORMANCES"]
        N = len(labels)
        valeurs = [trymoy, wins, tmoy, ranking, niceperf, trymoy]  # on rajoute wins a la fin pour fermer le graphe
        print(valeurs)
        angles = [n / float(N) * 2 * pi for n in range(N)]  # angle entre chaque ligne du graphe
        angles += angles[:1]
        # Initialise the spider plot
        plt.figure(facecolor=(1.0, 0.47, 0.42, 0))
        ax = plt.subplot(111, polar=True)

        # Draw one axe per variable + add labels

        plt.xticks(angles[:-1], labels, color='black', size=8)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([25, 50, 75], ["25", "50", "75"], color="black", size=7)
        plt.ylim(0, 100)

        # Plot data
        ax.plot(angles, valeurs, linewidth=1, linestyle='solid', color="red")

        # Fill area
        ax.fill(angles, valeurs, 'red', alpha=0.4)
        ax.set_facecolor((1.0, 0.47, 0.42))

        # Show the graph
        plt.savefig("static/graphe.png")
        plt.close()
    elif nbG == 2:

        labels = ["essais", "regularité", "rapidité", "rang", "performance"]
        N = len(labels)

        angles = [n / float(N) * 2 * pi for n in range(N)]  # angle entre chaque ligne du graphe
        angles += angles[:1]
        # Initialise the spider plot
        plt.figure(facecolor=(1.0, 0.47, 0.42, 0))
        ax = plt.subplot(111, polar=True)

        # Draw one axe per variable + add labels

        plt.xticks(angles[:-1], labels, color='white', size=8)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([25, 50, 75], ["25", "50", "75"], color="white", size=7)
        plt.ylim(0, 100)

        # Plot data
        count = 0
        for i in args:

            wins = ratio(i)
            tmoy = scale("tmoy", i)
            trymoy = scale("trymoy", i)
            niceperf = scale("niceperf", i)
            ranking = scale("ranking",i)
            valeurs = [trymoy, wins, tmoy, ranking, niceperf, trymoy]  # on rajoute wins a la fin pour fermer le graphe
            if count == 0:
                ax.plot(angles, valeurs, linewidth=1, linestyle='solid', color="red")
                ax.fill(angles, valeurs, 'red', alpha=0.4)
                count += 1
            else:
                ax.plot(angles, valeurs, linewidth=1, linestyle='solid', color="yellow")
                ax.fill(angles, valeurs, 'yellow', alpha=0.4)
        # Fill area

        ax.set_facecolor((1.0, 0.47, 0.42))

        # Show the graph

        plt.savefig("static/graphe.png")
        plt.close()

graph(1,0)