import math
num = 8

as_bin = bin(num)[2:]
print(type(as_bin))

print(int(as_bin,2))
'''
print(as_bin)

print(int(as_bin, 2)) 

num_2 = 7
bin_n = bin(num_2)
str_num = str(bin_n[2:])
left_pad = str_num.zfill(len(str_num) +1)
print(left_pad) 
'''

x = "hi there"
print(x[3:3])

print(math.ceil(1))
print(math.ceil(1.0001))