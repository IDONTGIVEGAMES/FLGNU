import socket
import threading

HOST = input("Enter server IP (e.g., 127.0.0.1): ")
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print("\n" + data.decode())
        except:
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Room ID
        data = s.recv(1024).decode()
        room_id = input(data)
        s.sendall(room_id.encode())

        # Nickname
        data = s.recv(1024).decode()
        nickname = input(data)
        s.sendall(nickname.encode())

        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        while True:
            msg = input()
            if msg.lower() == "/exit":
                break
            s.sendall(msg.encode())

main()
