class Personnage:
    def __init__(self, data):
        self.nom = data["name"]
        self.atk = data["atk"]
        self.defense = data["def"]
        self.pv = data["hp"]


class Monstre:
    def __init__(self, data):
        self.nom = data["name"]
        self.atk = data["atk"]
        self.defense = data["def"]
        self.pv = data["hp"]
