class Lettres:

    def __init__(self,lettre:str): #un etat de lettre est definit par sa lettre si presente et si correctement placée
        self.lettre: str = lettre #mot a deviner
        self.presente: bool = False #si la lettre est présente
        self.correcte: bool = False #si la lettre est au bon endroit
        pass