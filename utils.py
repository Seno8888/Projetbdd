from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["jeu_video"]


def sauvegarder_score(joueur, vagues):
    db.scores.insert_one({"joueur": joueur, "vagues": vagues})


def afficher_classement():
    print("CLASSEMENT")
    scores = list(db.scores.find().sort("vagues", -1).limit(3))
    if len(scores) == 0:
        print("aucun score enregistre")
    else:
        for i in range(len(scores)):
            s = scores[i]
            print(str(i + 1) + ". " + s["joueur"] + " - " + str(s["vagues"]) + " vagues")
