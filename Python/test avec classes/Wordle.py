from lettres import Lettres
import sqlite3

class Wordle:
    """la classe Wordle represente une instance de jeux  """
    essaisMax = 6
    tailleMot = 7

    def __init__(self,motSecret:str):
        self.motSecret: str = motSecret #mot a deviner
        self.essais = [] #liste des essais

    def essai(self,mot:str):
        self.essais.append(mot)

    def dejatest(self,lettre1:Lettres,mot:list):
        for i in mot:
            if lettre1.presente == i.presente and lettre1.correcte == i.correcte and lettre1.lettre == i.lettre:
                return True
            else:
                return False

    def validation(self,mot:str):
        """readaptation de la fonction utilisé dans le premier algorithme"""
        resultat = []
        for i in range(self.tailleMot):
            l = Lettres(mot[i])
            l.presente = mot[i] in self.motSecret
            l.correcte = (mot[i] == self.motSecret[i])
            resultat.append(l)

        for i in range(len(resultat)):
            nbl = 0
            nbc = 1

            for k in range(len(resultat)):
                l=resultat[i]
                lt=resultat[k]
                if l.lettre==lt.lettre:
                    nbl+=1
                if l.lettre==lt.lettre and l.correcte==True:
                    nbc+=1

            for j in range(len(resultat)):

                if i!=j:
                    l1=resultat[i]
                    l2=resultat[j]
                    if (l1.lettre==l2.lettre and l2.correcte==True and l1.correcte!=l2.correcte and nbl==nbc ):
                        resultat[i].presente = False
                    elif (l1.lettre==l2.lettre and l1.correcte==True and l1.correcte!=l2.correcte and nbl==nbc  ):
                        resultat[j].presente = False
                    elif (l1.lettre==l2.lettre and l2.correcte==l1.correcte==False and l1.presente==l2.presente ):
                        if i>j:
                            resultat[i].presente=False
                        else:
                            resultat[j].presente=False
                    else:
                        None
                else:
                    None

    @property
    def motValid(self):
        """propriété deffinissant si un mot est valide ou non"""
        if self.essais[-1]== self.motSecret:
            return True
        else:
            return False

    @property
    def motvalide(self):
        connecteur = sqlite3.connect("database.db")
        cursor = connecteur.cursor()
        verif = (cursor.execute("SELECT mot from dico where mot=(?)", (self.essais[-1],))).fetchall()
        if not verif:
            self.essais.pop()
            return False
        connecteur.close()
        return True

    @property
    def essaiPoss(self):
        """propriété deffinissant si il reste des essais"""
        if len(self.essais)<self.essaisMax:
            return True
        else:
            return False

