import socket
import pickle
import RSA as rsa
import random
import math


keys = {
    # "Alice": {"e": 65537, "n": 235711131719},
    "Bob": {"e": 2123, "n": 118403}
}


    
def pka_server():
    e = 2123
    n = 118403
    d = 12939
    

    print(f"Public key PKA(e, n): ({e}, {n})")
    print(f"Private key PKA(d, n): ({d}, {n})")
    pka = {
        "e": e,
        "n": n
    }



    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"PKA berjalan di {host}:{port}")

    
    client_socket, addr = server_socket.accept()
    print(f"Menerima koneksi dari {addr}")

    # Menerima request ID (A/B)
    client_id = client_socket.recv(1024).decode('utf-8')
    print(f"Permintaan kunci publik untuk: {client_id}")

    # Kirim kunci publik yang diminta
    if client_id in keys:
        keys_pka = rsa.encrypt_rsa(keys[client_id], d, n)
        print(f"keys = {keys_pka}")
        client_socket.send(pickle.dumps(keys_pka))
    else:
        client_socket.send(b"ID tidak dikenal")

    client_socket.close()


pka_server()
