import os
import math
import csv
import json
from bplustree import *
from sessions import *
from manipulation import *
from definition import *
from parsing import *

len_page_bytes = 256
no_pages_in_file = 32


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
loadTrees(btrees)

parsing("src/input_1.txt", "output.txt", types, btrees)

# saving trees for next sessions
saveTrees(btrees)
