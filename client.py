import socket
import threading
import sys
import os
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb

Host = 'localhost'
Port = 9999  # Any port bethween 0 and 65535

def add_message_to_message_box(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + "\n")
    message_box.config(state=tk.DISABLED)

def connect_to_server():
    try:
        client.connect((Host, Port))
        #print("Connected to server on port: %s" % Port)
        add_message_to_message_box("Connected to the server")
        #communicate_to_server(client)

    except:
        message_box.showerror("unable to connect to server", f"Unable to connect to server {Host}:{Port}")
        #print("Connection failed. Error : " + str(sys.exc_info()))
        exit(0)
        #print("Connecting to server...")

    username = username_textbox.get()
    if username != "":
        client.sendall(username.encode('utf-8'))

    else:
        message_box.showerror("Username is empty", "Username is empty")
        sys.exit()
    threading.Thread(target=listen_for_messages,
                     args=(client, )).start()
    threading.Thread(target=send_message_to_server, args=(client,)).start()

def send_message():
    print("Sending message...")


DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1824'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT=('Helvetica', 17)
BUTTON_FONT = ('Helvetica', 15)
SMALL_FONT = ('Helvetica', 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False,False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter Username:", bg=DARK_GREY, fg=WHITE, font=FONT)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=DARK_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect_to_server)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)
 
message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = tkst.ScrolledText(middle_frame, bg=MEDIUM_GREY, fg=WHITE, font=SMALL_FONT, width=67, height=23)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages(client):
    while True:

        data = client.recv(2048).decode('utf-8')
        if data != "":

            # check if data has : in it
            if ":" not in data:
                add_message_to_message_box(data)
                continue
            else:
                message = data.split(":")
                add_message_to_message_box(message[0] + ": " + message[1])
        else:
            message_box.showerror("Error", "Empty message received from server")
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


#def communicate_to_server(client):

    

    #while True:
        #data = client.recv(2048).decode('utf-8')
        #if data == "":
        #    break
        #print(data)


def main():

    root.mainloop() 

    
   


if __name__ == '__main__':
    main()
