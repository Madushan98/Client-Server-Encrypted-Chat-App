import socket
import threading
import sys

Host = 'localhost'
Port = 1234  # Any port bethween 0 and 65535


def listen_for_messages(client):
    while True:
        data = client.recv(2048).decode('utf-8')
        if data != "":
            message = data.split(":")
            print(message[0] + ": " + message[1])
        else:
            print("Empty message received.")
            break
        


def send_message_to_server(client):
    while True:
        message = input("Message: ")
        if message != "":
            client.sendall(message.encode('utf-8'))
        else:
            print("Message is empty")
            break   
        


def communicate_to_server(client):

    username = input("Enter your username: ")
    if username != "":
        client.sendall(username.encode('utf-8'))

    else:
        print("Username is empty")
        sys.exit()
    threading.Thread(target=listen_for_messages,
                     args=(client, )).start()
    send_message_to_server(client)

    while True:
        data = client.recv(2048).decode('utf-8')
        if data == "":
            break
        print(data)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((Host, Port))
        print("Connected to server on port: %s" % Port)
        communicate_to_server(client)

    except:
        print("Connection failed. Error : " + str(sys.exc_info()))
        sys.exit()


if __name__ == '__main__':
    main()
