import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
HOST = '192.168.1.11'
PORT = 8080

# AF_INET works for stablish connections via host:port with ipv4
# SOCK_STREAM sets TCP as transfer protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT)) #  Bind the socket to a ip and port

list_of_users = []

def get_data_from_conn(server):
    global list_of_users

    conn, addr = server.accept()
    list_of_users.append(conn)
    with conn:
        print(f'{addr} joined!')
        while True:
            data = conn.recv(4096)
            if data: # If client socket was closed the recieved data will be falsy (but it still recieves data)
                for u in list_of_users:
                    if u != conn:  # If is not the same conn
                        u.sendall(data)
            else:
                break


if __name__ == '__main__':
    with server:
        server.listen()
        user1 = threading.Thread(target=get_data_from_conn, args=(server,))
        user2 = threading.Thread(target=get_data_from_conn, args=(server,))
        user1.start()
        user2.start()
