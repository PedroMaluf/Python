import os
from posixpath import split

def main():
    i = 0

    path = '/'.join(input('File path: ').split('\\')) +'/'

    standard_text = input('New standard name: ')

    file_type = input('File type: ')

    for filename in os.listdir(path):
        os.rename(path + filename, path + standard_text + str(i + 1) + file_type)
        i += 1


if __name__ == '__main__':
    main()