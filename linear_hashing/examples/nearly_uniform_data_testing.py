from lh import LinearHashing
from test_set_generator import get_nearly_uniform_test_sets


if __name__ == "__main__":

    (nums_to_insert, nums_to_search) = get_nearly_uniform_test_sets()

    case_0 = LinearHashing(page_size = 3, policy = 0)
    case_1 = LinearHashing(page_size = 3, policy = 1, max_overflow = 5)
    case_2 = LinearHashing(page_size = 3, policy = 2, size_limit = 0.9)
    case_3 = LinearHashing(page_size = 3, policy = 3)
    
    case_0.testing("./data/nearly_uniform/case_0.txt", nums_to_insert, nums_to_search)
    case_1.testing("./data/nearly_uniform/case_1.txt", nums_to_insert, nums_to_search)
    case_2.testing("./data/nearly_uniform/case_2.txt", nums_to_insert, nums_to_search)
    case_3.testing("./data/nearly_uniform/case_3.txt", nums_to_insert, nums_to_search)


    print("done") 