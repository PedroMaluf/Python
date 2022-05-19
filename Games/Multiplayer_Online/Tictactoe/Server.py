import socket
from _thread import *
import pickle
from Game import Game


server = '192.168.0.5'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def read_pos(str):
    str = str.split(",")
    return int(float(str[0])), int(float(str[1]))


def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])


try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print('Waiting for a connection, Server Started')

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount

    conn.send(str.encode(str(p)))
    reply = ''

    while True:
        try:
            data = conn.recv(4096*4).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset()
                    elif data != 'get':
                        print(data)
                        data = read_pos(data)
                        print(data)
                        game.play(p, data)
                    
                    conn.sendall(pickle.dumps(game))

            else:
                break
        except:
            break
            
    print('Lost connection')
    try:
        del games[gameId]
        print('Closing Game ', gameId)
    except:
        pass

    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print('Connected to:', addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print('Crating a new game...')
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
