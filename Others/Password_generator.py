import random

lower_case = 'abcdefghijklmnopqrstuvwxyz'
upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
chars ='!@#$%¨&*()-_=+[]{},.;:/?'
num = '1234567890'

#Get the passwords specs with the user
num_of_passwords = int(input("How many passwords do you want to create?"))
password_size = int(input("What is the size of the passwords?"))

aux = password_size + 1

while aux > password_size:
    num_lower_case = max(int(input("How many lower case letters?")),1)
    num_upper_case = int(input("How many upper case letters?"))
    num_chars = int(input("How many special characters?"))
    num_num = int(input("How many numbers?"))
    aux = num_lower_case + num_num + num_chars + num_upper_case

    if aux > password_size:
        print('This number does not add up. Remember your passwords will have {password_size} characters')

#Create the passwords
for passwords in range(num_of_passwords):
    count_lower_case = 0
    count_upper_case = 0
    count_chars = 0
    count_num = 0

    #Ensure the minimum amount of each type of character
    while count_lower_case < num_lower_case or count_upper_case < num_upper_case or count_chars < num_chars or count_num < num_num:
        password = []
        count_lower_case = 0
        count_upper_case = 0
        count_chars = 0
        count_num = 0

        for size in range(password_size):
            type = random.choice(['lower','upper','char','num'])

            if type == 'lower':
                password.append(random.choice(lower_case))
                count_lower_case += 1

            elif type == 'upper':
                password.append(random.choice(upper_case))
                count_upper_case += 1

            elif type == 'char':
                password.append(random.choice(chars))
                count_chars += 1

            elif type == 'num':
                password.append(random.choice(num))
                count_num += 1

    print(''.join(password))
