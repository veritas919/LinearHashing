from lh import LinearHashing


if __name__ == "__main__":

    # create linear hashing object 
    x = LinearHashing(page_size = 3, policy = 3) 

    # the lines below show a few configuration options for the LinearHashing object 
    # x = LinearHashing(page_size = 5, policy = 0)
    # x = LinearHashing(page_size = 3, policy = 1, max_overflow = 5)
    # x = LinearHashing(page_size = 2, policy = 2, size_limit = 0.7)

    # insert numbers into the hash table 
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

    # print contents of hash table as well as the level and pointer to a file 
    x.PrintFile("./data/table_content/hash_table_1.txt")  

    # search hash table for number specified and print the number of pages searched to find the specified number in the hash table 
    print(x.Search(45))
    print(x.Search(23)) 
    print(x.Search(950))
    print(x.Search(2))
    print(x.Search(99)) 

    # print hash table contents to console 
    x.Print()

    # get stats 
    stats_info = x.GetStats()

    # print stats to console 
    print("~~~~~~~~~~STATS~~~~~~~~~~~~~")
    print("count", stats_info.Count())
    print("main buckets", stats_info.Buckets())
    print("number of pages", stats_info.Pages())
    print("overflow buckets", stats_info.OverflowBuckets())
    print("number of splits", stats_info.SplitCount())
    print("access count", stats_info.Access())
    print("access count during insert only", stats_info.AccessInsertOnly())
    print("space utilization", stats_info.SpaceUtilization())
