import time
from random import randint
from BitVector import *
import random
import xlsxwriter


def power(x, y, p) :
    res = 1
    x = x % p
    while (y > 0) :
        if ((y & 1) == 1) :
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res

def invMod(a,prime):
    # power=prime-2
    return power(a,prime-2,prime)


def generatePrime(bits):
    # Generate a random prime number of the specified bit length.
    bitVector = BitVector(intVal = 0)
    isPrime = 0
    while isPrime < 0.999:
        bitVector=bitVector.gen_random_bits(bits)
        #testing for primality  
        isPrime= bitVector.test_for_primality()

    intVal=bitVector.intValue()
    return intVal


def generatePoint(bits):
    x = BitVector(intVal=0, size=bits)
    y = BitVector(intVal=0, size=bits)
    x[0] = 1
    y[0] = 1
    for i in range(1, bits-1):
        x[i] = randint(0,1)
        y[i] = randint(0,1)
    return x.intValue(),y.intValue()




def generateElipticCurve(prime,x,y,bits):
    startVal=-1*(1<<bits)
    endVal=(1<<bits)

    a = random.randint(startVal,endVal)
    # init b
    b=0
    while True:
        b = (y**2-x**3-a*x)%prime
        if (4*(a**3)+27*(b**2))%prime==0 or (a==0) or (b==0): #choose another a 
            a = random.randint(startVal,endVal)
        else:
            break
    #check
    # print("a= ",a," b= ",b)
    return a


def add(x1,y1,x2,y2,prime,a):
    #divisions are done by multiplying by the inverse
    if x1==x2 and y1==y2:
        s=(3*x1**2+a)%prime
        t=(2*y1)%prime
        s=(s*invMod(t,prime))%prime
        x3=(s**2-2*x1)%prime
        y3=(s*(x1-x3)-y1)%prime
    else:
        s=(y2-y1)*invMod(x2-x1,prime)%prime
        x3=(s**2-x1-x2)%prime
        y3=(s*(x1-x3)-y1)%prime

    return x3,y3



def doubleAndAdd(d,x,y,prime,a):# d is the number of times to double and add

    #if odd then multiply by 2 and add 1
    #if even then only  multiply by 2, no add
    if d==1:
        return (x,y)
    tx,ty = doubleAndAdd(d>>1,x,y,prime,a)
    tx,ty = add(tx,ty,tx,ty,prime,a)
    if d%2==1:
        tx,ty = add(tx,ty,x,y,prime,a)
    return tx,ty

def average(arr):
    sum=0
    for i in range(len(arr)):
        sum+=arr[i]
    return sum/(len(arr))

def main():
    #secret key
    a=2
    b=2
    keylenths={128,192,256}
    iterateNo=5

    #printing report
    workbook = xlsxwriter.Workbook('ComputationTime for ECDH.xlsx')
 
    #add work sheet
    worksheet = workbook.add_worksheet()
    

    worksheet.write('A1', 'KeyLength')
    worksheet.write('B1', 'A')
    worksheet.write('C1', 'B')
    worksheet.write('D1', 'Shared key(R)')

    row=1
    col=0
    for bits in keylenths:

        worksheet.write(row,col,bits)
        j=1
        timeA=[iterateNo]
        timeB=[iterateNo]
        timeKey1=[iterateNo]
        while j<iterateNo:
            start_time = time.time()*1000*1000
            prime=generatePrime(bits)
            # prime=17
            #point
            x,y=generatePoint(bits)
            # x=5
            # y=1

            #curve  ........... co-efficients
            c_a=generateElipticCurve(prime,x,y,bits)
            # print(prime,a,b)

            #encrypt
            #calculate A,B
            A_x,A_y=doubleAndAdd(a,x,y,prime,c_a)
            time1=time.time()*1000*1000-start_time
            timeA.append(time1)
            # print("timeA= ",timeA)
            start_time = time.time()*1000*1000
            B_x,B_y=doubleAndAdd(b,x,y,prime,c_a)
            time2=time.time()*1000*1000-start_time
            timeB.append(time2)

            # print("timeB= ",timeB)
            start_time = time.time()*1000*1000
            key1_x,key1_y=doubleAndAdd(a,B_x,B_y,prime,c_a)
            # key2_x,key2_y=doubleAndAdd(b,A_x,A_y,prime,c_a)
            time3=time.time()*1000*1000-start_time
            timeKey1.append(time3)
            # print("timeKey1= ",timeKey1)
            j+=1

        # print("timeA= ",timeA)  
        # print("timeB= ",timeB)
        # print("timeKey1= ",timeKey1)
        worksheet.write(row,col+1,average(timeA))
        worksheet.write(row,col+2,average(timeB))
        worksheet.write(row,col+3,average(timeKey1))

        row+=1

    workbook.close()


main()