import pygame
import sprites

pygame.init()
pygame.display.set_caption("CONNECT 4")

running = True
SCREEN_SIZE = 804, 800
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
BOARD_IMG_SIZE = 804, 692
COLUMNS, ROWS = 7, 6  # X, Y

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
clock = pygame.time.Clock()

board = sprites.VisibleBoard(BOARD_IMG_SIZE, (COLUMNS, ROWS), (0, SCREEN_HEIGHT - BOARD_IMG_SIZE[1]), SCREEN_SIZE)

current_colour = "red"

while running:
    events = pygame.event.get()

    screen.fill("grey")
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    chip_placed = board.update(events, current_colour)

    if chip_placed:
        if current_colour == "red":
            current_colour = "yellow"
        else:
            current_colour = "red"

    screen.blit(board.image, board.rect)

    pygame.display.flip()
    clock.tick()
    print(clock.get_fps())
