import socket, multiprocessing

LOCAL_HOST = 'localhost'
LOCAL_PORT = 8001
REMOTE_HOST = 'www.google.com'
REMOTE_PORT = 80

local_address = socket.gethostbyname(LOCAL_HOST)
remote_address = socket.gethostbyname(REMOTE_HOST)

def handle_request(conn, addr):
    outside = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    outside.connect((remote_address, REMOTE_PORT))
    while True:
        data = conn.recv(4096)
        outside.sendall(data)
        if not data: break
    outside.shutdown(socket.SHUT_WR)
    while True:
        data = outside.recv(4096)
        conn.sendall(data)
        if not data: break
    outside.close()
    conn.shutdown(socket.SHUT_WR)
    conn.close()

def main():
    multiprocessing.set_start_method('fork')
    with socket.socket() as inside:
        inside.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        inside.bind((local_address, LOCAL_PORT))
        inside.listen(1)

        while True:
            conn, addr = inside.accept()
            p = multiprocessing.Process(
                target=handle_request, args=(conn, addr))
            p.start()

main()
