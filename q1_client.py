import pickle
import socket
from typing import Any

local_inventory: dict = {}
current_item: dict = {}
is_logged_in: bool = False
should_end: bool = False

PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

def create_socket() -> socket.socket:
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server(s: socket.socket):
    s.connect(ADDRESS)

def receive_response(s: socket.socket) -> tuple[str, bytes]:
    received_data = s.recv(1024)
    status = received_data[1:2].decode()
    received_body = received_data[2:]
    return status, received_body

def display_menu() -> str:
    if not is_logged_in:
        print("1. User Login")
    print("2. View Current Server Inventory")
    print("3. View local inventory")
    print("4. Purchase Items")
    print("5. Logout")
    print("6. Quit")
    user_input = input("=> ")
    return str(user_input)

def handle_login_response(status: str):
    if status == "S":
        global is_logged_in
        is_logged_in = True
        print("Login Successful")
    else:
        print("Login Failed")

def display_inventory(response: bytes):
    inventory: dict = pickle.loads(response)
    print("Here is the server inventory")
    for item, quantity in inventory.items():
        print(f"{item}: {quantity}")

def display_local_inventory():
    print("Here is the local inventory")
    for item, quantity in local_inventory.items():
        print(f"{item}: {quantity}")

def handle_purchase_response(status: str):
    if status == "Z":
        print("Item not found")
    elif status == "Y":
        print("Item out of stock")
    elif status == "S":
        for key, val in current_item.items():
            if key in local_inventory:
                local_inventory[key] += val
            else:
                local_inventory[key] = val
        print("Purchase successful")

def logout():
    global is_logged_in
    is_logged_in = False

def process_data(s: socket.socket):
    choice = display_menu()
    if choice == "3":
        display_local_inventory()
        return
    if choice == "6":
        global should_end
        should_end = True
        return
    if choice != "1" and not is_logged_in:
        print("Need to be logged in")
        return

    send_request(s, choice)
    status, response_bytes = receive_response(s)

    if choice == "1":
        handle_login_response(status)
    elif choice == "2":
        display_inventory(response_bytes)
    elif choice == "4":
        handle_purchase_response(status)
    elif choice == "5":
        logout()

def send_request(s: socket.socket, header):
    body: Any = b"X"
    if header == "1":
        user_id = input("User ID: ")
        password = input("Password: ")
        credentials = {user_id: password}
        body = pickle.dumps(credentials)
    elif header == "4":
        item_upc = input("Item UPC: ")
        item_quantity = input("Item Quantity: ")
        global current_item
        current_item = {int(item_upc): int(item_quantity)}
        body = pickle.dumps(current_item)
    message = header.encode() + b"X" + body
    s.send(message)

def load_local_inventory():
    with open("localInv.pickle", "rb") as f:
        global local_inventory
        local_inventory = pickle.load(f)

def unload_local_inventory():
    with open("localInv.pickle", "wb") as f:
        pickle.dump(local_inventory, f)

def main():
    s = create_socket()
    connect_to_server(s)
    while not should_end:
        process_data(s)
    s.close()

if __name__ == "__main__":
    load_local_inventory()
    main()
    unload_local_inventory()