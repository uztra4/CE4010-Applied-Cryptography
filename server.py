#############################################################################
# imports
#############################################################################


#############################################################################
# imports
#############################################################################
# to create socket
import socket

# to compress
import zlib
import gzip

#to create AES secret key
from Crypto.Cipher import AES

# for padding
from Crypto.Util.Padding import pad

# create psudo-random numbers
import os


#############################################################################
# creating socket
#############################################################################
# define host and port number
HOST = socket.gethostname()    # all available interfaces
PORT = 44444  # any port > 1023

# creating socket
s = socket.socket()
s.bind((HOST, PORT))

# setting the number of client server can listen simultaneously
s.listen(1) 

# accept new connection
conn, addr = s.accept()

# flag to ensure that client connected to server successfully
string = 'Client connected: ' + str(addr)
print(string) # print in server
conn.sendall(str.encode(string)) # send to client


#############################################################################
# set secret
#############################################################################
# default case
secret = "CE4010{4PPl13d_cRypt0_15_fun!}"

# case 2 (duplicate string 4PP)
# secret = "CE4010{4PPlY1ng_4PPl13d_cRypt0_15_fUn!}"


#############################################################################
# encrypt function (AES-CTR)
# why in server?
    # we are mimicking the compression encryption done in a server and how a CRIME attack
    # can make use of this vulnerability to obtain secret cookie
#############################################################################
# plaintext is the random guess
def encrypt(plaintext):

    # cipher creates a 16 byte (128 bit) AES secret key that can be used to encrypt secret
    cipher = AES.new(os.urandom(16), AES.MODE_CTR)

    # concatenate plaintext and secret
    stringConcat = plaintext + secret

    # pad before encryption
    padString = pad(stringConcat.encode(), 16)

    # # encode the stringConcat (convert string into bytes)
    # encodeString = padString.encode()

    # concatenate plaintext with secret
    # compressedString = gzip.compress(padString)
    compressedString = zlib.compress(padString)
    
    # return encrypted plain text in hexadecimal
    return cipher.encrypt(compressedString)


#############################################################################
# main function
#############################################################################
def server():
    while True:

        # 1024 is maximum bytes that can be received
        data = conn.recv(1024)
        
        if not data:
            break
        
        # convert plaintext from byte to string
        dataString = data.decode()

        # convert plaintext to ciphertext
        inputEncrypted = encrypt(dataString)

        # sendall can only pass bytes data type
        conn.sendall(inputEncrypted)

    conn.close()


if __name__ == '__main__':
    server()