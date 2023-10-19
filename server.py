import socket
import threading

def handle_client(client_socket, client_address, clients):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == "exit":
                break

            # Отправить сообщение от одного клиента всем остальным клиентам
            for client in clients:
                if client != client_socket:
                    client.send(f"Client {client_address}: {message}".encode())
        except ConnectionResetError:
            break

    client_socket.close()
    clients.remove(client_socket)
    print(f"Client {client_address} has disconnected.")

    # Отправить сообщение о выходе клиента всем остальным клиентам
    for client in clients:
        client.send(f"Client {client_address} has disconnected.".encode())

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 1234))
    server_socket.listen(5)
    print("Server started. Waiting for connections...")

    clients = []

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(f"Client {client_address} has connected.")

        # Запустить поток для обработки клиента
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clients))
        client_thread.start()

if __name__ == "__main__":
    start_server()