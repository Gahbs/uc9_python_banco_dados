class Animal:
    def __init__(self, comer):
        self._comer = comer

class Voador:
    def __init__(self, voar):
        self._voar = voar

class Morcego(Animal, Voador): 
    def __init__(self, comer, voar):
        Animal.__init__(self, comer)
        Voador.__init__(self, voar)

    def detalhes(self):
        return f"Comer: {self._comer} | Voar: {self._voar}"

morcegao = Morcego("Está comendo", "Está Voando")

print(morcegao.detalhes())