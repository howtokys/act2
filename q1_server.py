import pickle
import socket
from typing import Any

user_credentials: dict = {"user1": "pass1", "user2": "pass2"}
server_inventory: dict = {0xA1: 50, 0xB2: 30}

PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
is_logged_in: bool = False
should_end: bool = False

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDRESS)
    return s

def start_listening(s: socket.socket):
    s.listen()
    print(f"Server is listening on {SERVER}:{PORT}")

def handle_login(credentials: dict) -> bytes:
    user_id = list(credentials.keys())[0]
    if user_id in user_credentials and credentials[user_id] == user_credentials[user_id]:
        global is_logged_in
        is_logged_in = True
        return b"S"
    return b"F"

def handle_inventory() -> bytes:
    return b"S" + pickle.dumps(server_inventory)

def handle_purchase(item_request: dict) -> bytes:
    item_upc = next(iter(item_request))
    item_qty = item_request[item_upc]
    if item_upc not in server_inventory:
        return b"Z"
    elif server_inventory[item_upc] < item_qty:
        return b"Y"
    server_inventory[item_upc] -= item_qty
    return b"S"

def handle_logout() -> bytes:
    global is_logged_in
    is_logged_in = False
    return b"S"

def process_request(connection_socket: socket.socket):
    try:
        received_data = connection_socket.recv(1024)
        if not received_data:
            global should_end
            should_end = True
            return
        header = received_data[:1].decode()
        response_body = b""
        received_body = None

        if header != "1" and not is_logged_in:
            status = b"F"
            connection_socket.send(header.encode() + status)
            return

        if header == "1":
            received_body = pickle.loads(received_data[2:])
            response_body = handle_login(received_body)
        elif header == "2":
            response_body = handle_inventory()
        elif header == "4":
            received_body = pickle.loads(received_data[2:])
            response_body = handle_purchase(received_body)
        elif header == "5":
            response_body = handle_logout()

        connection_socket.send(header.encode() + response_body)
    except Exception as e:
        print(f"Error processing request: {e}")

def main():
    s = create_socket()
    start_listening(s)
    connection_socket, connection_address = s.accept()
    while not should_end:
        process_request(connection_socket)
    connection_socket.close()
    s.close()

if __name__ == "__main__":
    main()