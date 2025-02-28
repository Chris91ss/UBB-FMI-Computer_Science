import socket

HOST = '172.20.10.11'  
PORT = 12345

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Connected to the game server.")
    try:
        while True:
            server_message = client_socket.recv(1024).decode()
            if not server_message:
                break
            print("Server:", server_message)
            
            if "Make a guess" in server_message:
                guess = input("Enter your guess: ")
                client_socket.sendall(guess.encode())
            
            if "Your final position" in server_message:
                print("Game over.")
                view_score = input("Would you like to see your final score? (yes/no): ").strip().lower()
                if view_score == "yes":
                    client_socket.sendall("score".encode())
                    score_message = client_socket.recv(1024).decode()
                    print("Your Score:", score_message)
                break

    finally:
        print("Disconnecting from the server.")
        client_socket.close()

if __name__ == "__main__":
    start_client()

