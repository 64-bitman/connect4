import socket
import threading
import sprites
from termcolor import colored

COLUMNS, ROWS = 7, 6  # X, Y

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
board = sprites.Board((COLUMNS, ROWS))

server.bind((HOST, PORT))


if __name__ == '__main__':

    def listen():
        server.listen()

        while True:
            conn, addr = server.accept()

            try:
                print(colored(f"new connection at {addr}", "red"))
            except socket.error:
                print(colored(f"connection closed at {addr}", "red"))
                conn.close()


    x = board.add_chip_to_column(1, "red")
    board.add_chip_to_column(1, "red")
    board.add_chip_to_column(1, "red")
    board.add_chip_to_column(1, "red")

    print(board.check_x_consecutive_chips(x))
