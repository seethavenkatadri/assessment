# Given 2 lists, get the row wise common items in them. Provide a solution which should scale to very large lists by using many CPUs
#
#
#
# For example,
# list1 = [[1, 3, 5], [5, 6, 7, 8], [10, 11, 12], [20, 21]]
# list2 = [[2, 3, 4, 5], [6, 9, 10], [11, 12, 13, 14], [21, 24, 25]]
# Output:
# [[3, 5], [6], [11, 12], [21]]

import multiprocessing as mp

# Using a queue to ensure ordering in the results
output = mp.Queue()

def len_check(list1,list2):
    if len(list1) != len(list2):
        print('Both lists should be of same length')
        return
    else:
        print('Length checked.. Proceeding..')

def element_intersection(x,y):
    # adds the intersection result to output queue
    output.put(list(x & y))

if __name__ == "__main__":
    list1 = [[1, 3, 5], [5, 6, 7, 8], [10, 11, 12], [20, 21]]
    list2 = [[2, 3, 4, 5], [6, 9, 10], [11, 12, 13, 14], [21, 24, 25]]
    len_check(list1,list2)
    result=[]


    processes =[]

    # Creates multiple processes
    processes =[mp.Process(target=element_intersection, args=(set(list1[i]),set(list2[i]))) for i in range(len(list1))]

    # Start processes
    for p in processes:
        p.start()

    # Exit the processes
    for p in processes:
        p.join()

    # Get process results from the output queue
    result = [output.get() for p in processes]

    print(result)