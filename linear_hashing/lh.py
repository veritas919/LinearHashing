import copy 
import math 
import random 

from lh_stats import LinearHashingStats 
     
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

        self.is_an_overflow_rn = False 
        self.num_buckets_overflowing = 0    
        self.num_buckets = 1 # keeping track of main buckets....NOT overflow. used to det to level up   

        self.hash_table = {}
        self.hash_table [0] = []

        self.stats = LinearHashingStats(hash_table=self.hash_table, page_size=self.page_size) 

    ########################################################################## GENERAL INSERT ####################################
    def general_insert(self, num):
        split_occured = False
        self.stats.access_insert_only += 1 
        self.stats.access += 1 
        
        # for level 0 
        if self.level == 0:
            # Insert number 
            self.hash_table[0].append(num) # add number 
             
            # check for split condition  ----- > create new bucket, rehash, level up, reset ptr 
            if self.check(self.policy) == True: 
                self.hash_table[1] = [] # create new bucket 

                copy_of_bucket_0 = copy.deepcopy(self.hash_table[0])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_0:
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
 

        # for other levels
        else:             
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


            # if split condition holds  ----- > create new bucket, rehash, move ptr. Check if leveling up, and if so, reset ptr
            if self.check(bucket_key) == True:
                # print("spliting bucket: ", )
                bin_of_ptr =  bin(self.ptr)[2:]

                new_bucket_value_0 = self.ptr
                new_bucket_value_1 = self.ptr + 2**(self.level)

                # rehash 
                copy_of_bucket_being_split = copy.deepcopy(self.hash_table[self.ptr])
                bucket_0 = []
                bucket_1 = []
                for item in copy_of_bucket_being_split:
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
                    self.level += 1
                    self.ptr = 0

                
        return split_occured 
    ################################################### Checks Splitting Condition Based on Policy ##############################
    def check(self, bucket_key):
        if self.policy == 0:
            if self.level == 0:
                if self.is_overflowed_right_now(0):
                    return True
            else:
                if self.is_overflowed_right_now(bucket_key):
                    return True 
        
        elif self.policy == 1:
            if self.get_total_number_of_overflow_buckets() >= self.max_overflow:
                return True
        
        elif self.policy == 2:
            if self.get_current_capacity_ratio() >= self.size_limit:
                return True
        
        elif self.policy == 3:
            if self.is_overflowed_right_now(self.ptr) == True:
                return True

        return False           

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

    ##################################################################### HELPER FUNCTIONS ############################################

    # use for determining when to split for policy 2 
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
            if num_items_for_key == 0: # if no numbers in key, assume we still must read 1 page 
                page_number += 1
            else:
                page_number += int(math.ceil(num_items_for_key / self.page_size)) 

        current_capacity = (num_items_in_table) / (page_number * self.page_size)
        return current_capacity          

        
    def get_num_buckets(self):
        return self.num_buckets 

    def is_overflowed_right_now(self, bucket_key):
        if bucket_key not in self.hash_table:
            print("error...key not in table. can't check for overflow")
        else:
            if len(self.hash_table[bucket_key]) > self.page_size: #overrflow!
                return True 
            else:
                return False 
            

    def get_total_number_of_overflow_buckets(self):
        num_overflow = 0
        for key in self.hash_table:
            num_items_for_key = len(self.hash_table[key])
            if num_items_for_key == 0:
                continue
            overflow_for_that_key = int(math.ceil(num_items_for_key / self.page_size)) - 1
            num_overflow += overflow_for_that_key 

        #print("num overflow: ", num_overflow)
        return num_overflow 

    # my own print method. not to be utilized for assesment. 
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

if __name__ == "__main__":
    # x = LinearHashing(page_size = 5, policy = 0)
    # x = LinearHashing(page_size = 3, policy = 1, max_overflow = 5)
    # x = LinearHashing(page_size = 2, policy = 2, size_limit = 0.7)
    x = LinearHashing(page_size = 3, policy = 3)

    x.general_insert(2)
    x.general_insert(0)
    x.general_insert(1) 
    x.general_insert(5)
    x.general_insert(23)
    x.general_insert(42)
    x.general_insert(55)
    x.general_insert(10)

    x.general_insert(22)
    x.general_insert(100)
    x.general_insert(95) 
    x.general_insert(46)
    x.general_insert(23)
    x.general_insert(240)
    x.general_insert(111)
    x.general_insert(42)


    x.PrintFile("output2.txt")
    arr = x.ListBucket(1)
    print(arr)

    print(x.Search(45))
    print(x.Search(23)) 
    print(x.Search(950))
    print(x.Search(2))
    print(x.Search(99)) 

    x.Print()

    stats_info = x.GetStats()
    print("~~~~~~~~~~STATS~~~~~~~~~~~~~")

    print("count", stats_info.Count())
    print("main buckets", stats_info.Buckets())
    print("number of pages", stats_info.Pages())
    print("overflow buckets", stats_info.OverflowBuckets())
    print("number of splits", stats_info.SplitCount())
    print("access count", stats_info.Access())
    print("access count during insert only", stats_info.AccessInsertOnly())
    print("space utilization", stats_info.SpaceUtilization())

'''
    ##################################################################### Getting skewed distribution testing data ###########################################

    (nums_to_insert, nums_to_search) = get_skewed_test_sets()

    case_0 = LinearHashing(page_size = 3, policy = 0)
    case_1 = LinearHashing(page_size = 3, policy = 1, max_overflow = 5)
    case_2 = LinearHashing(page_size = 3, policy = 2, size_limit = 0.9)
    case_3 = LinearHashing(page_size = 3, policy = 3)
    
    case_0.testing("skewed_case_0.txt", nums_to_insert, nums_to_search)
    case_1.testing("skewed_case_1.txt", nums_to_insert, nums_to_search)
    case_2.testing("skewed_case_2.txt", nums_to_insert, nums_to_search)
    case_3.testing("skewed_case_3.txt", nums_to_insert, nums_to_search)


    print("done") 

    
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
    
    '''
    

