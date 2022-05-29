import os
import math
import csv
import json
import jsonpickle
from bplustree import *



len_recordHeader = 1
len_pageHeader = 15
len_page_bytes = 2048
no_pages_in_file = 32


# storing objects and trees for types created so far

types = {}
btrees = {}


def loadTrees():
    # deserializing json files for b+ trees (in between sessions)
    for filename in os.listdir('.'):
        if filename.endswith('.json'):
            typename = filename[:-5]
            treefile = open(filename, "r")
            treedict = json.load(treefile)

            btrees[typename] = BPlusTree()
            for key in treedict:
                btrees[typename].insert(key, treedict[key])
            
            btrees[typename].show()

        

def saveTrees():
    for typename in btrees:
        leaves = btrees[typename].traverse()
        # Serializing json 
        json_object = json.dumps(leaves, indent = 4)
    
        # Writing to sample.json
        with open(typename +".json", "w") as f:
            f.write(json_object)



def createType(name, no_fields, pk_order, fields):
    fileName = name + ".txt"
    f = open(fileName, 'w')
    f.close()

    type = Type(name, no_fields, pk_order, fields)
    types[name] = type

    # added to the btrees dictionary
    btrees[name] = BPlusTree()
    # save bplustree to a file

class Type:
    def __init__(self, name, no_fields, pk_order, fieldHeaders):
        self.name = name
        self.no_fields = no_fields
        self.pk_order = pk_order
        self.fieldHeaders = fieldHeaders 
        self.pages = [] # keeping index of available records
        self.fileName = name + ".txt"
        self.record_length = (len_recordHeader + no_fields*20 + 2)
        self.max_records = math.floor((len_page_bytes - len_pageHeader) / self.record_length)

    # each type has exactly one base file
    # if the current file gets full then new file should be opened

    # this is used for create record
    def findAvailableIndex(self):
        
        for pageno, page in enumerate(self.pages):
            # if page is full
            if not page:
                pass
            else:
                index = page[0]
                page.pop(0)
                return pageno+1, index
        
        if len(self.pages) == no_pages_in_file: # current file is full
            pass
            # new file
        else: #creating new page
            self.pages.append([i+1 for i in range(self.max_records)])
            startbyte = len_page_bytes*(len(self.pages)-1)

            f = open(self.fileName, 'r+')
            f.seek(startbyte)
            # writing page header manually
            f.write("$$$$$$$$$$$$$\n")
            f.close()

            index = self.pages[-1][0]
            self.pages[-1].pop(0)
            return len(self.pages), index




    def createRecord(self, fields):
        f = open(self.fileName, 'r+')

        # bunu nereye yazacaz --> file manager
        address = self.findAvailableIndex()
        pageno = address[0]
        index = address[1]

        startbyte = len_page_bytes*(pageno-1) + len_pageHeader + self.record_length*(index-1)
        f.seek(startbyte)
        # manuel record header entry
        f.write("0")

        for field in fields:
            f.write(field.ljust(20))

        f.write("\n")
        f.close()

        #rid = 
        # open bplustree from the corresponding file
        # angel.json load
        # build the tree from scratch with regard to information in the file

        # new insert
        pk = fields[self.pk_order-1]

        bplustree = btrees[self.name] 
        # inserting <key, value: closest starting byte to the beginning of the file>
        bplustree.insert(pk, startbyte)
    
        






createType("angel", 3, 1, ["modric", "casemiro", "rodrigo"])
typename = "angel"
types[typename].createRecord(["a", "b", "c"])
types[typename].createRecord(["d", "e", "f"])
types[typename].createRecord(["g", "h", "x"])
types[typename].createRecord(["f", "c", "v"])
types[typename].createRecord(["z", "s", "p"])

# btrees[typename].show()
# leaves = btrees[typename].traverse()
# print(leaves)











