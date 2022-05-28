import os
import math

len_recordHeader = 1
len_pageHeader = 15
len_page_bytes = 2048
no_pages_in_file = 10

class FileManager:

    def __init__(self, name, no_fields):
        self.no_file = 1

        self.fileNames = []
        fileName = name + str(self.no_file -1) + ".txt"
        self.fileNames.append(fileName)
        f = open(fileName, 'a')
        f.close()

        s = (len_page_bytes - len_pageHeader) / (len_recordHeader + no_fields*20 + 2)
        self.no_records = math.floor(s)

    def createNewFile():
        self.no_file += 1
        fileName = name + str(self.no_file -1) + ".txt"
        self.fileNames.append(fileName)
        f = open(fileName, 'a')
        self.file = f
        f.close()

    def insertRecord(self, fields):
        search = True
        i = -1
        while search:
            if i < len(self.fileNames):
                i += 1
            f = open(self.fileNames[i], 'r')

            if os.stat(self.fileNames[i]).st_size == 0:
                self.createPage(self.fileNames[i], i, 0)

            for k in range(no_pages_in_file):
                f.seek(2 + 2048*k)
                byte = f.read(1)
                if byte == "0":
                    page = k
                    search = False
                    break
                elif byte == "":
                    self.createPage(self.fileNames[i], i, k)


        # 0,0 
        
        f = open(self.fileNames[i], 'a+')
        f.write("0")
        for field in fields:
            f.write(field.ljust(20))
        f.write("\n")
        self.updatePageHeader(self.fileNames[i], i, k, 0)


    def createPage(self, fileName, fileNum, pageNum):
        f = open(fileName, 'a')
        f.seek(len_page_bytes*pageNum)
        f.write("$ 0 "+str(pageNum)+" "+str(self.no_records)+" 00 "+str(fileNum)+"\n")

    # type: 0 if inserted a new record 1 if deleted a new record
    def updatePageHeader(self, fileName, fileNum, pageNum, type):
        if type == 0:
            f = open(fileName, 'a')
            f.seek(len_page_bytes*pageNum)
            f.write("$ 0 "+str(pageNum)+" "+str(self.no_records)+" 01 "+str(fileNum)+"\n")

class Type:
    def __init__(self, name, no_fields, pk_order, fields):
        self.name = name
        self.no_fields = no_fields
        self.pk_order = pk_order
        self.fields = fields
        
        self.fileManager = FileManager(name, no_fields)

# name: type-name (str)
# no_fields: number of fields (int)
# pk_order: primary key orde (int)
# fields: a list contains tuples (field name,field type)
def createType(name, no_fields, pk_order, fields):
    t = Type(name, no_fields, pk_order, fields)
    types.append(t)

    # add to System catalog
    # create the b+tree

# name: type-name (str)
def deleteType(name):
    for i in range(len(types)):
        if types[i].name == name:
            index = i
    t = types[i]
    for i in range(t.fileManager.no_file):
        os.remove(t.fileManager.fileNames[i])
    types.remove(t)

    #also remove the relevant b+tree

def listType():
    for i in range(len(types)):
        print(types[i].name)

# name: type-name (str)
# fields: a list contains field values
def createRecord(typeName, fields):
    for i in range(len(types)):
        if types[i].name == typeName:
            index = i
    t = types[index]

    rid = t.fileManager.insertRecord(fields)

    # insert b+tree with this rid.

# Take the input and call necessary functions. 

types = [] # use system catalog instead of this


createType("angel", 3, 1, [("name","str"),("alias", "str"),("affiliation","str")])
createType("evil", 10, 1, [("name", "str"), ("type", "str"), ("alias", "str"), ("spell", "str")])
createRecord("angel", ["Tyrael", "ArchangelOfJustice", "HighHeavens"])

#deleteType("angel")
#listType()