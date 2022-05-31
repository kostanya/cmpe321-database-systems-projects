import os
import json
from bplustree import *
from manipulation import *


def loadTrees(btrees):
    # deserializing json files for b+ trees (in between sessions)
    for filename in os.listdir('.'):
        if filename.endswith('.json'):
            typename = filename[:-5]
            treefile = open(filename, "r")
            treedict = json.load(treefile)

            btrees[typename] = BPlusTree()
            for key in treedict:
                btrees[typename].insert(key, treedict[key])
            

        

def saveTrees(btrees):
    for typename in btrees:
        leaves = btrees[typename].traverse()
        # Serializing json 
        json_object = json.dumps(leaves, indent = 4)
    
        # Writing to sample.json
        with open(typename +".json", "w") as f:
            f.write(json_object)



def diskToRam(types):
    catalog = open("SystemCatalog.txt", "r")
    lines = catalog.readlines()


    # loading type objects to memory
    for line in lines:
        words = line.split()
        name = words[0]
        no_fields = int(words[1])
        pk_order = int(words[2])

        # assuming line is proper
        fieldHeaders = []
        for header in words[3:]:
            fieldHeaders.append(header)
        
        
        #loading type object to memory to manage types
        types[name] = Type(name, no_fields, pk_order, fieldHeaders)

    
        # reading the page headers from files 
        filename = name + ".txt"
        f = open(filename, 'r+')
        byteptr = 9

        # reading disk page by page to ram in order to get the information from the previous sessions
        while True:
            f.seek(byteptr)
            availablerecord = f.read(2)
            if not availablerecord:
                break

            types[name].pages.append(int(availablerecord))
            byteptr += len_page_bytes

        
        f.close()
        #print(types[name].pages)
