import socket, multiprocessing

LOCAL_ADDRESS = 'localhost'
LOCAL_PORT = 8001
REMOTE_ADDRESS = 'www.google.com'
REMOTE_PORT = 80

def handle_request(conn, addr):
    outside = socket.create_connection((REMOTE_ADDRESS, REMOTE_PORT))
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
        inside.bind((LOCAL_ADDRESS, LOCAL_PORT))
        inside.listen(1)

        while True:
            conn, addr = inside.accept()
            p = multiprocessing.Process(
                target=handle_request, args=(conn, addr))
            p.start()

main()
