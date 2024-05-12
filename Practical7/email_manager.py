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

# send emails function
def send_email():
    # Prompt user for email details
    receiver = input("Receiver's email: ")
    subject = input("Subject: ")
    message = input("Message: ")
    bcc = input("BCC: ")

    # Email sender details
    sender = MY_EMAIL
    mailserver = ("sandbox.smtp.mailtrap.io", 2525)

    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(mailserver)

    # Authenticate with base64 encoding
    base64_str = ("\x00"+USERNAME+"\x00"+PASSWORD).encode()
    base64_str = base64.b64encode(base64_str)
    auth_msg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
    client_socket.send(auth_msg)
    recv_auth = client_socket.recv(1024)
    print(recv_auth.decode())

    # Message to send
    mail_from = f"MAIL FROM: <{sender}>\r\n"
    client_socket.send(mail_from.encode())
    recv_mail_from = client_socket.recv(1024)
    print("After MAIL FROM command: "+recv_mail_from.decode())

    # Send RCPT TO command
    rcpt_to = f"RCPT TO: <{receiver}>\r\n"
    client_socket.send(rcpt_to.encode())
    recv_rcpt_to = client_socket.recv(1024)
    print("Server: "+recv_rcpt_to.decode())

    # Send DATA command
    data = "DATA\r\n"
    client_socket.send(data.encode())
    print("Sent DATA command")
    recv_data = client_socket.recv(1024)
    print("Server: "+recv_data.decode())

    # Make email header
    to = f"To: {receiver}\r\n"
    fr = f"From: {sender}\r\n"
    bcc = f"Bcc: {bcc}\r\n"
    subject_header = f"Subject: {subject}\r\n"
    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    date_header = "Date: " + date + "\r\n\r\n"

    # Construct email
    email = to + fr + bcc + subject_header + date_header + message + "\r\n.\r\n"

    # Send email
    client_socket.send(email.encode())
    recv_email = client_socket.recv(1024)
    print("Server: "+recv_email.decode())

    # Quit
    quit_cmd = "QUIT\r\n"
    client_socket.send(quit_cmd.encode())
    recv_quit = client_socket.recv(1024)
    print(recv_quit.decode())

    # Close connection
    client_socket.close()

    print("Email sent successfully!")

# Main function
def main():
    while True:
        user_input = input("What would you like to do? (get emails, send email, exit): ")
        if user_input == "get emails":
            get_emails()
        elif user_input == "send email":
            send_email()
        elif user_input == "exit":
            break
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()
