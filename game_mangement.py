import socket
import threading
import time


class Player:
    connection: socket.socket

    def __init__(self, player_id, connection: socket.socket, address):
        self.id = player_id
        self.game_name = ""
        self.connection = connection
        self.address = address

    def __repr__(self):
        return f"Player(id: {self.id}, game_name: {self.game_name}, address: {self.address})"


class GameManager:
    """class for holding/managing all active games"""
    def __init__(self):
        self.active_games = []
        self.lobby = []  # players in waiting room
        self.format = "utf-8"

    def add_player(self, conn: socket.socket, addr):
        new_player = Player(len(self.lobby), conn, addr)
        new_thread = threading.Thread(target=self.manage_player, args=(new_player,))

        self.lobby.append(new_player)
        new_thread.start()

    def manage_player(self, player: Player):
        while True:
            str_lobby = str(self.lobby)
            header = "!" + str(len(str_lobby))

            header += " " * (4 - len(header))

            player.connection.sendall(header.encode(self.format))
            player.connection.sendall(str_lobby.encode(self.format))

    def create_game(self, player1, player2):
        new_game = Game(player1, player2)

        new_game.name = f"Game {len(self.active_games)}"
        self.active_games.append(new_game)

        return new_game


class Game:
    """class for managing/holding a game between players"""
    def __init__(self, player1, player2):
        self.name = ""
        self.current_color = "red"

    def start(self):
        ...

