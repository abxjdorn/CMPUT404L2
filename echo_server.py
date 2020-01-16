import time, socket, multiprocessing

HOST = 'localhost'
PORT = 8001

def handle_request(conn, addr):
    message = b''
    while True:
        data = conn.recv(4096)
        time.sleep(0.5)
        message += data
        conn.sendall(data)
        if not data: break
    print(message)
    conn.close()

def main():
    multiprocessing.set_start_method('fork')
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            print(conn, addr)
            p = multiprocessing.Process(
                target=handle_request, args=(conn, addr))
            p.start()

main()
