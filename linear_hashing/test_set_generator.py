import math 
import random 
from scipy.stats import skewnorm          # used for generating skewed distribution

# https://stackoverflow.com/questions/24854965/create-random-numbers-with-left-skewed-probability-distribution
# referenced  above site for generating skewed dataset

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

# generate nearly uniformly distributed test data sets 
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

# generate skewed data sets 
def get_skewed_test_sets():

    nums_to_insert = []
    nums_to_search_for = []
    # do this test 4 times and find average 
    for i in range(4):
        a_list_insert = []
        a_list_search = []
        
        # generate skewed data. skewed left 10 
        data = skewnorm.rvs(a = 10, size = 50, scale = 1)   # uncomment line that imports skewnorm at top if you want to run this 
        data = data - min(data)
        data = data / max(data)
        data = data * 100 # data <= 100 
        for item in data:
            a_list_insert.append(math.floor(item))
        
        # do 20 searches 
        for i in range(20):
            random_num_to_find = random.randint(0,100)
            a_list_search.append(random_num_to_find)
        
        nums_to_insert.append(a_list_insert)
        nums_to_search_for.append(a_list_search)

    return (nums_to_insert, nums_to_search_for)