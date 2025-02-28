import socket
import time
import random

# Server configurations
HOST = '192.168.1.190'  # Update with your actual server IP
PORT = 12345

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("[Client] Connected to the server")

    buffer = ""
    while True:
        # Receive the server's current data type request (even or odd)
        buffer += client_socket.recv(1024).decode()
        
        # Process each state line separately
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            state = line.strip()
            print(f"[Client] Received server state: {state}")

            # Generate random data based on the server's state
            if state == 'even':
                data = random.choice([2, 4, 6, 8])
            elif state == 'odd':
                data = random.choice([1, 3, 5, 7, 9])
            else:
                print("[Client] Unknown state received, retrying...")
                continue

            # Send the data to the server
            client_socket.sendall(str(data).encode())
            print(f"[Client] Sent {state} data: {data}")

            # Wait 2 seconds before sending the next data
            time.sleep(2)

    client_socket.close()
    print("[Client] Disconnected from server")

if __name__ == "__main__":
    connect_to_server()

