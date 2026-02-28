import socket
import threading
from crypto_utils import *

TCP_PORT = 5000
UDP_PORT = 5001
BUFFER_SIZE = 4096				#bigger buffer for receiving AES keys and encrypted messages

clients = {}   					#server saves the AES key for each client

private_key, public_key = generate_rsa_keys()
public_bytes = serialize_public_key(public_key)


def handle_client(conn, addr):
    print(f"[TCP] Client connected: {addr}")

    conn.send(public_bytes)				#server sends the public RSA key; will be used by client for encrypting the AES key

    encrypted_aes = conn.recv(BUFFER_SIZE)
    aes_key = rsa_decrypt(private_key, encrypted_aes)
    clients[conn] = aes_key

    print(f"[INFO] Key received from {addr}")

    while True:						#while the client is connected
        try:
            data = conn.recv(BUFFER_SIZE)
            if not data:				#not data == b''
                break

            message = aes_decrypt(aes_key, data)
            print(f"[{addr[0]}] {message}")

            broadcast(message, conn)

        except Exception as e:				#catches any error that might occur in the while and displays it
            print(f"[ERROR] {addr}: {e}")
            break

    print(f"[TCP] Client disconnected: {addr}")
    del clients[conn]
    conn.close()


def broadcast(message, source_conn):			#source_conn = TCP socket of the sender client		
    for conn, key in clients.items():
        if conn != source_conn:
            try:
                encrypted = aes_encrypt(key, message)
                conn.send(encrypted)
            except:
                pass

#used for server discovery; let's the client know that server is online
def udp_listener():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("0.0.0.0", UDP_PORT))

    while True:						#UDP runs permanently, at the same time with the TCP, in a different thread
        data, addr = udp_sock.recvfrom(1024)
        udp_sock.sendto(b"SERVER_ONLINE", addr)


def start_tcp_server():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind(("0.0.0.0", TCP_PORT))
    tcp_sock.listen()					#allows server to start waiting and accepting clients

    print("[TCP] Server open...")

    while True:
        conn, addr = tcp_sock.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()			#creates a thread for the client


if __name__ == "__main__":
    threading.Thread(target=udp_listener, daemon=True).start()
    start_tcp_server()
