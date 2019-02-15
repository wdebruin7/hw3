import socket
import sys

args = sys.argv

if (len(args) >= 3) and (args[2] == '-l'):
    host = socket.gethostname()
else:
    host = 'comp431sp19.cs.unc.edu'

port = int(args[1])

for line in sys.stdin:

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        s.sendall(line.encode('utf-8'))
        msg = s.recv(1024)
        s.close()
        print (msg.decode('utf-8'), end='')
    except OSError as e:
        print('Connection error')
