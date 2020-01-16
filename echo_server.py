import time, socket

HOST = 'localhost'
PORT = 8001

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(2)

    while True:
        conn, addr = s.accept()
        print(conn, addr)
        message = b''
        while True:
            data = conn.recv(4096)
            time.sleep(0.5)
            message += data
            conn.sendall(data)
            if not data: break
        print(message)
        conn.close()
