# first of all import the socket library 
import socket	
import pickle	
import importlib

AES=importlib.import_module("1905022_AES")
ECDH=importlib.import_module("1905022_ECDH")

def main():
    # next create a socket object 
    s = socket.socket()		 
    print ("Socket successfully created")

    # reserve a port on your computer in our 
    # case it is 12345 but it can be anything 
    port = 12345			

    # Next bind to the port 
    # we have not typed any ip in the ip field 
    # instead we have inputted an empty string 
    # this makes the server listen to requests 
    # coming from other computers on the network 
    s.bind(('', port))		 
    print ("socket binded to %s" %(port)) 

    # put the socket into listening mode 
    s.listen(5)	 
    print ("socket is listening")		

    #elliptic curve diffie hellman encryption
    # a,g,Ka,Kb
    bits=128
    a=5
    prime=ECDH.generatePrime(bits)
    g_x,g_y=ECDH.generatePoint(bits)
    ka=ECDH.generateElipticCurve(prime,g_x,g_y,bits)
    A_x,A_y=ECDH.doubleAndAdd(a,g_x,g_y,prime,ka)

    #aes encryption
    plainText="Never Gonna Give you up"
    key="BUET CSE19 Batch"
    # plainText="Two One Nine Two"#"Never Gonna Give you up"
    # key="Thats my Kung Fu"#"BUET CSE19 Batch"
    keyLen=192
    round=12
   
   

    # a forever loop until we interrupt it or 
    # an error occurs 
    while True: 

        # Establish connection with client. 
        c, addr = s.accept()	 
        print ('Got connection from', addr )

        c.send("cheques-shubh".encode())
        print()

        msg = str(g_x)+","+str(g_y)+","+str(prime)+","+str(ka)+","+str(A_x)+","+str(A_y)
        c.send(msg.encode())


        print("Plain Text:")
        print(plainText)
        print()
        print("Computing Shared Key:")
        msg=c.recv(1024).decode()
        [B_x,B_y] = msg.split(",")
        B_x = int(B_x)
        B_y = int(B_y)
        key1_x,key1_y=ECDH.doubleAndAdd(a,B_x,B_y,prime,ka)
        print("Shared Key:")
        print("key1_x = ",key1_x)
        print("key1_y = ",key1_y)
        print()
        print("Sending Cypher Text:")

        iv=AES.generateRandString(keyLen//8)
        key=AES.genFixedLengthKey(keyLen//8,key)
        keys=AES.generateKey(key,round)
        cipherText=AES.AES_Encrypt(keyLen,plainText,keys,iv,round)


       
        # hexCArr=pickle.dumps(hexCArr)
        c.send(pickle.dumps(cipherText))
        print(cipherText)

        # Close the connection with the client 
        c.close()

        # Breaking once connection closed
        break
main()