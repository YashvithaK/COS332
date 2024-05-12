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