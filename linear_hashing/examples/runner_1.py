from lh import LinearHashing

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


    # x.PrintFile("output2.txt")
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