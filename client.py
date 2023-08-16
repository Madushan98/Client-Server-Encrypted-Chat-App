import socket
import threading
import sys
import os
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
from datetime import datetime

Host = "13.233.250.226"
Port = 9999  # Any port bethween 0 and 65535

def add_message_to_message_box(message):
    message_box.config(state=tk.NORMAL)

    # Define colors for chat bubbles
    bubble_bg_color = OCEAN_BLUE
    bubble_text_color = WHITE

    # Create a custom tag for the chat bubble style
    message_box.tag_configure("bubble", background=bubble_bg_color, foreground=bubble_text_color, justify="left", wrap="word", spacing2=5)

    # Get the current date and time
    current_time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # Add the message to the message box with chat bubble styling
    message_box.insert(tk.END, "\n", ("bubble",))
    message_box.insert(tk.END, message + "\n", ("bubble",))
    
    # Add the current time in a smaller font inside the bubble
    message_box.insert(tk.END, f"{current_time}\n", "small")

    # Configure small font style for the current time inside the bubble
    message_box.tag_configure("small", font=("Helvetica", 10), foreground="gray")

    message_box.config(state=tk.DISABLED)
    message_box.see(tk.END)



def connect_to_server():
    try:
        client.connect((Host, Port))
        #print("Connected to server on port: %s" % Port)
        add_message_to_message_box("[SERVER] Connected to the server")
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

    threading.Thread(target=listen_for_messages,
                     args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        message_box.showerror("Message is empty", "Message is empty") 
        



DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1824'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT=('Helvetica', 17)
BUTTON_FONT = ('Helvetica', 15)
SMALL_FONT = ('Helvetica', 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = tk.Tk()
root.geometry("600x520")
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
            if " : " not in data:
                add_message_to_message_box(data)
                continue
            else:
                message = data.split(" : ")
                add_message_to_message_box(message[0] + " : " + message[1])
        else:
            message_box.showerror("Error", "Empty message received from server")
            break

def send_file_to_server(client):
    # Get the file name from the command line input
    file_name = input("Enter the file name: ")

    # Check if the file exists
    if not os.path.exists(file_name):
        add_message_to_message_box(f"File '{file_name}' not found.")
        return

    # Send the file to all connected clients
    try:
        with open(file_name, 'rb') as file:
            data = file.read()
            client.sendall(data)
        add_message_to_message_box(f"File '{file_name}' sent to server.")
    except Exception as e:
        add_message_to_message_box(f"Error sending file to clients: {e}")
    


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
            add_message_to_message_box("Message is empty")
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
