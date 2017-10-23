import itertools

# Taking input from user for support, confidence and filename.
support = int(raw_input("Enter the Minimum Support Value %: "))
confidence = int(raw_input("Enter the Minimum Confidence Value %: "))
filename = raw_input("Enter the name for the Database: ")

# Initializing Variables
collections = {}
transactions = 0
data_set = []
transaction_list = []
f = open(filename, "r")
for line in f:
    transaction_list = []
    transactions += 1
    for word in line.split():
        transaction_list.append(word)
        if word not in collections.keys():
            collections[word] = 1
        else:
            count = collections[word]
            collections[word] = count + 1
    data_set.append(transaction_list)

# Printing the Database
print "--------------DATABASE-------------------"
for i in data_set:
    print i
print"------------------------------------------"
# Computing 1st Frequent Item Set
first_frequent_list = []
for key in collections:
    if (100 * collections[key]/transactions) >= support:
        element_list = []
        element_list.append(key)
        first_frequent_list.append(element_list)


# Defining the Apriori Algorithm
def apriori_gen(frequent_item_dataset, k):
    length = k
    result = []
    for list1 in frequent_item_dataset:
        for list2 in frequent_item_dataset:
            counter = 0
            c = []
            if list1 != list2:
                while counter < length-1:
                    if list1[counter] != list2[counter]:
                        break
                    else:
                        counter += 1
                else:
                    if list1[length-1] < list2[length-1]:
                        for item in list1:
                            c.append(item)
                        c.append(list2[length-1])
                        if not infrequent_item_set(c, frequent_item_dataset, k):
                            result.append(c)

    return result


# Function to compute subset of Superset
def findsubsets(super_set, m):
    return set(itertools.combinations(super_set, m))


# Removing infrequent items from the subset.
def infrequent_item_set(c, least_frequent_list, k):
    infrequent_list = findsubsets(c, k)
    for item in infrequent_list:
        s = []
        for l in item:
            s.append(l)
        s.sort()
        if s not in least_frequent_list:
            return True
    return False


# Calculating Frequent ItemSets
def frequent_itemsets():
    k = 2
    least_fq = []
    frequent_list = []
    for item in first_frequent_list:
        least_fq.append(item)
    while least_fq != []:
        least_frequent_items = []
        apriori_result = apriori_gen(least_fq, k-1)

        for c in apriori_result:
            counter_a = 0
            transact = 0
            s = set(c)
            for transaction_lists in data_set:
                transact += 1
                t = set(transaction_lists)
                if s.issubset(t):
                    counter_a += 1
            if (100 * counter_a/transact) >= support:
                c.sort()
                least_frequent_items.append(c)
        least_fq = []
        for l in least_frequent_items:
            least_fq.append(l)
        k += 1
        if least_frequent_items != []:
            frequent_list.append(least_frequent_items)
    return frequent_list


# Generation Association Rules
def generating_association_rules():
    num = 1
    list_of_frequent_items = frequent_itemsets()
    print "--------------------------------------------------------"
    print "                ASSOCIATION RULES                       "
    print "--------------------------------------------------------"
    for iq in list_of_frequent_items:
        for l in iq:
            length = len(l)
            counter = 1
            while counter < length:
                r = findsubsets(l, counter)
                counter += 1
                for item in r:
                    inc1 = 0
                    inc2 = 0
                    s = []
                    m = []
                    for j in item:
                        s.append(j)
                    for k in data_set:
                        if set(s).issubset(set(k)):
                            inc1 += 1
                        if set(l).issubset(set(k)):
                            inc2 += 1
                    if 100*inc2/inc1 >= confidence:
                        for index in l:
                            if index not in s:
                                m.append(index)
                        print "Rule#  %d : %s ==> %s %d  %d " % (num, s, m, 100*inc2/len(data_set), 100*inc2/inc1)
                        num += 1


generating_association_rules()
print "--------------------------------------------------------"
