nome_1 = input("Insira o nome da primeira pessoa: ")
idade_1 = int(input("Insira a idade da primeira pessoa: "))
nome_2 = input("Insira o nome da segunda pessoa: ")
idade_2 = int(input("Insira a idade da segunda pessoa: "))

media_idades = (idade_1 + idade_2) / 2

print(f"DADOS DA PRIMEIRA PESSOA: \n Nome: {nome_1} \n Idade: {idade_1}" )
print("\n")
print(f"DADOS DA SEGUNDA PESSOA: \n Nome: {nome_2} \n Idade: {idade_2}" )
print(f"Idade média entre {nome_1} e {nome_2} é de: {media_idades:.2f}")

