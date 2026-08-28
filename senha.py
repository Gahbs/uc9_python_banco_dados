senha = int(input("Digite sua primeira senha: "))
senha_colocada = int(input("Digite uma senha: "))

while senha_colocada != senha:
    senha_colocada = int(input("Senha incorreta, digite a senha correta: "))

print("Senha correta, bem vindo(a)!!" )