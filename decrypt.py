import socket, pickle, random, math, RSA as rsa, json


def permute(k, arr, n):
    return ''.join([k[arr[i] - 1] for i in range(n)])

def hex2bin(s):
    return bin(int(s, 16))[2:].zfill(len(s) * 4)

def bin2hex(s):
    integer_value = int(s, 2)
    hex_value = hex(integer_value)[2:].upper()
    hex_value = hex_value.zfill(len(s) // 4)
    return hex_value

def hex2str(hex_string):
    bytes_object = bytes.fromhex(hex_string)
    return bytes_object.decode("utf-8")

def bin2dec(binary):
    return int(str(binary), 2)

def dec2bin(num):
    return format(num, '04b')


def shift_left(k, nth_shifts):
    s = ""
    for i in range(nth_shifts):
        for j in range(1, len(k)):
            s = s + k[j]
        s = s + k[0]
        k = s
        s = ""
    return k

def xor(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))



initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]


exp_d = [
        32, 1, 2, 3, 4, 5, 4, 5,
        6, 7, 8, 9, 8, 9, 10, 11,
        12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21,
        22, 23, 24, 25, 24, 25, 26, 27,
        28, 29, 28, 29, 30, 31, 32, 1]


per = [16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25]


sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]


final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25]


def decrypt(pt, rkb, rk):
    pt = hex2bin(pt)
    pt = permute(pt, initial_perm, 64)

    print("After initial permutation", bin2hex(pt))
    print(" ------------------------------------------------------------ ")
    print("| Round      |  left      |  Right     |  round key (48-bit) |")
    print(" ------------------------------------------------------------ ")
    
    left = pt[0:32]
    right = pt[32:64]
    for i in range(0, 16):
        
        right_expanded = permute(right, exp_d, 48)
        xor_x = xor(right_expanded, rkb[i])
        sbox_str = ""
        for j in range(0, 8):
            row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin2dec(
                int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec2bin(val)

        
        sbox_str = permute(sbox_str, per, 32)

        
        result = xor(left, sbox_str)
        left = result

    
        if(i != 15):
            left, right = right, left
        if(i < 10):
            print("| Round ", i, "  | ", bin2hex(left),
				" | ", bin2hex(right), " | ", rk[i], "      | ")
        else:
            print("| Round ", i, " | ", bin2hex(left),
				" | ", bin2hex(right), " | ", rk[i], "      | ")
        
    
    combine = left + right
    cipher_text = permute(combine, final_perm, 64)
    
    return cipher_text



def ecb_decrypt(ciphertext, rkb, rk):
    plaintext = ""
    
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        decrypted_block = decrypt(block, rkb, rk)
        plaintext += decrypted_block
    
    return plaintext



def start_client():
    # RSA

    e = 2123
    d = 77171
    n = 118403

    print("Public Key Bob(e, n) : ", e, n)
    print("Private Key Bob(d, n) : ", d, n)


#   KONEK

    pka_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345
    pka_socket.connect((host, port))

    pka_socket.send(b"Alice")
    public_key_alice = pickle.loads(pka_socket.recv(2048))
    e_pka=17
    n_pka=3233
    
    public_key_alice = rsa.decrypt_rsa(public_key_alice, e_pka, n_pka)
    public_key_alice = json.loads(public_key_alice)
    pka_socket.close()


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12346
    server_socket.bind((host, port))

    server_socket.listen()

    print(f"Server berjalan di {host}:{port}")

    client_socket, addr = server_socket.accept()
    print(f"Menerima koneksi dari {addr} \n")
     

    e_alice = public_key_alice["e"]
    n_alice = public_key_alice["n"] 




    while True:

        data_rec = client_socket.recv(2048)
        
        data_rec = pickle.loads(data_rec)

        print("Data yang diterima: ", data_rec)
        
        cipher_text = data_rec["ciphertext_h1"]
        key = data_rec["key"]

        key_decrypt_first = rsa.decrypt_rsa(key, d, n)

        key_decrypt_first = json.loads(key_decrypt_first)

        key_decrypt_second = rsa.decrypt_rsa(key_decrypt_first, e_alice, n_alice)

        key = key_decrypt_second
        key = hex2bin(key)

        keyp = [57, 49, 41, 33, 25, 17, 9,
                1, 58, 50, 42, 34, 26, 18,
                10, 2, 59, 51, 43, 35, 27,
                19, 11, 3, 60, 52, 44, 36,
                63, 55, 47, 39, 31, 23, 15,
                7, 62, 54, 46, 38, 30, 22,
                14, 6, 61, 53, 45, 37, 29,
                21, 13, 5, 28, 20, 12, 4]

        key = permute(key, keyp, 56)


        shift_table = [1, 1, 2, 2,
                    2, 2, 2, 2,
                    1, 2, 2, 2,
                    2, 2, 2, 1]

        rkb_decrypt = []  
            


        key_comp = [14, 17, 11, 24, 1, 5,
                    3, 28, 15, 6, 21, 10,
                    23, 19, 12, 4, 26, 8,
                    16, 7, 27, 20, 13, 2,
                    41, 52, 31, 37, 47, 55,
                    30, 40, 51, 45, 33, 48,
                    44, 49, 39, 56, 34, 53,
                    46, 42, 50, 36, 29, 32]

        print("Decryption\n")
        print("Cipher Text : ", cipher_text)

        left = key[0:28] 
        right = key[28:56]
        rkb_decrypt = []
        rk_decrypt = []

        for i in range(0, 16):
            left = shift_left(left, shift_table[i])
            right = shift_left(right, shift_table[i])
            combine_str = left + right
            round_key = permute(combine_str, key_comp, 48)
            round_key_hex = bin2hex(round_key)
            
            rkb_decrypt.insert(0, round_key) 
            rk_decrypt.insert(0, round_key_hex) 
            

        text = bin2hex(ecb_decrypt(cipher_text, rkb_decrypt, rk_decrypt))
        print("Plain Text hex: ", text)
        text = hex2str(text)
        print("Plain Text After Decrypt: ", text)
        print(" -----------------------------")
if __name__ == "__main__":
    start_client()