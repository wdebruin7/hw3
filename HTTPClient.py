import socket
import sys

args = sys.argv

host = socket.gethostname()
port = int(args[1])


for line in sys.stdin:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(line.encode('ascii'))


    msg = s.recv(1024)
    s.close()
    print ("Recieved: "+ msg.decode('ascii'), end='')
