import socket

HOST = 'www.google.com'
PORT = 80

address = socket.gethostbyname(HOST)
s = socket.create_connection((address, PORT))

s.sendall(b'GET / HTTP/1.1\r\n\r\n')
s.shutdown(socket.SHUT_WR)

received = b''
while True:
    b = s.recv(4096)
    received += b
    if not b: break

s.close()
print(received)
