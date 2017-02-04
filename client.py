# telnet program example
import socket, select, string, sys
import json

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

#main function
if __name__ == "__main__":
     
    # if(len(sys.argv) < 3) :
    #     print 'Usage : python telnet.py hostname port'
    #     sys.exit()
     
    # host = sys.argv[1]
    # port = int(sys.argv[2])
    host = 'localhost'
    port= 5000
    ip = get_ip()
    # ip = "54.86.13.221"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((ip, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages'
    prompt()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()
                # s.close()

                