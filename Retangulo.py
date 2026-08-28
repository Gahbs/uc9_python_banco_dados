import math

base = float(input("Digite a base do retângulo: "))
altura = float(input("Digite a altura do retangulo: "))

area = base * altura
perimetro = (base * 2) + (altura * 2)
diagonal = math.sqrt (base**2 + altura **2)

print("Área do retângulo: ", area)
print("Perímetro do retângulo: ", perimetro)
print("Diagonal do retângulo: ", diagonal)
