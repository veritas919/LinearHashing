# from . import Bucket 
import copy 
import math 

class LinearHashing:

    # constructor
    def __init__(self, page_size=None, policy = 0, max_overflow = 0, size_limit = 1.0):
        self.page_size = page_size
        self.policy = policy
        self.level = 0
        self.ptr = 0
        self.is_an_overflow_rn = False
        self.num_buckets_overflowing = 0
        self.num_buckets = 1 # only keeping track of main buckets rn....NOT overflow 
        self.max_overflow = max_overflow 
        self.size_limit = size_limit 

        self.hash_table = {}
        self.hash_table [0] = []

    def insert(self, number):
        if self.policy == 0:
            self.case_0_insert(number)
        elif self.policy == 1:
            self.case_1_insert(number) 


    def case_0_insert(self, num):
        split_occured = False
        print("in case 0")
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 
            # check if any bucket is overflowing 
            self.isOverflowedRightNow() 
                # if there is an overflow  ----- > create new bucket, rehash, level up, reset ptr 
            if self.is_an_overflow_rn == True:  
                self.hash_table[1] = [] # create new bucket 

                copy_of_bucket_0 = copy.deepcopy(self.hash_table[0])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_0:
                    # print(item)
                    if item % 2 == 0:
                        bucket_0.append(item)
                    else:
                        bucket_1.append(item) 
                self.hash_table[0] = bucket_0
                self.hash_table[1] = bucket_1 
                self.level = 1
                self.ptr = 0 
                self.num_buckets += 1
                split_occured = True 

                # self.isOverflowedRightNow()   # MUST RECHECK    WORKS FINE WITHOUT @@@@@@@@@@@@ TAKE OUT TEMP 

        # for other levels
        else: 
            print("else", num)
            print("Level is: ", self.level)
            
            ############ INSERT NUMBER INTO BUCKET ############
            num_as_bin = bin(num)[2:]
            
            if len(num_as_bin) <= self.level:
                ht_index_try_1 = num
                if ht_index_try_1 in self.hash_table:
                    self.hash_table[ht_index_try_1].append(num)
                else:
                    print("cant find matching bucket")

            # number as binary is necessarily >= 2 
            else: 
                bigger_last_bits = num_as_bin[-1: -(self.level + 2) : -1][::-1]
                smaller_last_bits = num_as_bin[-1: -(self.level + 1) : -1][::-1]
                if int(bigger_last_bits, 2) in self.hash_table:
                    self.hash_table[int(bigger_last_bits,2)].append(num) 
                elif int(smaller_last_bits, 2) in self.hash_table:
                    self.hash_table[int(smaller_last_bits,2)].append(num) 
                else:
                    print("problem. number is....:", num, bigger_last_bits, smaller_last_bits)

            self.isOverflowedRightNow()

            print("is overflow?", self.is_an_overflow_rn)
            # if there is an overflow  ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.is_an_overflow_rn == True:
                # print("spliiting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]
                print("spliting bucket: ", self.ptr)
                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
                    print("item in splitting bucket...",item)
                    item_as_bin = bin(item)[2:]

                    if len(item_as_bin) <= self.level + 1:
                        k_bits_as_int = item 
                    else:
                        k_bits_as_int = int(item_as_bin[-1: -(self.level + 2) : -1][::-1], 2)
                    
                    if k_bits_as_int == new_bucket_value_0:
                        bucket_0.append(item)
                    elif k_bits_as_int == new_bucket_value_1:
                        bucket_1.append(item)
                    else:
                        print("problemo. item val is: ", item) 

                self.hash_table[new_bucket_value_0] = bucket_0
                self.hash_table[new_bucket_value_1] = bucket_1 
                
                self.num_buckets += 1
                self.ptr +=1 
                split_occured = True 
                # post split, check if next level now
                if self.num_buckets == 2**(self.level+1):
                    print("incrementing level")
                    print(self.num_buckets) 
                    self.level += 1
                    self.ptr = 0

                # self.isOverflowedRightNow() # RECHECK...MUST DO        WORKS FINE WITHOUT  @@@@@@@@@@@@@@@@@@@@@@ TAKE OUT 
        return split_occured 


    def get_num_buckets(self):
        return self.num_buckets 

    def isOverflowedRightNow(self):
        flag = False 
        for key in self.hash_table:
                if len(self.hash_table[key]) > self.page_size: #overrflow!
                    self.is_an_overflow_rn = True
                    flag = True
        if flag == True:
            self.is_an_overflow_rn = True
        else:
            self.is_an_overflow_rn = False 

    def get_total_number_of_overflow_buckets(self):
        num_overflow = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            overflow_for_that_key = int(math.ceil(num_items_for_key / self.page_size)) - 1
            num_overflow += overflow_for_that_key 

        return num_overflow 




    def print_ht(self):
        for key in self.hash_table:
            print("key", key)
            for item in self.hash_table[key]:
                print(item) 
            print("\n")

if __name__ == "__main__":
    x = LinearHashing(page_size = 2, policy = 0, max_overflow = 2)
    x.insert(2)
    x.insert(0)
    x.insert(1) 
    print("bucket #: ", x.get_num_buckets())
    x.insert(5)
    print("bucket #: ", x.get_num_buckets())
    x.insert(23)
    print("bucket #: ", x.get_num_buckets())
    x.insert(42)
    print("bucket #: ", x.get_num_buckets())
    x.insert(55)
    print("bucket #: ", x.get_num_buckets())
    x.insert(10)
    print("bucket #: ", x.get_num_buckets())
    x.print_ht()
    x.insert(999)
    x.insert(-13)
    x.insert(-55)

    # x.print_ht() 
    x.insert(43) 

    x.print_ht() 
    
    x.insert(45)
    x.insert(2328356)
    x.insert(8) 
    x.insert(21)
    x.insert(32)
    x.insert(2000)
    x.insert(0)
    x.insert(1) 


    x.print_ht()


