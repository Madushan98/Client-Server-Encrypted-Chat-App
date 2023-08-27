import socket
import threading
import sys
import rsa

public_key, private_key = rsa.newkeys(1024)
client_public_keys = {}

Host = 'localhost'
Port = 9999  # Any port bethween 0 and 65535

clients = []


def listen_for_messages(client, username):
    while 1:
        response = rsa.decrypt(client.recv(1024) , private_key).decode('utf-8')  
        if response != "":
            if response == "send_file":
                file_data = client.recv(512).decode('utf-8')
                file = open("new_file", "w")
                file.write(file_data)
                file.close()
                print("File received")
                continue
            message = username + " : " + response
            send_message_to_all(message, client)
        else:
            print("Message is empty")


def send_message_to_client(client, data):
    recipient_public_key = client_public_keys[client]
    print(recipient_public_key)
    client.sendall(rsa.encrypt(str(data).encode('utf-8'), recipient_public_key))


def send_message_to_all(data, client):
    for user in clients:
        if user[1] != client:
            send_message_to_client(user[1], data)
        else:
            send_message_to_client(user[1], "[You] :" + data)   


def client_handler(client,username):
    while 1:
        if username != "":
            clients.append((username, client))
            #print(client)
            send_message_to_all(username + " has joined the chat", client)
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
        client.send(public_key.save_pkcs1("PEM"))
        client_public_key = rsa.PublicKey.load_pkcs1(client.recv(1024))
          
        client_username = client.recv(1024).decode('utf-8')
        
        print("Got connection from", address)
        print("Username: ", client_username)
        
        client_public_keys[client] = client_public_key
      
        threading.Thread(target=client_handler, args=(client,client_username)).start()


if __name__ == '__main__':
    main()
