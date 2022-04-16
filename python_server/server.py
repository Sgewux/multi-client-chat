import socket
from concurrent.futures import ThreadPoolExecutor

from user import User

HOST = '192.168.1.11' # here goes you host private ip adress, this may be different for you
PORT = 8080

# AF_INET works for stablish connections via host:port with ipv4
# SOCK_STREAM sets TCP as transfer protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT)) #  Bind the socket to a ip and port

list_of_users = []

def send_to_all_but_me(me, data):
    '''
    Utility function to send a message to
    all the active users but the one who was passed
    as parameter.
    '''
    global list_of_users
    for u in list_of_users:
        if u != me:  # If is not the same user
            u.sendall(data)


def handle_usr_connection(server):
    '''
    Function for handling user connection:
    
    -Wait for a client to connect.
    -Creates a User obj with username and proxy object
    -Adds the User obj to a global list of users.
    -Wait the client for sending a message.
    -Once message is sent:
        - iterates through the global list of users
        - sends the message to all the users in the server but
          the one who sent the message
    -If the received data is a "falsy" value, client has closet its connection,
     therefore:
        -removes the User obj from the global list of users
         so as to avoid sending messages to that socket because will be closed.
        -notifies all the other users that a user left the chat.
        -breaks the loop.
    
    Note: All messages have \n added at the end, this was made in order to
          achieve compatibility with Java client.
    '''
    global list_of_users

    conn, addr = server.accept()
    with conn:
        username = conn.recv(4096)
        user = User(username.decode('utf-8'), conn) 
        log = f'{user.username} joined! \n'
        send_to_all_but_me(user, log.encode('utf-8'))
        list_of_users.append(user)  # Append user to list_of_users
        while True:
            data = conn.recv(4096)
            if data: # If client socket was closed the recieved data will be falsy (but it still recieves data)
                data = user.username  + ': ' + data.decode('utf-8') + '\n'  # Username: message
                send_to_all_but_me(user, data.encode('utf-8'))
            else:
                # Gotta remove the socket obj of the former usr (which will be closed) to avoid broken pipe
                list_of_users.remove(user)
                leaving_message = f'{user.username} left the chat. \n'
                send_to_all_but_me(user, leaving_message.encode('utf-8'))
                break


def main():
    num_of_clients = input('Number of clients: ')
    num_of_clients = int(num_of_clients)
    with server:
        server.listen()
        print('Server started.')
        with ThreadPoolExecutor(max_workers=num_of_clients) as executor:
           server_socket_objects = [server for i in range(num_of_clients)]
           executor.map(handle_usr_connection, server_socket_objects)
    print('Server instance finished')


if __name__ == '__main__':
    main()