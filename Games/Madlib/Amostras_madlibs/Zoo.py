def madlib():

    #Get the necessary words from the user input
    parente = input("Parente: ")
    animal1 = input("Animal: ")
    animal2 = input("Outro animal: ")
    adj1 = input("Adjetivo: ")
    adj2 = input("Outro adjetivo: ")
    verbo1 = input("Verbo no gerundio: ")

    #Include the words on the text
    madlib = f"Fui no zoologico com a meu/minha {parente} e quando chegamos lá vimos um(a) {animal1} {adj1} {verbo1} com um(a) {animal2} {adj2}!"

    #Print the text for the user
    print(madlib)
