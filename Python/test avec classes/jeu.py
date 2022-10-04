from Wordle import Wordle
import random as rd
from lettres import Lettres

def main():
    print("hello world!")
    wordle=Wordle("bonsoir")
    while wordle.essaiPoss :
        m = input("test : ")
        wordle.essai(m)
        if wordle.motValid :
            return("you win")

if __name__=="__main__":
    main()