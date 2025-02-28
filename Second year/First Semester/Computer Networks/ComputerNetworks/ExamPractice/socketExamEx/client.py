import socket
import random
import time

# Server settings
SERVER_IP = '172.20.10.11'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    while True:
        # Receive the demand type from the server
        demand_type = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Server demands a {demand_type} number.")

        # Generate a number based on the demand
        if demand_type == "positive":
            number = random.randint(1, 10)
        elif demand_type == "negative":
            number = -random.randint(1, 10)
        else:
            print("Received unknown command. Disconnecting.")
            break

        # Send the number to the server
        client_socket.sendall(str(number).encode())
        print(f"Sent: {number}")

        # Wait before the next communication cycle
        time.sleep(1)

    client_socket.close()

if __name__ == "__main__":
    main()

