# Import socket module 
import socket	
import pickle
import importlib

AES=importlib.import_module("1905022_AES")
ECDH=importlib.import_module("1905022_ECDH")

	 


def main():
    # Create a socket object 
    s = socket.socket()		
   

    # Define the port on which you want to connect 
    port = 12345			

    # connect to the server on local computer 
    s.connect(('127.0.0.1', port)) 

    s.recv(1024).decode()

    # receive data from the server and decoding to get the string.
    #receive ecdh parameters
    msg = s.recv(1024).decode()
    [g_x,g_y,prime,ka,A_x,A_y] = msg.split(",")
    b=1
    g_x = int(g_x)
    g_y = int(g_y)
    ka = int(ka)
    A_x = int(A_x)
    A_y = int(A_y)

    key="BUET CSE19 Batch"
    # key="Thats my Kung Fu"
    keylen=192
    key=AES.genFixedLengthKey(keylen//8,key)
    round=12
    
    


    B_x,B_y=ECDH.doubleAndAdd(b,g_x,g_y,prime,ka)
    #send key_b

    msg = str(B_x)+","+str(B_y)

    s.send(msg.encode())

    #calculate key
    print("Computing Shared Key:")
    key2_x,key2_y=ECDH.doubleAndAdd(b,A_x,A_y,prime,ka)
    print("Shared Key : ")
    print("key2_x = ",key2_x)
    print("key2_y = ",key2_y)


   
    data = []
    while True:
        packet = s.recv(4096)
        if not packet: break
        data.append(packet)
    cipherText = pickle.loads(b"".join(data))
    print()
    print("Received Cipher Text : ")
    print(cipherText)
    keys=AES.generateKey(key,round)
    keys.reverse()
    decryptedText=AES.AES_Decrypt(cipherText,keys,round,keylen//8)
    print()
    print("Decrypted Text : ")
    print(decryptedText)
    # close the connection 
    s.close()	 


main()
        
