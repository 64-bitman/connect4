import socket
import threading
import sprites
import game_mangement
from termcolor import colored

COLUMNS, ROWS = 7, 6  # X, Y

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
board = sprites.Board((COLUMNS, ROWS))
manager = game_mangement.GameManager()

server.bind((HOST, PORT))


def listen():
    server.listen()

    while True:
        conn, addr = server.accept()

        print(colored(f"new connection at {addr}", "red"))
        manager.add_player(conn, addr)


if __name__ == '__main__':
    listen()
