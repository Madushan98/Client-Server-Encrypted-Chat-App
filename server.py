import socket
import threading
import sys

Host = 'localhost'
Port = 1234  # Any port bethween 0 and 65535

clients = []


def listen_for_messages(client, username):
    while 1:
        response = client.recv(2048).decode('utf-8')
        if response != "":
            message = username + " : " + response
            send_message_to_all(message, client)
        else:
            print("Message is empty")


def send_message_to_client(client, data):
    client.sendall(data.encode('utf-8'))


def send_message_to_all(data, client):
    for user in clients:
        if user[1] != client:
            send_message_to_client(user[1], data)


def client_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != "":
            clients.append((username, client))
            break
        else:
            print("Username is empty")
            break

    threading.Thread(target=listen_for_messages,
                     args=(client, username,)).start()


def main():
    # Creating a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((Host, Port))
        print("Server started on port: %s" % Port)

    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    server.listen(5)  # Now wait for client connection.

    while True:
        client, address = server.accept()
        print("Got connection from", address)
        threading.Thread(target=client_handler, args=(client,)).start()

    while True:
        client, address = server.accept()  # Establish connection with client.
        print("Got connection from", address)


if __name__ == '__main__':
    main()
