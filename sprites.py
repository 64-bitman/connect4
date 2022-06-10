import pygame
import numpy as np
from linetimer import CodeTimer


class BoardException(Exception):
    pass


class Board(pygame.sprite.Sprite):
    def __init__(self, img_size, board_size, topleft, screen_size):
        self.static_board = pygame.Surface(img_size).convert()  # to be drawn over `self.static_image`
        self.static_image = self.static_board.copy().convert_alpha()  # blank surface to blit in chips

        self.image = self.static_image.copy()
        self.rect = self.image.get_rect(topleft=topleft)
        self.colour = 0, 0, 255

        self.x_grid = None
        self.y_grid = None
        self.columns = {}

        self.screen_size = screen_size
        self.board_size = board_size
        self.cell_gap = 20  # distance between each cell and the border in px
        self.cell_size = (img_size[0] - self.cell_gap) / board_size[0] - self.cell_gap, \
                         (img_size[1] - self.cell_gap) / board_size[1] - self.cell_gap

        self.game_won = {"won": False, "colour": None, "chips": []}
        self.num_in_a_row = 4

        self.static_image.fill((0, 0, 0, 0))
        self.initiate_board()
        super().__init__()

    def update(self, events, current_color) -> bool:
        """draw everything onto the board and check any events"""
        self.image = self.static_image.copy()
        chip_placed = False
        current_color = current_color.lower() if current_color is not None else None

        for column_num, properties in self.columns.items():
            if current_color is not None:
                mouse_pos = pygame.mouse.get_pos()
                rel_screen_rect = properties["rect"].copy()  # column rect relative to the screen rect

                rel_screen_rect.topleft += pygame.Vector2(0, self.screen_size[1] - self.image.get_size()[1])

                # check if any columns have been clicked
                if rel_screen_rect.collidepoint(mouse_pos):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            self.place_chip(column_num, current_color)
                            chip_placed = not chip_placed
                            break

            # draw and update chips
            for chip in properties["chips"]:
                chip.fall()
                self.image.blit(chip.image, chip.rect)

        self.image.blit(self.static_board, (0, 0))

        if self.game_won["won"]:
            if all([chip.done_falling for chip in self.game_won["chips"]]):
                positions = [chip.rect.center for chip in self.game_won["chips"]]

                pygame.draw.lines(self.image, "black", False, positions, 7)

        return chip_placed

    def initiate_board(self):
        """calculate the cell positions, initiate the chips dict, and draw the board"""
        x_p = [x * (self.cell_size[0] + self.cell_gap) + self.cell_gap for x in range(0, self.board_size[0])]
        y_p = [y * (self.cell_size[1] + self.cell_gap) + self.cell_gap for y in range(0, self.board_size[1])]
        xx, yy = np.meshgrid(x_p, y_p, indexing="ij")

        self.x_grid = xx
        self.y_grid = yy

        # add column items (sets) to the chips dict
        for column in range(0, self.board_size[0]):
            column_size = self.cell_size[0] + self.cell_gap, self.rect.bottom
            column_topleft = (self.cell_size[0] + self.cell_gap) * column + self.cell_gap / 2, 0

            column_rect = pygame.Rect(*column_topleft, *column_size)
            # to represent empty cells that will be removed when a chip is added to that pos

            self.columns[column] = {"chips": set(), "rect": column_rect}

        # draw the board
        self.static_board.fill(self.colour)
        self.static_board.set_colorkey((0, 0, 0))  # make the cells in the board transparent

        for x in range(0, self.board_size[0]):
            for y in range(0, self.board_size[1]):
                cell_template = pygame.Surface((101, 101)).convert()
                cell_template.fill(self.colour)

                pygame.draw.circle(cell_template, (0, 0, 0), cell_template.get_rect().center, 50)
                cell_template = pygame.transform.scale(cell_template, self.cell_size)

                self.static_board.blit(cell_template, self.get_cell_pos(x, y))

        self.image = self.static_board.copy()

    def get_cell_pos(self, x, y):
        if 0 <= x < self.board_size[0] and 0 <= y < self.board_size[1]:
            return self.x_grid[x, y], self.y_grid[x, y]
        else:
            raise BoardException(f"CELL POSITION ({x}, {y}) OUT OF BOUNDS")

    def get_column_height(self, column_num):
        """return the position on top of the highest chip/bottom in the column"""
        return self.board_size[1] - len(self.columns[column_num]["chips"]) - 1

    def add_chip_to_set(self, chip, column_num):
        self.columns[column_num]["chips"].add(chip)

    def place_chip(self, column_num, colour):
        if len(self.columns[column_num]["chips"]) < self.board_size[1]:  # if column not full
            chip_board_pos = column_num, self.get_column_height(column_num)
            chip_position = self.get_cell_pos(*chip_board_pos)

            start_position = pygame.Vector2(self.get_cell_pos(column_num, 0)) + (0, -self.cell_size[1])
            new_chip = Chip(self.cell_size, colour, chip_board_pos, chip_position, start_position)

            self.add_chip_to_set(new_chip, column_num)
            self.check_x_consecutive_chips(chip_board_pos, colour, self.num_in_a_row)

    def check_x_consecutive_chips(self, board_pos, colour, count=4):
        """check if the chip makes x in a row"""
        board_pos = pygame.Vector2(board_pos)
        directions = (pygame.Vector2(-1, -1), pygame.Vector2(0, -1), pygame.Vector2(1, -1), pygame.Vector2(1, 0))
        winning_lines = {}

        # calculate all the possible points that make a line in each direction (ex.topleft and bottomright make a line)
        for direction in directions:
            line = [tuple(board_pos.copy() + direction * n) for n in range(0, count)]
            opposite_line = [tuple(board_pos.copy() + direction.rotate(180) * n) for n in range(1, count)]

            winning_lines[tuple(direction.xy)] = set(line + opposite_line)

        for direction, positions in winning_lines.items():
            winning_chips = set()
            found = 0

            # change all the positions that are occupied to the chip that occupies it
            for column_num, properties in self.columns.items():
                for chip in properties["chips"]:
                    if chip.colour == colour and chip.board_pos in positions:
                        positions.remove(chip.board_pos)
                        positions.add(chip)

            # check if there are any x consecutive lines
            for cell in sorted(positions, key=lambda x: (x[0], x[1])):
                if found < count:
                    if type(cell) == Chip:
                        found += 1
                        winning_chips.add(cell)
                    else:
                        found = 0
                        winning_chips.clear()
                else:
                    break

            if found >= count:
                self.game_won = {"won": True, "colour": colour, "chips": winning_chips}
                break


class VisibleBoard(Board):
    def __init__(self, img_size, board_size, topleft, screen_size):
        super().__init__(img_size, board_size, topleft, screen_size)



class Chip(pygame.sprite.Sprite):
    def __init__(self, size, colour, col_row, intended_pos, topleft=(0, 0)):
        self.image = pygame.transform.smoothscale(pygame.image.load("images/red_chip.png"), size).convert_alpha()

        if colour == "yellow":
            self.image = pygame.transform.smoothscale(pygame.image.load("images/yellow_chip.png"), size).convert_alpha()

        self.rect = self.image.get_rect(topleft=topleft)
        self.mask = pygame.mask.from_surface(self.image)

        self.size = size
        self.colour = colour
        self.board_pos = col_row
        self.intended_pos = intended_pos

        self.done_falling = False

        super().__init__()

    def fall(self):
        if not self.done_falling:
            if self.rect.top < self.intended_pos[1]:
                self.rect.move_ip(0, 10)

            if self.rect.top >= self.intended_pos[1]:
                self.done_falling = True
                self.rect.top = self.intended_pos[1]

    def __repr__(self):
        return f"Chip({self.colour}, {self.board_pos})"

    def __getitem__(self, index):
        return self.board_pos[index]


if __name__ == '__main__':
    ...