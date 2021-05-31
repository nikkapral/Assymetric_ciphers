class Encryption:

    def __init__(self):
        pass

    def Enc(self, text, key):
        return "".join([chr(ord(text[i]) ^ key) for i in range(len(text))])