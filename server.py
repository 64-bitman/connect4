import socket
import pygame
import sprites

COLUMNS, ROWS = 7, 6  # X, Y

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4000
mformat = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
board = sprites.Board((COLUMNS, ROWS))

server.bind((HOST, PORT))

if __name__ == '__main__':
    board.add_chip(sprites.Chip("red", (1, 2)), 3)

    print(board.chips)
    print(board.check_x_consecutive_chips(()))
