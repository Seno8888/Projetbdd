# Projet ELIO CHARNAY


from game import jouer
from utils import afficher_classement, sauvegarder_score


while True:
    choix = int(input("1 demarrer le jeu, 2 classement, 3 quitter : "))

    if choix == 1:
        joueur = input("votre nom : ")
        vagues = jouer(joueur)
        sauvegarder_score(joueur, vagues)
        afficher_classement()

    elif choix == 2:
        afficher_classement()

    elif choix == 3:
        
        break

