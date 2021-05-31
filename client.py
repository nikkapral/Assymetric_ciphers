import socket
import random
import time

from encriprion import Encryption



class Encryption_Data:

    def __init__(self):
        self.a = random.randint(2, 100)
        self.g = random.randint(2, 100)
        self.p = random.randint(2, 100)
        self.A = self.g ** self.a % self.p
        self.B = 0

    def private_key_K(self):
        K = self.B ** self.a % self.p
        return K

enc_data = Encryption_Data()
enc = Encryption()


client = socket.socket(

    socket.AF_INET,
    socket.SOCK_STREAM

)





try:
    client.connect(("127.0.0.1",1234))
    print("Connected")
except ConnectionRefusedError as e:
    print(f"ERROR: {e}")

while True:
    if enc_data.B == 0: 
        client.send(f'A: {enc_data.A}'.encode())
        time.sleep(0.25)
        client.send(f'g: {enc_data.g}'.encode())
        time.sleep(0.25)
        client.send(f'p: {enc_data.p}'.encode())
        time.sleep(0.25)
        print(f'Sended to server: A: {enc_data.A}\n g: {enc_data.g}\n p: {enc_data.p}')

        while True:
            data = client.recv(1024).decode("utf8")
            if data[:6] == 'B':
                enc_data.B = int(data.split(' ')[2])
                print(f'Key from server: {enc_data.B}')
                print(f'Private key from server: {enc_data.private_key_K()}')
            if enc_data.B != 0:
                break

    text = input("\nMessage: ")
    new_text = enc.Enc(text, enc_data.private_key_K())
    client.send(new_text.encode())

    if len(text) == 0 or text.lower() == 'stop':
        print("Disconnected")
        break

    try:
        enced_data = client.recv(1024).decode("utf8")
        denced_data = enc.Enc(enced_data, enc_data.private_key_K())
        print(f"\nServer answer: {denced_data}")
    except ConnectionResetError as e:
        print(f"ERROR: {e}")
        break

client.close()