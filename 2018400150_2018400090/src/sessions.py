import os
import json
from bplustree import *


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
            
            btrees[typename].show()

        

def saveTrees(btrees):
    for typename in btrees:
        leaves = btrees[typename].traverse()
        # Serializing json 
        json_object = json.dumps(leaves, indent = 4)
    
        # Writing to sample.json
        with open(typename +".json", "w") as f:
            f.write(json_object)