import logging
import socket
import json
import re

FORMAT = "utf-8"
HEADER_SIZE = 6
HOST = socket.gethostbyname(socket.gethostname())
PORT = 4000

WAITING = "waiting"
FULL = "full"
EMPTY = "empty"
ACTIVE = "active"

CONFIRM = "CONFIRM"
MADE_NICKNAME = "MADE_NICKNAME"
GET_GAMES = "GET_GAMES"

GAME_DATA_STR = "GAME DATA STR"
GAME_DATA = "GAME DATA"

GAME_DELETED = "game_deleted"
GAME_COMMAND = "GAME_COMMAND"
INGAME_COMMAND = "ingame_command"

STARTED_GAME = "started game"
LEFT_GAME = "left game"

NOT_HOST_ERROR = "can only start the game if you are the host"
COMMAND_INVALID_ERROR = "command is invalid"
GAME_IS_INVALID_ERROR = "game to be joined does not exist or you have already created a game"

NAME_ALREADY_EXISTS_ERROR = "nickname already exists"
NAME_IS_INVALID_LENGTH_ERROR = "nickname must be/over 4 characters and be/below 20 characters"
NAME_CONTAINS_INVALID_CHARS_ERROR = "nickname must only contain alphanumeric characters"


def send_msg(msg: str, msg_type, conn: socket.socket, header_size, msg_format="utf-8"):
    json_msg = json.dumps({"contents": msg, "type": msg_type})
    header = ":" + str(len(json_msg))
    header += " " * (header_size - len(header) - 1) + ":"

    conn.sendall(header.encode(msg_format))
    conn.sendall(json_msg.encode(msg_format))


def recv_msg(conn: socket.socket, header_size, msg_format="utf-8"):
    header = b""

    while True:
        recv_header = conn.recv(header_size - len(header))
        header += recv_header
        if len(header) == HEADER_SIZE or recv_header == b"":
            break

    if re.match(r":\d+\s*:", header.decode(msg_format)):
        header_length = int(header[1:-1])  # remove the colons sandwiching the number
        msg = b""

        while True:
            recv_msgx = conn.recv(header_length - len(msg))

            msg += recv_msgx
            if len(msg) == header_length:
                break
            if recv_msgx == b"":
                return False

        try:
            json_msg = json.loads(msg.decode(msg_format))

            return json_msg
        except json.JSONDecodeError:
            logging.error("JSON decode error")

    return False


def send_validation(validation: bool, conn, header_size, opt_contents=None):
    send_msg((validation, opt_contents), CONFIRM, conn, header_size)


def confirm_validation(conn, header_size):
    while True:
        validation = recv_msg(conn, header_size)

        if validation is not False:
            if validation["type"] == CONFIRM:
                return validation["contents"]
