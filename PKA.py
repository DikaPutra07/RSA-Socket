import socket
import pickle
import RSA as rsa
import random
import math, json

alice = {
    "e": 543059,
    "n": 730801
}

bob = {
    "e": 2123,
    "n": 118403
}



def pka_server():
    e=17
    n=3233
    d=2753   

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

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Menerima koneksi dari {addr}")

        client_id = client_socket.recv(1024).decode('utf-8')
        print(f"Permintaan kunci publik untuk: {client_id}")

        if client_id == "Alice":
            alice_dumps = json.dumps(alice)
            print(f"alice dumps = {alice_dumps}")
            keys_pka = rsa.encrypt_rsa(alice_dumps, d, n)
            print(f"keys = {keys_pka}")
        elif client_id == "Bob":
            bob_dumps = json.dumps(bob)
            print(f"bob dumps = {bob_dumps}")
            print(f"type bob dumps = {type(bob_dumps)}")
            keys_pka = rsa.encrypt_rsa(bob_dumps, d, n)
            print(f"keys = {keys_pka}")
        
        print(f"keys dumps = {keys_pka}")
        client_socket.send(pickle.dumps(keys_pka))
        
        client_socket.close()


pka_server()
