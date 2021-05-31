import random
import socket
import time
from encriprion import Encryption



class Encryption_Data:

    def __init__(self):
        self.b = random.randint(2, 100)
        self.g = 0
        self.p = 0
        self.A = 0

    def public_key_B(self):
        B = self.g ** self.b % self.p
        return B

    def private_key_K(self):
        K = self.A ** self.b % self.p
        return K

server = socket.socket(

    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(

    ("127.0.0.1",1234)

)

enc_data = Encryption_Data()
enc = Encryption()

while True:

    server.listen(1)

    conn = server.accept()[0]
    print()

    while True:

        if enc_data.A != 0 and enc_data.p != 0 and enc_data.g != 0:
            print(f'Sended key B to client {enc_data.public_key_B()}')
            print(f'Have made private key B: {enc_data.private_key_K()}')
            time.sleep(0.25)
            conn.send(f'Key B: {enc_data.public_key_B()}'.encode())

        try:
            data = conn.recv(1024).decode("utf8")
        except ConnectionResetError:
            break

        if data[:6] == 'key A':
            print(data)
            enc_data.A = int(data.split(' ')[2])
        elif data[:8] == 'g':
            print(data)
            enc_data.g = int(data.split(' ')[2])
        elif data[:8] == 'p':
            print(data)
            enc_data.p = int(data.split(' ')[2])
        else:

            data = enc.Enc(data, enc_data.private_key_K())
            new_data = enc.Enc("client message: " + data, enc_data.private_key_K())

            if data == "stop":
                break
            else:

                conn.send(new_data.encode())

                print()

    if data == "stop":
        break

conn.close()

