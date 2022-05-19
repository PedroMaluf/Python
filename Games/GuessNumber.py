import random


def guess_num(range_num):

    #Define a random number between one and the range inputed by the user
    random_num = random.randint(1,range_num)

    #Get the first guess from the user input
    guess = int(input(f"Try a number between 1 and {range_num}: "))

    #Counting the number of guesses
    count_guess = 1
    if guess != random_num:
        print("Sorry, wrong number. Try again!")
        dif0 = abs(guess - random_num)

    #This loop will keep going until the user get the number right
    while guess != random_num:
        guess = int(input("New guess: "))
        difaux = abs(guess - random_num)
        count_guess += 1

        #Return to the user if the new guess is closer or not from the right number
        if guess != random_num:
            if dif0 > difaux:
                print("Hotter! Try again!")
            elif dif0 < difaux:
                print("Colder! Try again")
            else:
                print("All the same! Try again")
        dif0 = difaux

    print(f"Correct! The right number is {random_num}! You have guesses {count_guess} times until you get it right")


def computer_guess(range_num):
    low = 1
    high = range_num
    tried_num =[]   #List of all number already guesses so it will not repeat itself

    #First guess
    guess = random.randint(low,high)
    feedback = input(f'Is {guess} your number (y/n)? ').lower()
    tried_num.append(guess)

    #Second guess
    if feedback == 'n':
        guess = random.randint(low,high)

        while guess in tried_num:
            guess = random.randint(low,high)
        tried_num.append(guess)

    #Loop will keep trying until the user inform that it guessed the right number
    while feedback != 'r' and feedback != 'y':

        #If the new guess is as far from the right number as the guess before the number must be exactly between them
        if feedback == 's':
            guess = (guess + tried_num[-2]) // 2

        else:

            #With every loop it update a new low or a new high, depending if the new guess is colder or hotter and if it is bigger or lower than the guess before
            if feedback == 'c':
                if tried_num[-2] > guess:
                    low = max((guess + tried_num[-2]) // 2,low)
                else:
                    high = min((guess + tried_num[-2]) // 2, high)
                guess = random.randint(low,high)

                while guess in tried_num:
                    guess = random.randint(low,high)
                tried_num.append(guess)

            elif feedback =='h':
                if tried_num[-2] > guess:
                    high = min((guess + tried_num[-2]) // 2,high)
                else:
                    low = max((guess + tried_num[-2]) // 2,low)
                guess = random.randint(low,high)

                while guess in tried_num:
                    guess = random.randint(low,high)
                tried_num.append(guess)
        
        feedback = input(f'Is {guess} the right number (r)? If not, am I colder (c), hotter(h) or is the same (s)?').lower()
    
    print(f'Yay! The computer guessed your number, {guess}, correctly!')


#Get the range of number option from the user input
range_num = int(input("How many options?"))

#Get if the user wanna try to guess or if they wants to let the computer guess and then call the right function
choice = input('Do you want yourself (me) or the computer (pc) to guess?')
if choice == 'me':
    guess_num(range_num)
else:
    computer_guess(range_num)
