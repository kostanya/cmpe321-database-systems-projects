import os
import sys
import math
import csv
import json
import sys
from bplustree import *
from sessions import *
from manipulation import *
from definition import *
from parsing import *

# always check if the systemcatalog exists,
# if not create
if os.path.exists("SystemCatalog.txt"):
    pass
else:
    f = open("SystemCatalog.txt", 'w')
    f.close()


# storing objects and trees for types created so far
types = {}
btrees = {}

# reading disk to RAM 
bufferManager(types)

# loading trees from previous sessions
loadTrees(btrees, types)

input = sys.argv[1]
output = sys.argv[2]
parsing(input, output, types, btrees)

# saving trees for next sessions
saveTrees(btrees)
