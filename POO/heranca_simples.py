class Veiculo:
    def __init__(self, marca, ano):
        self._marca = marca
        self._ano = ano

    def detalhes(self):
        return f"Marca: {self._marca} | Ano: {self._ano}"

class Carro(Veiculo):
    def __init__(self, marca, ano, portas):
        super().__init__(marca, ano)
        self._portas = portas

    def detalhes(self):
        return f"Marca: {self._marca} | Ano: {self._ano} | Portas: {self._portas}" 

carro1 = Carro("BYD", 2025, 8)
carro2 = Carro("Fiat", 2016, 4)

print(carro1.detalhes())
print(carro2.detalhes())