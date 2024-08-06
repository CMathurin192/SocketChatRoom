"""Written by Caleb Mathurin
   August 5, 2024,
   Written in PyCharm Community Edition 2024.1.1 in Python 3.12
   This is the code for my chat room using sockets. (It acts as both the client and server code depending
   on what you choose.)"""

#CM 8/5/24 - imports
import socket
import threading

#CM 8/5/24 - menu navigation variables
menu = "select_username"
run_once = True

#CM 8/5/24 - socket variables
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
client_socket = socket.socket()
clients = []

#CM 8/5/24 - client_send_message function
def client_send_message():
    message = input()
    client_socket.send(f"{client_username}: {message}".encode("utf-8"))

#CM 8/5/24 - client_recv_message function
def client_recv_message():
    while True:
        msg = client_socket.recv(1024).decode("utf-8")
        print(msg)

#CM 8/5/24 - server function
def server_handle_clients():
    client, address = server.accept()
    while True:
        text = client.recv(1024).decode("utf-8")
        print(text)
        clients.append(client)

#CM 8/5/24 - server_recv_message function (host)
def server_recv_message():
    while True:
        client, address = server.accept()
        msg = client.recv(1024).decode("utf-8")
        print(msg)

#CM 8/5/24 - server (host) send message
def server_send_message():
    message = input()
    clients[1].send(f"{client_username}: {message}".encode("utf-8"))


#CM 8/5/24 - introductory code
print("This is a chat room made using sockets in Python that can support up to 10 people in a room." + "\n")

#CM 8/5/24 - main while loop
while True:
    #CM 8/5/24 - have client select a username
    if menu == "select_username":
        client_username = input("Enter a username to represent yourself in a server (10 character maximum): ")
        if len(client_username) > 10:    # too long
            print("This username is too long." + "\n")
        elif len(client_username) <= 0:  # invalid (too short)
            print("This username is invalid." + "\n")
        else:                            # valid
            menu = "host_or_guest"

    #CM 8/5/24 - get client's server choice
    if menu == "host_or_guest":
        host_or_guest = input("To host a server, type \"host\". To join an existing server, type \"guest\": ")

        if host_or_guest == "host":
            print("You have selected the host role. Have your guests enter " + HOST + " to join your server.")
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((HOST, PORT))
            server.listen(1)
            clients.append(server)
            menu = "chat_room"
        elif host_or_guest == "guest":
            entered_host = input("You have selected the guest role. Enter a host's IP address to join their server: ")
            try:
                client_socket.connect((entered_host, PORT))
                client_socket.send(f"{client_username} has joined the chat room!".encode("utf-8"))
                menu = "chat_room"
            except:
                print("Connection to host failed. Please try again." + "\n")
        else:
            print("This is not a valid option. Please try again." + "\n")

    #CM 8/5/24 - chat_room events
    if menu == "chat_room":
        if run_once == True:
            print("\n" + "You are now in the chat room!" + "\n")
            run_once = False

        if host_or_guest == "host":
            server_handle_clients_thread = threading.Thread(target=server_handle_clients)
            server_handle_clients_thread.start()
            server_send_message()
            server_recv_message_thread = threading.Thread(target=server_recv_message)
            server_recv_message_thread.start()
        elif host_or_guest == "guest":
            client_send_message()
            client_recv_message_thread = threading.Thread(target=client_recv_message)
            client_recv_message_thread.start()

"""CM 8/5/24 - notes
   1. This chat room was originally going to support up to 10 people, which could easily be implemented, but
      I kept running into "ConnectionAbortedError: [WinError 10053] An established connection was aborted by the 
      software in your host machine" when trying to test with the 3rd chat room member. I could not find a solution
      to this error, so I decided to just keep it to two members.
   2. Use threads for functions that may have to wait for data to come in (Ex: waiting to be sent a message).
   3. Good experience I think?"""


