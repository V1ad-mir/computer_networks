import socket
import threading

def receive_messages(client_socket):
    while True:
        response = client_socket.recv(1024).decode()
        print(f"Received response: {response}")

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1234))
    print("Connected to server.")

    # Запустить поток для приема сообщений от сервера
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        client_socket.send(message.encode())
        if message == "exit":
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()