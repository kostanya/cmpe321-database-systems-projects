import os
import math
import csv
import json
from bplustree import *
from sessions import *
from manipulation import *
from definition import *
from parsing import *

# always check if systemcatalog exists,
# if not create
if os.path.exists("SystemCatalog.txt"):
    pass
else:
    f = open("SystemCatalog.txt", 'w')
    f.close()


# storing objects and trees for types created so far
types = {}
btrees = {}

# reading disk to RAM page by page to get information from previous sessions
diskToRam(types)

# loading trees from previous sessions
loadTrees(btrees, types)

parsing("src/input.txt", "output.txt", types, btrees)

# saving trees for next sessions
saveTrees(btrees)
