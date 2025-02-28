import socket

# Server configurations
HOST = '127.0.0.1'  # Server IP address
PORT = 12345  # Server port

# Main function to connect to the server
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[Client] Connected to server at {HOST}:{PORT}")

    try:
        while True:
            # Sending data to the server
            message = input("[Client] Enter message to send (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                print("[Client] Disconnecting from server.")
                break

            client_socket.sendall(message.encode('utf-8'))

            # Receiving response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"[Client] Server response: {response}")
    except Exception as e:
        print(f"[Client] Error: {e}")
    finally:
        client_socket.close()
        print("[Client] Connection closed.")

if __name__ == "__main__":
    connect_to_server()

