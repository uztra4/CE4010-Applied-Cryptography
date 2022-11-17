#############################################################################
# imports
#############################################################################
# to create socket
import socket

#############################################################################
# creating socket
#############################################################################
# define host and port number
HOST = socket.gethostname()
PORT = 44444  

# creating socket
s = socket.socket()

# connect to server
s.connect((HOST, PORT))

# receive response
response = s.recv(1024).decode()

# flag to print response to ensure connectivitiy
print(response)


#############################################################################
# set prefix
#############################################################################
# default case
prefix = "CE4010{"

# case 2 (Show )
# prefix = "CE4010{4PPl1"

# case 3 (Show APPLYING)
# prefix = "CE4010{4PPlY"

# case 4 (wont have result meaning that it is likely that the 4PP here is the first occurance and compress the subsequent 4PP)
# prefix = "CE4010{4PPlY1ng_"

# array to store strings with correct guess
prefixKnown = []

# put known prefix into array
prefixKnown.append(prefix)


#############################################################################
# for loop for CRIME algo (obtain length of encrypted data)
    # flag to track number of repeated strings in a secret
#############################################################################
def CRIME():
    # loop through array
    for x in prefixKnown:
        # print(prefixKnown)
        # loop through all ASCII values from A to z, special characters
        for i in range(33, 127):
            
            # append an extra character to "known prefix" to guess
            guessString = x + chr(i)

            # convert guessString to bytes
            guessString_Bytes = guessString.encode()

            # send to server to encrypt
            s.sendall(guessString_Bytes)

            # get the encrypted guessString
            guessString_encrypt = s.recv(1024).decode('latin-1')

            # do the same for wrongString
            wrongString = x + ','  # assuming that ',' will never appear in the secret cookie
            wrongString_Bytes = wrongString.encode()
            s.sendall(wrongString_Bytes)
            wrongString_encrypt = s.recv(1024).decode('latin-1')

            # compare string length
            # if guess is lesser than the wrong string, means compression happened
            if (len(guessString_encrypt) < len(wrongString_encrypt)):

                # append the correct character into prefixKnown
                prefixKnown.append(guessString)
            
                #print the result
                # print(guessString + ' ' + str(len(guessString_encrypt)) + ' ' + str(len(wrongString_encrypt)))
                print(guessString)

        
    s.close()

if __name__ == '__main__':
    CRIME()