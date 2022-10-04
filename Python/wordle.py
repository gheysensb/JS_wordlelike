import random as rd

mots = ["bonjour", "bonsoir"]

def choix(nblettre,mots):
    """cette fonction permet de choix un mot d'une longeur donné dans le dictionnaire"""

    mot = rd.choice(mots)
    while len(mot) != nblettre:
        mot = rd.choice(mots)
    return(mot)

def validation(i,testmot,mot,count,tent):
    """cette fonction permet de tester chaque lettre et de dire si elle et valide correct mais pas ua bonne endroit ou incorrect"""

    if testmot[i] == mot[i]:
        # temporaire : affichage lettre au bon endroit
        tent[count][i] = (testmot[i], "2")

    elif testmot[i] in mot:
        # temporaire : affichage lettre correct mais mal placé
        tent[count][i] = (testmot[i], "1")
    else:
        # temporaire : affichage lettre incorrect
        tent[count][i] = (testmot[i], "0")

def motvalid(testmot,nblettre,mot,count,tent,essais):
    """cette fonction permet de determiner si un mot est correct ou pas"""

    for i in range(nblettre):
        validation(i,testmot,mot,count,tent)

    if testmot == mot:
        print("you win")
        return("win")

    elif testmot != mot and count == (essais - 1):
        print("you lose")
        return("lose")

def entree(nbl):
    """cette fonction test si le mot entree et de la bonne longueur et est dans le dictionnaire"""
    testmot=""
    while len(testmot) != nbl or not(testmot in mots):
        print(f"veuillez entrer un mot de {nbl} lettres valide : ")
        testmot = input()
        if len(testmot) != nbl:
            print("la longueur du mot n'est pas valide")
        elif not(testmot in mots):
            print("le mot n'est pas dans le dictionnaire")
    return(testmot)

def wordle(nbl, essais):

    tentatives = [0 for i in range(essais)]
    mot = choix(nbl,mots)

    for count in range(essais):
        test=entree(nbl)
        tent = [(0, 0) for i in range(len(mot))]
        tentatives[count] = tent[:]



        valid=motvalid(test,nbl,mot,count,tentatives,essais)
        if valid == "win":
            return()

        print(tentatives)


wordle(7, 6)
