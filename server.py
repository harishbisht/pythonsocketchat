# Tcp Chat server
 
import socket, select

PAIRED_LIST = []
WAITING = []
CONNECTION_LIST = []

def get_paired_member(sock):
    l =  [socket for socket in PAIRED_LIST if socket[0] == sock or socket[1] == sock]
    if l:
        if l[0][0] == sock:
            return l[0][1]
        else:
            return l[0][0]
    else:
        return []

def delete_pairings(sock):
    l =  [socket for socket in PAIRED_LIST if socket[0] == sock or socket[1] == sock]
    if l:
        l = l.pop()
        PAIRED_LIST.remove(l)
    pass

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def new_connection(sock):
    if WAITING:
        othersock = WAITING.pop()
        PAIRED_LIST.append((othersock,sock))
        send_message(sock,"You are now connected")
        send_message(othersock,"You are now connected")
    else:
        WAITING.append(sock)
        send_message(sock,"Waiting for other user")
    CONNECTION_LIST.append(sock)

    pass

def connection_closed(sock):
    pairedsocket = get_paired_member(sock)
    if pairedsocket:
        message = "Stranger is offline"
        try:
            pairedsocket.send(message)
        except Exception,e:
            pass
        delete_pairings(sock)
    pass



def send_message_to_paired(sock,message):
    socket = get_paired_member(sock)
    if socket:
        send_message(socket,message)
    else:
        send_message(sock,"Not Connected")
    pass


def send_message(sock,message):
    try :
        sock.send(message)
    except Exception,e:
        print e
        connection_closed(sock)




if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip = get_ip()
    server_socket.bind((ip, PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        try:
            read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

            for sock in read_sockets:
                #New connection
                if sock == server_socket:
                    # Handle the case in which there is a new connection recieved through server_socket
                    sockfd, addr = server_socket.accept()
                    new_connection(sockfd)
                #Some incoming message from a client
                else:
                    # Data recieved from client, process it
                    try:
                        data = sock.recv(RECV_BUFFER)
                        if data:
                            send_message_to_paired(sock,data)
                            # broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                    except Exception,e:
                        connection_closed(sock)
                        continue
        except:
            pass
    server_socket.close()