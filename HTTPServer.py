import socket
import sys
import os

request = ['','','']
requestErrors = [
    'ERROR -- Invalid Method token.\n',
    'ERROR -- Invalid Absolute-Path token.\n',
    'ERROR -- Invalid HTTP-Version token.\n',
    'ERROR -- Spurious token before CRLF.\n'
]

def main():

    args = sys.argv
    port = int(args[1])

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", port))
        server_socket.listen(1)
    except OSError as e:
        print('Connection error')
        return

    while True:
        (client_socket, address) = server_socket.accept()
        print("Connection established with {}".format(str(address)))

        line = client_socket.recv(1024)
        line = line.decode('ascii')

        resp = line
        resp += handleHandleLine(line)

        client_socket.send(resp.encode('ascii'))

def handleHandleLine(line):
    currTokenIdx = 0
    resp = ''

    if line[0] in ' \f\n\r\t\v':
        return requestErrors[0]

    arr = line.split(' ')

    for elt in arr:
        elt = elt.strip()
        if elt == '': continue
        rv = checkSubstring(currTokenIdx, elt)
        currTokenIdx += 1
        if rv < 0:
            break

    if rv != 0:
        return requestErrors[rv]

    if currTokenIdx == 3:
        resp += 'Method = ' + request[0] + '\n'
        resp += 'Request-URL = ' + request[1] + '\n'
        resp += 'HTTP-Version = ' + request[2] + '\n'

        if request[1].split('.')[-1].lower() not in ['txt', 'html', 'htm']:
            return '501 Not Implemented: ' + request[1] + '\n'

        try:
            path = os.getcwd() + request[1]
            file = open(request[1][1:].lower(), 'r')
            for line in file:
                resp += line
            return resp
        except FileNotFoundError:
            return '404 Not Found: ' + request[1] + '\n'
        except IOError as e:
            return 'ERROR: ' + e + '\n'
    else: return requestErrors[currTokenIdx-4]

def validFilepath(token):
    if token[0] != '/':
        return -3
    token = token.lower()
    #pdb.set_trace()
    for char in token:
        if char not in 'qwertyuiopasdfghjklzxcvbnm1234567890._/': return -3
    return 0

def validHTTPVersion(token):
    #pdb.set_trace()
    arr = token.split('/')
    if len(arr) != 2 or arr[0] != 'HTTP': return -2
    arr = arr[1].split('.')
    if len(arr) != 2: return -2
    for elt in arr:
        for char in elt:
            if char not in '1234567890': return -2
    return 0

def checkSubstring(tokenIdx, token):
    global request
    rv = 0
    if tokenIdx == 0 and token != 'GET': rv = -4
    elif tokenIdx == 1: rv = validFilepath(token)
    elif tokenIdx == 2: rv = validHTTPVersion(token)
    elif tokenIdx > 2: rv = -1

    if rv == 0: request[tokenIdx] = token
    return rv

if __name__ == "__main__":
    main()
