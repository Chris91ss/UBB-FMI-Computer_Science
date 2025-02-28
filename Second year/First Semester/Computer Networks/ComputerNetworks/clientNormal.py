import socket
import random

HOST = '172.20.10.11'
PORT = 12345
ROUND_DATA = [
    (0, 9),
    (10, 90),
    (100, 999),
    (1000, 9999)
]

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Connected to the game server.")
    try:
        round_index = 0
        while True:
            server_message = client_socket.recv(1024).decode()
            if not server_message:
                break
            print("Server:", server_message)
            
            if "Round" in server_message and "Make a guess" in server_message:
                try:
                    round_index = int(server_message.split()[1]) - 1
                except ValueError:
                    pass

                interval = ROUND_DATA[round_index]
                guess = random.randint(interval[0], interval[1])
                client_socket.sendall(str(guess).encode())

            if "Your final position" in server_message:
                print("Game over.")
                client_socket.sendall("score".encode())
                score_message = client_socket.recv(1024).decode()
                print("Your Score:", score_message)
                break

            if "Correct!" in server_message or "Incorrect" in server_message:
                round_index = min(round_index + 1, len(ROUND_DATA) - 1)

    finally:
        print("Disconnecting from the server.")
        client_socket.close()

if __name__ == "__main__":
    start_client()

