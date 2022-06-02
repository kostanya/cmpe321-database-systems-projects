import os
import json
from bplustree import *
from manipulation import *


def loadTrees(btrees, types):
    # deserializing json files for b+ trees (in between sessions)
    for filename in os.listdir('.'):
        if filename.endswith('.json'):
            typename = filename[:-5]
            treefile = open(filename, "r")
            treedict = json.load(treefile)

            btrees[typename] = BPlusTree()
            for key in treedict:
                type = types[typename]
                
                if type.fieldHeaders[2*type.pk_order-1] == 'int':
                    btrees[typename].insert(int(key), treedict[key])
                else:
                    btrees[typename].insert(key, treedict[key])

                
            

def saveTrees(btrees):
    for typename in btrees:
        leaves = btrees[typename].traverse()
        # Serializing json 
        json_object = json.dumps(leaves, indent = 4)
    
        # Writing to sample.json
        with open(typename +".json", "w") as f:
            f.write(json_object)



def bufferManager(types):
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

    
        files = []
        # reading the page headers from files 
        for filename in os.listdir('.'):
            if filename.startswith(name) and filename.endswith(".txt"):
                ls = filename.split('.')
                fullname = ls[0]
                fileno = int(fullname[len(name):])
                files.append(fileno)

        files.sort()
        if len(files) > 0:
            end = files[-1]
        else:
            end = 0

        

        idx = 0
        for i in range(1, end+1):
            filename = name + str(i) + ".txt"
            types[name].files.append(filename)

            if files[idx] == i:

                f = open(filename, 'r+')
                byteptr = 3

                # reading disk page by page to ram in order to get the information from the previous sessions
                while True:
                    f.seek(byteptr)
                    currentrecord = f.read(2)

                    f.seek(byteptr + 6)
                    availablerecord = f.read(2)

                    if not availablerecord: 
                        break

                    types[name].no_records.append(int(currentrecord))
                    types[name].available.append(int(availablerecord))
                    byteptr += len_page_bytes

                idx += 1
                f.close()
            else:
                types[name].available.extend([-1]*no_pages_in_file)
                types[name].no_records.extend([0]*no_pages_in_file)


