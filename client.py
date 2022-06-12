import time
import socket
import pygame
import sprites
from termcolor import colored

pygame.init()
pygame.display.set_caption("CONNECT 4")

SCREEN_SIZE = 804, 800
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
BOARD_IMG_SIZE = 804, 692
COLUMNS, ROWS = 7, 6  # X, Y

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4000
mformat = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))
current_colour = "red"


def game_loop():
    pygame.init()
    pygame.display.set_caption("CONNECT 4")
    running = True

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
    clock = pygame.time.Clock()

    board = sprites.VisibleBoard(BOARD_IMG_SIZE, (COLUMNS, ROWS), (0, SCREEN_HEIGHT - BOARD_IMG_SIZE[1]), SCREEN_SIZE)

    while running:
        events = pygame.event.get()

        screen.fill("grey")
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        chip_placed = board.update(events, current_colour)

        screen.blit(board.image, board.rect)

        pygame.display.flip()
        clock.tick()


buffer = ""

while True:
    header = client.recv(4).decode(mformat)

    if "!" in header:
        header = int(header.split("!")[1])
    else:
        continue

    print(colored(f"\r{client.recv(header).decode(mformat)}", "red"), end='')

