import random
from pymongo import MongoClient
from models import Personnage, Monstre

client = MongoClient("mongodb://localhost:27017/")
db = client["jeu_video"]

liste = list(db.personnages.find())


def afficher_equipe():


    print("personnages disponibles")
    for i in range(len(liste)):
        p = liste[i]
        print(str(i + 1) + ". " + p["name"] + " - ATK: " + str(p["atk"]) + " - DEF: " + str(p["def"]) + " - PV: " + str(p["hp"]))

def equipes(equipe, deja_choisis):
    print("equipe actuelle")
    if len(equipe) == 0:
        print("vide")
    else:
        for p in equipe:
            print(p.nom + " - ATK: " + str(p.atk) + " - DEF: " + str(p.defense) + " - PV: " + str(p.pv))

    choix = int(input("choisissez le personnage : "))

    if choix - 1 in deja_choisis:
        print("ce personnage est deja dans lequipe")
    elif choix < 1 or choix > len(liste):
        print("numero invalide")
    else:
        deja_choisis.append(choix - 1)
        equipe.append(Personnage(liste[choix - 1]))

    return equipe, deja_choisis


def creer_equipe():
    equipe = []
    deja_choisis = []
    afficher_equipe()

    while len(equipe) < 3:
        equipe, deja_choisis = equipes(equipe, deja_choisis)        

    print("Mon equipe")
    for p in equipe:
        print(p.nom)

    return equipe


def cree_monstre():
    data = list(db.monstres.aggregate([{"$sample": {"size": 1}}]))[0]
    monstre = Monstre(data)
    return monstre

def attaque_personnage(equipe,monstre):
    
    for p in equipe:
        if p.pv > 0 and monstre.pv > 0:
            degats = p.atk - monstre.defense
            if degats < 1:
                degats = 0
            monstre.pv = monstre.pv - degats
            print(p.nom + " attaque " + monstre.nom + " moins " + str(degats) + " PV monstre: " + str(monstre.pv))

def monstre_envie(monstre):
    if monstre.pv > 0:
        return True
    
    return False
    
def perso_envie(equipe):
    vivants = []
    for p in equipe:
        if p.pv > 0:
            vivants.append(p)
    return vivants

def attaque_monstre(equipe, monstre):
    vivants = perso_envie(equipe)
    if not vivants:
        return
    cible = random.choice(vivants)
    degats = monstre.atk - cible.defense
    if degats < 1:
        degats = 0
    cible.pv = cible.pv - degats
    print(monstre.nom + " attaque " + cible.nom + " moins " + str(degats) + " PV restant: " + str(cible.pv))

    if cible.pv <= 0:
        print(cible.nom + " est mort")
        
        


def tous_mort(equipe):
    vivants = perso_envie(equipe)

    for p in vivants:
        if len(vivants) > 0:
            return False

    print("toute l'equipe est morte")
    return True

def etat_equipe(equipe):
    print("etat de l equipe")
    for p in equipe:
        if p.pv > 0:
            print(str(p.nom) + " a " + str(p.pv) + " PV")
        else:
            print(str(p.nom) + " : est mort")

def combat(equipe, vague):
    monstre = cree_monstre()

    print("vague " + str(vague))
    print("atk: " + str(monstre.atk) + " def: " + str(monstre.defense) + " pv: " + str(monstre.pv))

    while monstre_envie(monstre):
        print("attaques de lequipe")
        attaque_personnage(equipe, monstre)

        if monstre_envie(monstre):
            print("attaque du monstre")
            attaque_monstre(equipe, monstre)
            etat_equipe(equipe)
            if tous_mort(equipe):
                return False
    print(monstre.nom + " est vaincus")
    return True





def victoire(equipe):
    input("appuyez sur entree pour commencer")

    vagues = 0
    while True:
        vague_actuelle = vagues + 1
        resultat = combat(equipe, vague_actuelle)

        if resultat:
            vagues = vagues + 1
            print("score: " + str(vagues) + " vagues gagné")
            input("appuyez sur entree pour la prochaine vague")
        else:
            break

    return vagues


def jouer(joueur):
    equipe = creer_equipe()

    vagues = victoire(equipe)

    print("fin de partie")
    print("joueur: " + joueur)
    print("vagues gagné: " + str(vagues))
    return vagues

