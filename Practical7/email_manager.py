import socket 
import base64
import time

# Using Mailtrap to send and read emails
USERNAME = "255a042f522676"
PASSWORD = "d200ffffe0a2a0"
MY_EMAIL = input("Please enter your email: ")

# Creating a client socket
def create_client_socket(mailserver):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(mailserver)

    # Authenticate with username and password using base64 encoding
    credentials = f"{USERNAME}\0{USERNAME}\0{PASSWORD}".encode()
    encoded_credentials = base64.b64encode(credentials)
    auth_msg = "AUTH PLAIN ".encode() + encoded_credentials + "\r\n".encode()
    client_socket.send(auth_msg)
    recv_auth = client_socket.recv(1024)
    print(recv_auth.decode())

    return client_socket

# get emails function
def get_emails():
    global USERNAME, PASSWORD, MY_EMAIL

    mailserver = ("pop3.mailtrap.io", 1100)
    clientSocket = create_client_socket(mailserver)

    stat = "STAT\r\n"
    print(stat)
    clientSocket.send(stat.encode())
    recv_stat = clientSocket.recv(1024)
    print(recv_stat.decode())

    list_cmd = "LIST\r\n"
    print(list_cmd)
    clientSocket.send(list_cmd.encode())
    recv_list = clientSocket.recv(1024)
    print(recv_list.decode())
    recv_list = clientSocket.recv(1024)
    print(recv_list.decode())

    while True:
        index = input("Please enter the mail you would like to read (or stop): ")

        if index == "stop":
            break

        retr = f"RETR {index}\r\n"
        print(retr)
        clientSocket.send(retr.encode())

        mail = b""
        while True:
            mail_chunk = clientSocket.recv(1024)
            mail += mail_chunk
            if mail_chunk[-5:] == b"\r\n.\r\n":
                break
        
        mail_text = mail.decode()

        # Check for BCC warning
        if f"Bcc: {MY_EMAIL}" in mail_text:
            print('\033[93m' + "[BCC Warning] " + mail_text + '\033[0m')
        else:
            print(mail_text)
    
    quit_cmd = "QUIT\r\n"
    clientSocket.send(quit_cmd.encode())
    recv_quit = clientSocket.recv(1024)
    print(recv_quit.decode())

    clientSocket.close()