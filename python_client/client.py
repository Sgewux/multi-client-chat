import socket
import threading

SERVER_HOST = '192.168.1.11' # here goes you host private ip adress, this may be different for you
SERVER_PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def look_for_messages(client):
    '''
    Function for wait messages sent by the server:
        - Other user messages.
        - Server info messages.
    '''
    while True:
        message = client.recv(4096).decode('utf-8')
        if message:
            print(f'{message}')
        else:
            break


def send_message(client):
    '''
    Function waits for an input and sends that message
    to the server.

    Note: We add two blanks at the input's beggining, thus to help the server
          to work with java clients. This blank spaces will be removed by the server.
    '''
    while True:
        usr_input = '  ' + input()
        usr_input = usr_input.encode('utf-8')

        client.sendall(usr_input)  # sending actual message


def main():
    with client:
        try:
            client.connect((SERVER_HOST, SERVER_PORT))
            username = input('Write your username: ')
            client.sendall(username.encode('utf-8'))
            print_messages = threading.Thread(
                target=look_for_messages, 
                args=(client,)
            )
            send_messages = threading.Thread(
                target=send_message,
                args=(client,)
            )

            print_messages.start()
            send_messages.start()

            # Joining threads in order to keep the client socket alive
            print_messages.join()
            send_messages.join()

        except KeyboardInterrupt:
            print('\n\nGood Bye!')


if __name__ == '__main__':
    main()