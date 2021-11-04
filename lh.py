# from . import Bucket 
import copy 
import math 
import random 


class LinearHashingStats:

    def __init__(self, hash_table, page_size):
        self.count = 0
        self.buckets = 0
        self.pages = 0
        self.overflow_buckets = 0
        self.access = 0
        self.access_insert_only = 0
        self.split_count = 0 

        self.hash_table = hash_table
        self.page_size = page_size 

    # return # of items in hash table
    def Count(self):
        # get number of items in the table
        num_items_in_table = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            num_items_in_table += num_items_for_key 
        return num_items_in_table

    # return # of main buckets ... NOT counting overflow. doesnt matter if bucket is empty or not....it counts  
    def Buckets(self):
        num_keys = 0
        for key in self.hash_table:
            num_keys += 1
        return num_keys 

    # returns # of pages in table. If bucket has no numbers in it, it still has 1 page 
    def Pages(self):
        # get number of pages in table
        page_number = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            if num_items_for_key == 0: 
                page_number += 1
            else:
                page_number += int(math.ceil(num_items_for_key / self.page_size)) 
        return page_number 

    def OverflowBuckets(self):
        num_overflow = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            if num_items_for_key == 0:
                continue
            overflow_for_that_key = int(math.ceil(num_items_for_key / self.page_size)) - 1
            num_overflow += overflow_for_that_key 

        # print("num overflow: ", num_overflow)
        return num_overflow 

    def SplitCount(self):
        return self.split_count 

    def Access(self):
        return self.access 

    def AccessInsertOnly(self):
        return self.access_insert_only

    def SpaceUtilization(self):
        # get number of items in the table
        num_items_in_table = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            num_items_in_table += num_items_for_key
        
        # get number of pages in table
        page_number = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            if num_items_for_key == 0: # if no numbers in key, assume it still has 1 page 
                page_number += 1
            else:
                page_number += int(math.ceil(num_items_for_key / self.page_size)) 

        current_capacity = (num_items_in_table) / (page_number * self.page_size)
        return current_capacity       



class LinearHashing:

    # constructor
    def __init__(self, page_size=None, policy = 0, max_overflow = 0, size_limit = 1.0):
        

        # basic error checking 
        if page_size < 0 or None:
            print("invalid page size. exitting.")
            quit()

        if policy not in range(0,4):
            print("invalid policy number. exitting.")
            quit() 
        if size_limit < 0 or size_limit > 1:
            print("size_limit should be in [0,1]")    
            quit()    
        
        self.page_size = page_size
        self.policy = policy
        self.level = 0
        self.ptr = 0
        self.max_overflow = max_overflow 
        self.size_limit = size_limit 

        self.is_an_overflow_rn = False  # dont think I need 
        self.num_buckets_overflowing = 0    # dont think I need 
        self.num_buckets = 1 # only keeping track of main buckets rn....NOT overflow. dont think I use this  

        print("SIZELIMIT", self.size_limit)

        self.hash_table = {}
        self.hash_table [0] = []

        self.stats = LinearHashingStats(hash_table=self.hash_table, page_size=self.page_size) 

    def Insert(self, number):
        # call appropriate insert function. Also increment access by one 
        if self.policy == 0:
            self.case_0_insert(number)
            self.stats.access += 1
            self.stats.access_insert_only += 1 
        elif self.policy == 1:
            self.case_1_insert(number)
            self.stats.access += 1 
            self.stats.access_insert_only += 1 
        elif self.policy == 2:
            self.case_2_insert(number)
            self.stats.access += 1 
            self.stats.access_insert_only += 1 
        elif self.policy == 3:
            self.case_3_insert(number)
            self.stats.access += 1
            self.stats.access_insert_only += 1 
        else:
            print("invalid value for policy.")

    ######################################################################### CASE 0 INSERT ##########################################################################
    def case_0_insert(self, num):
        split_occured = False
        print("in case 0")
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 
            # check if any bucket is overflowing 
            #self.isOverflowedRightNow(0) 
                # if there is an overflow  ----- > create new bucket, rehash, level up, reset ptr 
            if self.isOverflowedRightNow(0) == True:  
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
                self.stats.split_count += 1 # update stats object  

                # self.isOverflowedRightNow()   # MUST RECHECK    WORKS FINE WITHOUT @@@@@@@@@@@@ TAKE OUT TEMP 

        # for other levels
        else: 
            print("else", num)
            print("Level is: ", self.level)
            
            ############ INSERT NUMBER INTO BUCKET ############
            num_as_bin = bin(num)[2:]
            
            bucket_key = None 
            if len(num_as_bin) <= self.level:
                ht_index_try_1 = num
                if ht_index_try_1 in self.hash_table:
                    self.hash_table[ht_index_try_1].append(num)
                    bucket_key = ht_index_try_1
                else:
                    print("cant find matching bucket")

            # number as binary is necessarily >= 2 
            else: 
                bigger_last_bits = num_as_bin[-1: -(self.level + 2) : -1][::-1]
                smaller_last_bits = num_as_bin[-1: -(self.level + 1) : -1][::-1]
                if int(bigger_last_bits, 2) in self.hash_table:
                    self.hash_table[int(bigger_last_bits,2)].append(num)
                    bucket_key = int(bigger_last_bits,2)
                elif int(smaller_last_bits, 2) in self.hash_table:
                    self.hash_table[int(smaller_last_bits,2)].append(num) 
                    bucket_key = int(smaller_last_bits,2)
                else:
                    print("problem. number is....:", num, bigger_last_bits, smaller_last_bits)

            # self.isOverflowedRightNow()

            # print("is overflow?", self.is_an_overflow_rn)
            # if there is an overflow  ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.isOverflowedRightNow(bucket_key) == True:
                # print("spliiting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]
                print("spliting bucket: ", self.ptr)
                print("\n")
                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
                    # print("item in splitting bucket...",item)
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
                self.stats.split_count += 1
                # post split, check if next level now
                if self.num_buckets == 2**(self.level+1):
                    print("incrementing level")
                    print(self.num_buckets) 
                    self.level += 1
                    self.ptr = 0

                # self.isOverflowedRightNow() # RECHECK...MUST DO        WORKS FINE WITHOUT  @@@@@@@@@@@@@@@@@@@@@@ TAKE OUT 
        return split_occured 

    ##################################################################### CASE 1 INSERT ####################################################

    def case_1_insert(self, num):
        split_occured = False
        print("in case 1")
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 

            # if the number of overflow buckets is >= max_overflow  ----- > create new bucket, rehash, level up, reset ptr 
            if self.get_total_number_of_overflow_buckets() >=  self.max_overflow:  
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
                self.num_buckets += 1 # dont know abt this 
                split_occured = True
                self.stats.split_count += 1 

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

            #self.isOverflowedRightNow()

            #print("is overflow?", self.is_an_overflow_rn)
            # if the number of overflow buckets is >= maxoverflow  ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.get_total_number_of_overflow_buckets() >= self.max_overflow:
                # print("spliiting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]
                print("splitting bucket: ", self.ptr)
                print("\n")
                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
                    #print("item in splitting bucket...",item)
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
                self.stats.split_count += 1  
                # post split, check if next level now
                if self.num_buckets == 2**(self.level+1):
                    print("incrementing level")
                    print(self.num_buckets) 
                    self.level += 1
                    self.ptr = 0

        return split_occured 

######################################################################### CASE 2 ############################################################# 

    def case_2_insert(self, num):
        split_occured = False
        print("in case 2")
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 

            # if the number of overflow buckets is >= size_limit  ----- > create new bucket, rehash, level up, reset ptr 
            if self.get_current_capacity_ratio() >=  self.size_limit:  
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
                self.num_buckets += 1 # dont know abt this 
                split_occured = True
                self.stats.split_count += 1  

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

            # if the current capacity is >= size_limit  ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.get_current_capacity_ratio() >= self.size_limit:
                # print("spliiting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]
                print("splitting bucket: ", self.ptr)
                print("\n")
                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
                    #print("item in splitting bucket...",item)
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
                self.stats.split_count += 1  
                # post split, check if next level now
                if self.num_buckets == 2**(self.level+1):
                    print("incrementing level")
                    print(self.num_buckets) 
                    self.level += 1
                    self.ptr = 0

        return split_occured 


############################################################################### CASE 3 ##############################################################

    def case_3_insert(self, num):
        split_occured = False
        print("in case 3")
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 
            # if there is an overflow for bucket that would be split  ----- > create new bucket, rehash, level up, reset ptr 
            if self.isOverflowedRightNow(self.ptr) == True:  
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
                self.stats.split_count += 1  

                # self.isOverflowedRightNow()   # MUST RECHECK    WORKS FINE WITHOUT @@@@@@@@@@@@ TAKE OUT TEMP 

        # for other levels
        else: 
            print("else", num)
            print("Level is: ", self.level)
            
            ############ INSERT NUMBER INTO BUCKET ############
            num_as_bin = bin(num)[2:]
            
            bucket_key = None 
            if len(num_as_bin) <= self.level:
                ht_index_try_1 = num
                if ht_index_try_1 in self.hash_table:
                    self.hash_table[ht_index_try_1].append(num)
                    bucket_key = ht_index_try_1
                else:
                    print("cant find matching bucket")

            # number as binary is necessarily >= 2 
            else: 
                bigger_last_bits = num_as_bin[-1: -(self.level + 2) : -1][::-1]
                smaller_last_bits = num_as_bin[-1: -(self.level + 1) : -1][::-1]
                if int(bigger_last_bits, 2) in self.hash_table:
                    self.hash_table[int(bigger_last_bits,2)].append(num)
                    bucket_key = int(bigger_last_bits,2)
                elif int(smaller_last_bits, 2) in self.hash_table:
                    self.hash_table[int(smaller_last_bits,2)].append(num) 
                    bucket_key = int(smaller_last_bits,2)
                else:
                    print("problem. number is....:", num, bigger_last_bits, smaller_last_bits)

            # if there is an overflow for bucket that would be split ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.isOverflowedRightNow(self.ptr) == True:
                # print("spliiting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]
                print("spliting bucket: ", self.ptr)
                print("\n")
                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
                    # print("item in splitting bucket...",item)
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
                self.stats.split_count += 1 
                # post split, check if next level now
                if self.num_buckets == 2**(self.level+1):
                    print("incrementing level")
                    print(self.num_buckets) 
                    self.level += 1
                    self.ptr = 0
 
        return split_occured 


    ############################################################## Search #################################################################
    def Search(self, num_to_find):
        num_as_bin = bin(num_to_find)[2:]
        pages_accessed = 0

        # 1 bucket only. Level 0 
        if self.level == 0:
            # if the bucket is empty return 0. still have to read one page 
            if len(self.hash_table[0]) == 0:
                self.stats.access += 1 
                return 0
            else:
                for i, item in enumerate(self.hash_table[0]):
                    if item == num_to_find:
                        pages_accessed = int(math.ceil((i + 1) / self.page_size))
                        self.stats.access += pages_accessed 
                        return pages_accessed
                # number not found in bucket 
                self.stats.access += int(math.ceil(len(self.hash_table[0]) / self.page_size))
                return -1 * int(math.ceil(len(self.hash_table[0]) / self.page_size))
        
        # level >= 1         
        else:
            # bucket_key = None 
            if len(num_as_bin) <= self.level:
                ht_index_try_1 = num_to_find
                if ht_index_try_1 in self.hash_table:
                    # if the bucket to be searched is empty, return 0. still must read 1 page 
                    if len(self.hash_table[ht_index_try_1]) == 0:
                        self.stats.access += 1 
                        return 0
                    else:
                        for i, item in enumerate(self.hash_table[ht_index_try_1]):
                            if item == num_to_find:
                                pages_accessed = int(math.ceil((i + 1) / self.page_size))
                                self.stats.access += pages_accessed  
                                return pages_accessed

                        # number not found in bucket
                        self.stats.access += int(math.ceil(len(self.hash_table[ht_index_try_1]) / self.page_size))
                        return -1 * int(math.ceil(len(self.hash_table[ht_index_try_1]) / self.page_size))
                    
                else:
                    print("in search. cant find matching bucket key")

            # number as binary is necessarily >= 2 
            else: 
                bigger_last_bits = num_as_bin[-1: -(self.level + 2) : -1][::-1]
                smaller_last_bits = num_as_bin[-1: -(self.level + 1) : -1][::-1]
                if int(bigger_last_bits, 2) in self.hash_table:
                    # if the bucket to be searched is empty, return 0. takes 1 access to read page  
                    if len(self.hash_table[int(bigger_last_bits, 2)]) == 0:
                        self.stats.access += 1 
                        return 0
                    else:
                        for i, item in enumerate(self.hash_table[int(bigger_last_bits, 2)]):
                            if item == num_to_find:
                                pages_accessed = int(math.ceil((i + 1) / self.page_size))
                                self.stats.access += pages_accessed  
                                return pages_accessed

                        # number not found in bucket
                        self.stats.access += int(math.ceil(len(self.hash_table[int(bigger_last_bits, 2)]) / self.page_size))
                        return -1 * int(math.ceil(len(self.hash_table[int(bigger_last_bits, 2)]) / self.page_size))
                elif int(smaller_last_bits, 2) in self.hash_table:
                    # if the bucket to be searched is empty, return 0. also 1 read. 
                    if len(self.hash_table[int(smaller_last_bits, 2)]) == 0:
                        self.stats.access += 1 
                        return 0
                    else:
                        for i, item in enumerate(self.hash_table[int(smaller_last_bits, 2)]):
                            if item == num_to_find:
                                pages_accessed = int(math.ceil((i + 1) / self.page_size))
                                self.stats.access += pages_accessed  
                                return pages_accessed

                        # number not found in bucket
                        self.stats.access += int(math.ceil(len(self.hash_table[int(smaller_last_bits, 2)]) / self.page_size))
                        return -1 * int(math.ceil(len(self.hash_table[int(smaller_last_bits, 2)]) / self.page_size))
                    
                else:
                    print("problem. number is....:", num_to_find, bigger_last_bits, smaller_last_bits)
        

    ############################################################## Print to console method #######################################################
    # note: I print -- in between pages / overflow buckets 
    def Print(self):        
        for key in self.hash_table:
            key_binary = bin(key)[2:]
            print("key", key, end = " binary ")
            if (key + (2**(self.level)) in self.hash_table):
                keyStr = key_binary.zfill(self.level + 1)
            else:
                keyStr = key_binary.zfill(self.level)
            print(keyStr, end = " : ")

            count = 0
            for i, item in enumerate(self.hash_table[key]):
                print(item, end = " ") 
                count += 1
                if count == self.page_size and i != len(self.hash_table[key]) - 1:
                    print(" --  ", end = "")
                    count = 0
            print("\n")
        print("Level", self.level)
        print("Ptr", self.ptr)

    #################################################### Print to file object ##########################
    # note: I print -- in between pages / overflow buckets
    def PrintFile(self, fileObj):        
        with open(fileObj, 'w') as f:
            for key in self.hash_table:
                key_binary = bin(key)[2:]
                print("key", key, end = " binary ", file = f)
                if (key + (2**(self.level)) in self.hash_table):
                    keyStr = key_binary.zfill(self.level + 1)
                else:
                    keyStr = key_binary.zfill(self.level)
                print(keyStr, end = " : ", file = f)

                count = 0
                for i, item in enumerate(self.hash_table[key]):
                    print(item, end = " ", file = f) 
                    count += 1
                    if count == self.page_size and i != len(self.hash_table[key]) - 1:
                        print(" --  ", end = "", file = f)
                        count = 0
                print("\n", file = f)
            
            print("Level", self.level, file = f)
            print("Ptr", self.ptr, file = f)

    ####################################################################### Count ####################################################
    # returns number of items in hash table 
    def Count(self):
        # get number of items in the table
        num_items_in_table = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            num_items_in_table += num_items_for_key
        return num_items_in_table

    ####################################################################### ListBucket ##################################################
    # takes an integer representing the key. for ex. 7
    # returns all numbers in the bucket for that key 
    def ListBucket(self, bucket_key):
        if bucket_key in self.hash_table:
            results = self.hash_table[bucket_key]
            return results
        else:
            print("problem in ListBucket...bucket_key passed in as param not a key in hash table")

    ###################################################################### GetStats #################################################
    def GetStats(self):
        return self.stats 



    # use for Case 2 
    def get_current_capacity_ratio(self):
        # get number of items in the table
        num_items_in_table = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            num_items_in_table += num_items_for_key
        
        # get number of pages in table
        page_number = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            if num_items_for_key == 0: ####################################### if no numbers in key, assume it still starts with 1 page ????????????????? VERIFY THIS 
                page_number += 1
            else:
                page_number += int(math.ceil(num_items_for_key / self.page_size)) 

        current_capacity = (num_items_in_table) / (page_number * self.page_size)
        return current_capacity          

        
    def get_num_buckets(self):
        return self.num_buckets 

    def isOverflowedRightNow(self, bucket_key):
        if bucket_key not in self.hash_table:
            print("error...key not in table. can't check for overflow")
        else:
            if len(self.hash_table[bucket_key]) > self.page_size: #overrflow!)
                return True 
            else:
                return False 
            
        '''
        flag = False 
        for key in self.hash_table:
                if len(self.hash_table[key]) > self.page_size: #overrflow!
                    self.is_an_overflow_rn = True
                    flag = True
        if flag == True:
            self.is_an_overflow_rn = True
        else:
            self.is_an_overflow_rn = False 

        '''

    def get_total_number_of_overflow_buckets(self):
        num_overflow = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            if num_items_for_key == 0:
                continue
            overflow_for_that_key = int(math.ceil(num_items_for_key / self.page_size)) - 1
            num_overflow += overflow_for_that_key 

        print("num overflow: ", num_overflow)
        return num_overflow 




    def print_ht(self):
        for key in self.hash_table:
            print("key", key, end = " : ")
            for item in self.hash_table[key]:
                print(item, end = " ") 
            print("\n")


    def testing(self, fileObj, nums_to_insert, nums_to_search):
        with open(fileObj, 'w') as f:
            space_utilization_sum = 0 
            
            # do this test 4 times and find average 
            for i in range(4):
                
                to_insert = nums_to_insert[i]
                for item in to_insert:
                    self.Insert(item)
                
                to_search = nums_to_search[i]
                for item in to_search:
                    self.Search(item)
            
                space_utilization_sum += self.stats.SpaceUtilization() 
            
            average_access = self.stats.access / 4 
            avg_space_utilization = space_utilization_sum / 4 

            print("Average Access: ", average_access, file = f)
            print("Average Space Utilization: ", avg_space_utilization, file = f)

# generate random data sets to use for all tests 
def get_random_test_sets():
    nums_to_insert = []
    nums_to_search_for = []
    # do this test 4 times and find average 
    for i in range(4):
        a_list_insert = []
        a_list_search = []
        # generate and insert 50 random numbers
        for i in range(50):
            random_num = random.randint(0, 100)
            a_list_insert.append(random_num)
        
        # do 20 searches 
        for i in range(20):
            random_num_to_find = random.randint(0,100)
            a_list_search.append(random_num_to_find)
        
        nums_to_insert.append(a_list_insert)
        nums_to_search_for.append(a_list_search)

    return (nums_to_insert, nums_to_search_for)

def get_nearly_uniform_test_sets():

    nums_to_insert = []
    nums_to_search_for = []
    # do this test 4 times and find average 
    for i in range(4):
        a_list_insert = []
        a_list_search = []
        same_random_num = random.randint(0, 100)
        # generate and insert nearly 50 of the same numbers
        for i in range(50):
            if i == 7  or i == 25 or i == 32:
                a_list_insert.append(i)
            else:
                a_list_insert.append(same_random_num)
        
        # do 20 searches 
        for i in range(20):
            random_num_to_find = random.randint(0,100)
            a_list_search.append(random_num_to_find)
        
        nums_to_insert.append(a_list_insert)
        nums_to_search_for.append(a_list_search)

    return (nums_to_insert, nums_to_search_for)

def get_skewed_test_sets():

    nums_to_insert = []
    nums_to_search_for = []
    # do this test 4 times and find average 
    for i in range(4):
        a_list_insert = []
        a_list_search = []
        same_random_num = random.randint(0, 100)
        # generate and insert nearly 50 of the same numbers
        for i in range(50):
            if i == 7  or i == 25 or i == 32:
                a_list_insert.append(i)
            else:
                a_list_insert.append(same_random_num)
        
        # do 20 searches 
        for i in range(20):
            random_num_to_find = random.randint(0,100)
            a_list_search.append(random_num_to_find)
        
        nums_to_insert.append(a_list_insert)
        nums_to_search_for.append(a_list_search)

    return (nums_to_insert, nums_to_search_for)



if __name__ == "__main__":
    # x = LinearHashing(page_size = 2, policy = 0, max_overflow = 2)
    # x = LinearHashing(page_size = 2, policy = 1, max_overflow = 0) # should function same as default case 
    # x = LinearHashing(page_size = 2, policy = 2, size_limit = 0.7)

    #x = LinearHashing(page_size = 3, policy = 0)
    #x.random_testing("./random_test_case_0.txt")


    ##################################################################### Getting skewed distribution testing data ###########################################


    '''
    ###################################################################### Getting nearly uniform distribution testing data #######################################
    (nums_to_insert, nums_to_search) = get_nearly_uniform_test_sets()

    case_0 = LinearHashing(page_size = 3, policy = 0)
    case_1 = LinearHashing(page_size = 3, policy = 1, max_overflow = 5)
    case_2 = LinearHashing(page_size = 3, policy = 2, size_limit = 0.9)
    case_3 = LinearHashing(page_size = 3, policy = 3)
    
    case_0.testing("nearly_uniform_case_0.txt", nums_to_insert, nums_to_search)
    case_1.testing("nearly_uniform_case_1.txt", nums_to_insert, nums_to_search)
    case_2.testing("nearly_uniform_case_2.txt", nums_to_insert, nums_to_search)
    case_3.testing("nearly_uniform_case_3.txt", nums_to_insert, nums_to_search)


    print("done") 

    
    #################################################################### Getting random distribution testing data ###################################################### 
    (nums_to_insert, nums_to_search) = get_random_test_sets()

    case_0 = LinearHashing(page_size = 3, policy = 0)
    case_1 = LinearHashing(page_size = 3, policy = 1, max_overflow = 5)
    case_2 = LinearHashing(page_size = 3, policy = 2, size_limit = 0.9)
    case_3 = LinearHashing(page_size = 3, policy = 3)
    
    case_0.testing("random_case_0.txt", nums_to_insert, nums_to_search)
    case_1.testing("random_case_1.txt", nums_to_insert, nums_to_search)
    case_2.testing("random_case_2.txt", nums_to_insert, nums_to_search)
    case_3.testing("random_case_3.txt", nums_to_insert, nums_to_search)


    print("done") 

    
    x = LinearHashing(page_size = 1, policy = 2, size_limit = 0.7)

    x.insert(23)
    x.insert(22)
    x.insert(47)
    x.Print() 
    print(x.Search(23))
    print(x.Search(1))
    print(x.Search(47))
    print(x.Search(222222))
    
    
    x = LinearHashing(page_size = 2, policy = 3)

    x.Insert(2)
    x.Insert(0)
    x.Insert(1) 
    print("bucket #: ", x.get_num_buckets())
    x.Insert(5)
    print("bucket #: ", x.get_num_buckets())
    x.Insert(23)
    print("bucket #: ", x.get_num_buckets())
    x.Insert(42)
    print("bucket #: ", x.get_num_buckets())
    x.Insert(55)
    print("bucket #: ", x.get_num_buckets())
    x.Insert(10)
    print("bucket #: ", x.get_num_buckets())
    x.print_ht()
    x.Insert(999)
    x.Insert(-13)
    x.Insert(-55)

    # x.print_ht() 
    x.Insert(43) 

    x.print_ht() 
    
    x.Insert(45)
    x.Insert(2328356)
    x.Insert(8) 
    x.Insert(21)
    x.Insert(32)
    x.Insert(2000)
    x.Insert(0)
    x.Insert(1) 
    x.Insert(55)
    x.Insert(-55) 



    #x.print_ht()
    print(" about to print in binary.........")
    #x.Print() 
    x.PrintFile("output2.txt")
    #print(x.Count())
    arr = x.ListBucket(5)
    #print(arr) 

    print(x.Search(45))
    print(x.Search(23)) 
    print(x.Search(950))
    print(x.Search(47))
    print(x.Search(99)) 
    x.Insert(540)

    print()
    x.Print()

    stats_info = x.GetStats()
    print("STATS")

    print("count", stats_info.Count())
    print(stats_info.Buckets())
    print(stats_info.Pages())
    print(stats_info.OverflowBuckets())
    print(stats_info.SplitCount())
    print(stats_info.Access())
    print(stats_info.AccessInsertOnly())
    print(stats_info.SpaceUtilization())

    ''' 



