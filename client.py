import socket
import threading
import sys
import os

Host = 'localhost'
Port = 1234  # Any port bethween 0 and 65535


def listen_for_messages(client):
    while True:

        data = client.recv(2048).decode('utf-8')
        if data != "":

            # check if data has : in it
            if ":" not in data:
                print(data)
                continue
            else:
                message = data.split(":")
                print(message[0] + ": " + message[1])
        else:
            print("Empty message received.")
            break

def send_file_to_server(client):
    # Get the file name from the command line input
    file_name = input("Enter the file name: ")

    # Check if the file exists
    if not os.path.exists(file_name):
        print(f"File '{file_name}' not found.")
        return

    # Send the file to all connected clients
    try:
        with open(file_name, 'rb') as file:
            data = file.read()
            client.sendall(data)
        print(f"File '{file_name}' sent to server.")
    except Exception as e:
        print(f"Error sending file to clients: {e}")
    


def send_message_to_server(client):
    while True:
        message = input("Message: ")
        if message != "":
            if message == "send_file":
                client.sendall(message.encode('utf-8'))
                send_file_to_server(client)
                continue
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
    threading.Thread(target=send_message_to_server, args=(client,)).start()

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
