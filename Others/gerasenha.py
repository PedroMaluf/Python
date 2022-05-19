import random

letrasmin = 'abcdefghijklmnopqrstuvwxyz'
letrasmax = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
caracs ='!@#$%¨&*()-_=+[]{},.;:/?'
num = '1234567890'

numdesenhas = int(input("Quantas senhas vc quer gerar?"))
tamanhosenhas = int(input("Qual o tamanho das senhas?"))

aux = tamanhosenhas + 1

while aux > tamanhosenhas:
    numletrasmin = int(input("Quantas letras minusculas obrigatorias?"))
    numletrasmax = int(input("Quantas letras maisculas obrigatorias?"))
    numcarac = int(input("Quantas simbolos obrigatorios?"))
    numnum = int(input("Quantos numeros obrigatorios?"))
    aux = numletrasmin + numnum + numcarac + numletrasmax
    if aux > tamanhosenhas:
        print('Nao ta batendo o tamanho. Lembra que suas senhas vao ter apenas {tamanhosenhas} caracteres')

for sen in range(numdesenhas):
    contnumletrasmin = 0
    contnumletrasmax = 0
    contnumcarac = 0
    contnumnum = 0
    while contnumletrasmin < numletrasmin or contnumletrasmax < numletrasmax or contnumcarac < numcarac or contnumnum < numnum:
        senhas = ''
        contnumletrasmin = 0
        contnumletrasmax = 0
        contnumcarac = 0
        contnumnum = 0
        for tam in range(tamanhosenhas):
            qualtipo = random.choice(['min','max','carac','num'])
            if qualtipo == 'min':
                senhas += random.choice(letrasmin)
                contnumletrasmin += 1
            elif qualtipo == 'max':
                senhas += random.choice(letrasmax)
                contnumletrasmax += 1
            elif qualtipo == 'carac':
                senhas += random.choice(caracs)
                contnumcarac += 1
            elif qualtipo == 'num':
                senhas += random.choice(num)
                contnumnum += 1
    print(senhas)
