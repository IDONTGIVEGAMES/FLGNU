import socket
import threading

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345

clients = {}  # room_id: list of (conn, nickname)

def broadcast(room_id, message, sender_conn):
    for conn, _ in clients[room_id]:
        if conn != sender_conn:
            try:
                conn.sendall(message.encode())
            except:
                pass  # Client might be disconnected

def handle_client(conn, addr):
    try:
        conn.sendall("Enter room ID: ".encode())
        room_id = conn.recv(1024).decode().strip()

        conn.sendall("Enter your nickname: ".encode())
        nickname = conn.recv(1024).decode().strip()

        if room_id not in clients:
            clients[room_id] = []

        clients[room_id].append((conn, nickname))

        welcome = f"[{nickname} has joined room '{room_id}']"
        print(welcome)
        broadcast(room_id, welcome, conn)

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = f"{nickname}: {data.decode()}"
            print(message)
            broadcast(room_id, message, conn)
    except:
        pass
    finally:
        # Remove client from room
        for rid in clients:
            clients[rid] = [c for c in clients[rid] if c[0] != conn]
        conn.close()

def start_server():
    print(f"Server starting on port {PORT}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

start_server()
