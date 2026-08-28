largura = float(input("Digite a largura do terreno: "))
comprimento = float(input("Digite o comprimento do terreno: "))
metro_quadrado = float(input("Digite o valor do metro quadrado: "))

area = largura * comprimento
valor = area * metro_quadrado

print(f"A área do terreno é: ", area)
print(f"O valor do terreno é: {valor:.2f}")