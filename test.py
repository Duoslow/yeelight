import socket
while True:
    host = '192.168.1.2'
    port = 55443                   # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(b'{"id":1,"method":"set_power","params":["on"]}')
    data = s.recv(1024)
    print('Received', repr(data))
    s.close()