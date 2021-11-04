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

name = "Olivia"
print(name[-1: -3: -1])

num = 43
num_as_bin = bin(num)[2:]
print(num_as_bin)

bigger_last_bits = num_as_bin[-1: -(2 + 2) : -1]
print(bigger_last_bits[::-1]) 

res = 10/2
print(res)
print(type(res))

num = 0
as_bin = bin(num)[2:]
print(type(as_bin))
print(as_bin) 

print(int(as_bin,2))

i = 2
page_size = 2
print(int(math.ceil(i + 1 / page_size)))