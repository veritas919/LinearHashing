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

