import os
import math
import csv
import json
from bplustree import *
from sessions import *
from typeManager import *

len_page_bytes = 256
no_pages_in_file = 32

# storing objects and trees for types created so far

types = {}
btrees = {}


'''catalog = open("systemcatalog.txt", "r")
lines = catalog.readlines()

print(lines)

# loading type objects to memory
for line in lines:
    words = line.split()
    name = words[0]
    no_fields = words[1]
    pk_order = words[2]

    #loading type object to memory to manage types
    types[name] = Type(name, no_fields, pk_order)

    no_pages = words[-1]
    #no_files = 

    # reading the page headers from files '''





    





# loading trees from previous sessions
loadTrees(btrees)


def createType(name, no_fields, pk_order):
    fileName = name + ".txt"
    f = open(fileName, 'w')
    f.close()

    types[name] = Type(name, no_fields, pk_order)

    # added to the btrees dictionary
    btrees[name] = BPlusTree()
    # save bplustree to a file


        




createType("angel", 3, 1)
typename = "angel"


types[typename].createRecord(["a", "b", "c"], btrees)
types[typename].createRecord(["d", "e", "f"], btrees)
types[typename].createRecord(["g", "h", "x"], btrees)
types[typename].createRecord(["f", "c", "v"], btrees)
types[typename].createRecord(["z", "s", "p"], btrees)
types[typename].createRecord(["x", "s", "p"], btrees)
types[typename].createRecord(["w", "s", "p"], btrees)
types[typename].createRecord(["u", "s", "p"], btrees)

#print(types[typename].getLocation(btrees[typename].find("f")["f"]))


types[typename].updateRecord("f", ["f", "updated", "updated"], btrees)
types[typename].updateRecord("g", ["g", "updated", "updated"], btrees)

#types[typename].deleteRecord("a", btrees)
types[typename].deleteRecord("d", btrees)
types[typename].deleteRecord("g", btrees)
#types[typename].deleteRecord("f", btrees)

types[typename].searchRecord("f", btrees)


types[typename].listRecord(btrees)






#types[typename].createRecord(["c", "s", "p"], btrees)


#print(types[typename].pages)

#print(btrees[typename].find("z")["z"])




# btrees[typename].show()
# leaves = btrees[typename].traverse()
# print(leaves)


# saving trees for next sessions
saveTrees(btrees)











