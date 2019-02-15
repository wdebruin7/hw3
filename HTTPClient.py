import socket
import sys

args = sys.argv

host = 'comp431sp19.cs.unc.edu'
port = int(args[1])

for line in sys.stdin:

    try:
        print('attempting to connect...')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        print('connected!')

        s.sendall(line.encode('ascii'))
        msg = s.recv(1024)
        s.close()
        print ("Recieved: "+ msg.decode('ascii'), end='')
    except OSError as e:
        print('Connection error')
