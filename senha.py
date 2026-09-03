tentativas = 0
limite = 4

senha = int(input("Digite sua primeira senha: "))
senha_colocada = int(input("Digite uma senha: "))

while senha_colocada != senha:
    tentativas += 1

    if tentativas == limite:
        print("Tentativa final! Bloqueio automático em caso de erro!")

    if tentativas > limite:
        print("Conta bloquada. Excedeu o limite de tentativas!")
        break

    senha_colocada = int(input("Senha incorreta, digite a senha correta: "))
    
else:
    print("Bem vindo(a)!")

