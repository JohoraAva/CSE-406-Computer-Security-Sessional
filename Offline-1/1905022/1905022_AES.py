import time
from BitVector import *
import random
import string
import base64

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

#used in roundConstant
multiplier = BitVector(hexstring="02")

AES_modulus = BitVector(bitstring='100011011') # Used in gf_multiply_modular()
Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]


#decrypt 
InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)
InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

def fileToAscii(file_path):
    try:
        with open(file_path, 'rb') as file:
            # Read binary data from the file
            binary_data = file.read()
            
            # Encode the binary data using Base64
            ascii_string = base64.b64encode(binary_data).decode('ascii')
            
            return ascii_string
    except FileNotFoundError:
        return "File not found"

#ascii string to file
def asciiToFile(ascii_string, file_path):
    try:
        with open(file_path, 'wb') as file:
            # Convert the ascii string back to binary
            binary_data = base64.b64decode(ascii_string.encode('ascii'))
            
            # Write the binary data to the file
            file.write(binary_data)
            
            return True
    except FileNotFoundError:
        return False 
    

def strToHex(text):
    hexText=""
    for i in range(len(text)):
        hexText+=hex(ord(text[i]))[2:]
        hexText+=" "
    return hexText

def Lshift(word,n):
    for i in range(n):
        temp=word[0]
        word=word[1:]
        word.append(temp)
    return word

def substituteByte(word):
    temp=[]
    for i in word:
        temp.append(BitVector(intVal=Sbox[i.intValue()], size=8))
    return temp


def xor(word1,word2):
    temp=[]
    for i in range(len(word1)):
        temp.append(word1[i]^word2[i])
    return temp

def g(word,round):
    temp=Lshift(word,1)
    temp=substituteByte(temp)
    temp=xor(temp,[round,BitVector(intVal=0x00, size=8),BitVector(intVal=0x00, size=8),BitVector(intVal=0x00, size=8)])

    return temp


def convertToArr(text, isBitVector=False): #convert ascii to hex/bitvector array
    arr=[]
    for i in range(len(text)):
        if isBitVector:
            arr.append(BitVector(intVal=ord(text[i]), size=8))
        else:
            arr.append(text[i].encode().hex())
    return arr

def arrToMatrix(arr,isReverse):
    mat=[]
    length=len(arr)
    for i in range(4): # 4 rows
        rows=[]
        for j in range(i,length,4):
            if isReverse:
                rows.append(arr[j])
            else:
                rows.append(BitVector(hexstring=arr[j]))
        
        mat.append(rows)

    return mat


def printMat(mat):
    for i in range(4):
        for j in range(len(mat[i])):
            print(mat[i][j].get_bitvector_in_hex(),end=" ")
        print()
    print()


def xorMat(mat1,mat2):
    temp=[]
    for i in range(len(mat1)):
        rows=[]
        for j in range(len(mat1[i])):
            rows.append(mat1[i][j]^mat2[i][j])
        temp.append(rows)
    return temp

def substituteByteMat(mat):
    temp=[]
    for i in range(4):
        temp.append(substituteByte(mat[i]))
    return temp

def LshiftMat(mat):
    temp=[]
    for i in range(4):
        temp.append(Lshift(mat[i],i))
    return temp



def mixColMat(mat,opMat):
    #for encrypt , opMat=Mixer 
    #else InvMix
    temp=[len(mat[0])*[0] for i in range(4)]
    #init temp with bitvector
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            temp[i][j]=BitVector(intVal=0x00, size=8)

    for i in range(len(mat)):
        for j in range(len(mat[i])):
           for k in range(len(mat)):
            temp[i][j]^=opMat[i][k].gf_multiply_modular(mat[k][j],AES_modulus,8)	
    return temp



def getColArray(mat,col):
    temp=[]
    for i in range(len(mat)):
        temp.append(mat[i][col])
    return temp

def printArr(arr):
    for i in range(len(arr)):
        print(arr[i].get_bitvector_in_hex(),end=" ")
    print()


def transpose(mat):
    row=len(mat)
    col=len(mat[0])
    temp=[]
    for i in range(col):
        rows=[]
        for j in range(row):
            rows.append(mat[j][i])
        temp.append(rows)
    return temp


def generateKey(key,round):
    # round=10
    roundConstant=BitVector(hexstring="01")
    keys=[]

    #convert ascii to matrix
    hexKey=convertToArr(key)
    keyArr=arrToMatrix(hexKey,False)
    keys.append(keyArr)
   
    #gen next key
    # colArr1 xor colArr2
    col=len(keys[0][0])-1
    for l in range(round):

        colArr2=g(getColArray(keys[l],col),roundConstant)
        temKey=[]
        for i in range(len(keys[l][0])):
            colArr = getColArray(keys[l],i)
            colArr2=xor(colArr2,colArr)
            temKey.append(colArr2)
        
        temKey=transpose(temKey)

        keys.append(temKey)
        colArr=getColArray(temKey,col)
        roundConstant = multiplier.gf_multiply_modular(roundConstant, AES_modulus, 8)
    return keys

def generateCypherText(textArr,keys,round): #from plain mat to cipher mat
      #round 1
    cryptArr=xorMat(textArr,keys[0])
   

    #round 2-10
    for i in range(1,len(keys)):
        
        #byte substitution
        cryptArr=substituteByteMat(cryptArr)
        # printMat(cryptArr)
        cryptArr=LshiftMat(cryptArr)
        # printMat(cryptArr)
        #round 10, no mix column
        if i!=round:
            cryptArr=mixColMat(cryptArr,Mixer)
        cryptArr=xorMat(cryptArr,keys[i])
       
     
    return cryptArr

#return all blocks (4*4 matrix) 
def textToMats(hexText,keyLen,isDecrypt=False): 
    allTexts=[]
    i=0
    while i<len(hexText):
        block=[]
        for j in range(i,i+keyLen):
            if j<len(hexText):
                block.append(hexText[j])
        i+=keyLen
        if isDecrypt:
            allTexts.append(arrToMatrix(block,isDecrypt))
        else:
            allTexts.append(block)
    return allTexts



def padding(textArr,paddCount):

    temp=paddCount
   
    while temp>0:
        str=""
        if paddCount<16:
            str="0"
        str+=hex(paddCount)[2:]
        # print(str)
        textArr.append(str)
        temp-=1

    return textArr

def AES_Encrypt(keyLen,plainText,keys,iv,round): #let keylen=128, so per block character is 16

    #iv 
    ivArr=convertToArr(iv)
    ivMat=arrToMatrix(ivArr,False)

    #plain text
    hexText=convertToArr(plainText)


    #divide into 4*4 matrix
    blockSize=keyLen//8
    textBlocks=textToMats(hexText,blockSize)
   
    paddCount=blockSize-len(textBlocks[len(textBlocks)-1])
    if paddCount==0:
        textBlocks.append(blockSize*["00"])
    else:
        textBlocks[len(textBlocks)-1]=padding(textBlocks[len(textBlocks)-1],paddCount)
    textArr=[len(textBlocks)*[0] for i in range(len(textBlocks))]
    for i in range(len(textBlocks)):
        textArr[i]=arrToMatrix(textBlocks[i],False)

 


    #encryption
    cryptArr=[]
    for i in range(len(textArr)):
        textArr[i]=xorMat(textArr[i],ivMat)
        cryptArr.append(generateCypherText(textArr[i],keys,round))
        ivMat=cryptArr[i] 

    arr=convertMats(cryptArr)
    str=iv+arrToAscii(arr)
    
    return str


def RShift(word,n):
    for i in range(n):
        temp=word[-1]
        word=word[:-1]
        word.insert(0,temp)
    return word

def RShiftMat(mat):
    temp=[]
    for i in range(4):
        temp.append(RShift(mat[i],i))
    return temp

def inverseSubstituteByte(word):
    temp=[]
    for i in word:
        temp.append(BitVector(intVal=InvSbox[i.intValue()], size=8))
    return temp

def inverseSubstituteByteMat(mat):
    temp=[]
    for i in range(4):
        temp.append(inverseSubstituteByte(mat[i]))
    return temp

def generateDecryption(cipherMat,keys,round):

    decryptArr=xorMat(cipherMat,keys[0])
    #round 1
    decryptArr=RShiftMat(decryptArr)
    decryptArr=inverseSubstituteByteMat(decryptArr)
    decryptArr=xorMat(decryptArr,keys[1])
    decryptArr=mixColMat(decryptArr,InvMixer)

    #round 2-10
    for i in range(2,len(keys)):
        #byte substitution
        decryptArr=RShiftMat(decryptArr)
        decryptArr=inverseSubstituteByteMat(decryptArr)
        decryptArr=xorMat(decryptArr,keys[i])
        if i!=round:
            decryptArr=mixColMat(decryptArr,InvMixer)
     
    return decryptArr


def AES_Decrypt(cipherText,keys,round,blockSize):

    # separate ivMat,cipherMat 
    ivArr=convertToArr(cipherText[:blockSize])
    cipherText=cipherText[blockSize:]
    ivMat=arrToMatrix(ivArr,False)

    cipherMat=textToMats(convertToArr(cipherText,True),blockSize,True)


   
    # array of mats
    decryptArr=[]
    for i in range(len(cipherMat)):
        decryptArr.append(generateDecryption(cipherMat[i],keys,round))
        if i==0:
            decryptArr[i]=xorMat(decryptArr[i],ivMat)
        else:
            decryptArr[i]=xorMat(decryptArr[i],cipherMat[i-1])

    hexArr=convertMats(decryptArr)
    withoutPad=removePadding(hexArr)
    decryptedText=arrToAscii(withoutPad)
    return decryptedText


def matToArr(mat):
    temp=[]
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            temp.append(mat[i][j])
    return temp


def arrToAscii(arr):
    temp=""
    for i in range(len(arr)):
        temp+=chr(int(arr[i].get_bitvector_in_hex(),16))
    return temp





def convertMats(cipherMats): #convert cipher matrix to array
    hexArr=[]
    for i in range(len(cipherMats)):
        cipherMat=transpose(cipherMats[i])
        cipherArr=matToArr(cipherMat)
        for j in range(len(cipherArr)):
            cipherArr[j]=BitVector(intVal=cipherArr[j].intValue(), size=8)
            hexArr.append(cipherArr[j])

    return hexArr




#remove padding

def removePadding(text):
    length=len(text)
    intVal=text[length-1].get_bitvector_in_hex()

    if text[length-1]==BitVector(intVal=0x00, size=8):
        return text[:length-16]
    else :
        #remove appropriate number of bytes
        intVal=int(intVal,16)
        return text[:length-intVal]
   

#generate random string for ind-cpa
def generateRandString(length):
    temp=''.join(random.choices(string.ascii_letters, k=length))
    return temp


def genFixedLengthKey(length,key):
    temp=""
    for i in range(len(key)):
        temp+=key[i]
    while length>len(temp):
        temp+="00"
    return temp

       


def main():
    #var declaration
    plainText="Never Gonna Give you up"
    key="BUET CSE19 Batch"
    # plainText="Two One Nine Two"#"Never Gonna Give you up"
    # key="Thats my Kung Fu"#"BUET CSE19 Batch"
    keyLen=256
    round=14


    # file enc-dec
    # filename="file.txt"
    # plainText=fileToAscii("E:\Lab Courses\CSE-406\Offline-1\offline-1" +"//"+ filename)
    # print("plaintext= ", plainText)
    # # print("here")
    # key="Thats my Kung Fu"

    #key


    #encryption

    # #cbc
    # iv 
    iv=generateRandString(keyLen//8)
    startTime=time.time()
    #key
    key=genFixedLengthKey(keyLen//8,key)
    keys=generateKey(key,round)
    keyScheduleTime=time.time()-startTime
    #encryption
    startTime=time.time()
    cipherText=AES_Encrypt(keyLen,plainText,keys,iv,round)
    encryptTime=time.time()-startTime

    hexCArr=convertToArr(cipherText,True)
   
   

  
    
    #decryption
   
    keys=generateKey(key,round)
    keys.reverse()
    startDecrypt=time.time()
    decryptedText=AES_Decrypt(cipherText,keys,round,keyLen//8)
    decryptTime=time.time()-startDecrypt


    #file
    # asciiToFile(decryptedText,"E:\Lab Courses\CSE-406\Offline-1\offline-1" +"//"+ "decrypted_"+filename)

   



    # # //print
    print("Key:")
    print("In ASCII: ",key)
    print("In Hex: ",strToHex(key))
    print()
    print("Plain Text:")
    print("In ASCII: ",plainText)
    print("In Hex: ",strToHex(plainText))
    print()
    print("Cipher Text:")
    print("In Hex: ",strToHex(arrToAscii(hexCArr)))
    print("In ASCII: ",cipherText)
    print()
    print("Deciphered Text:")
    print("In Hex: ",strToHex(decryptedText))
    # printArr(hexArr)
    print("In ASCII: ",decryptedText)
    print()


    #time print 
    print("Execution Time Details:")
    print("Key Schedule Time: ",keyScheduleTime*1000,"ms")
    print("Encryption Time: ",encryptTime*1000,"ms")
    print("Decryption Time: ",decryptTime*1000,"ms")

    
# main()