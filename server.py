import socket
import pygame
import sprites

SCREEN_SIZE = 804, 800
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
BOARD_IMG_SIZE = 804, 692
COLUMNS, ROWS = 7, 6  # X, Y

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4000
mformat = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
board = sprites.VisibleBoard(BOARD_IMG_SIZE, (COLUMNS, ROWS), (0, SCREEN_HEIGHT - BOARD_IMG_SIZE[1]), SCREEN_SIZE)

server.bind((HOST, PORT))

if __name__ == '__main__':
    board.place_chip(2, "red")

    print(board.columns["chips"])
