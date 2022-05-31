from bplustree import *
from manipulation import *


def addCatalog(typename, no_fields, pk_order, fieldHeaders):
    sc = open('SystemCatalog.txt', 'a')

    command = ""
    for field in fieldHeaders:
        command += " " + field

    sc.write(typename + " " + str(no_fields)  + " " + str(pk_order) + command + "\n")


def deleteCatalog(name):
    sc = open('SystemCatalog.txt', 'r+')

    lines = []
    for line in sc.readlines():
        lines.append(line)
        fields = line.split()
        if fields[0] == name:
            lines.remove(line)


    sc = open('SystemCatalog.txt', 'w')
    for line in lines:
        sc.write(line)


def createType(name, no_fields, pk_order, fieldHeaders, types, btrees):
    if name not in types.keys():
        #filename = name + ".txt"
        #f = open(filename, 'w')
        #f.close()

        # adding to types dictionary
        types[name] = Type(name, no_fields, pk_order, fieldHeaders)

        # adding to the btrees dictionary
        btrees[name] = BPlusTree()

        # adding to system catalog
        addCatalog(name, no_fields, pk_order, fieldHeaders)
        
        print("type: " + name + " başarıyla yaratıldı")
        return True
    else:
        print("zaten bu type var")
        return False


def deleteType(name, types, btrees):
    # emptying disk memory
    filename = name + ".txt"
    if os.path.exists(filename):
        os.remove(filename)
        print(filename + " has been deleted successfully")
    else:
        print(filename + " does not exist!")

    # deleting the json file that carried information through sessions if it exists
    filename = name + ".json"
    if os.path.exists(filename):
        os.remove(filename)
        print(filename + " has been deleted successfully")
    else:
        print(filename + " does not exist!")

    # deleting the type manager object
    del types[name]

    # deleting the corresponding b+ tree
    del btrees[name]

    # deleting from system catalog
    deleteCatalog(name)

    print("type: " + name + " başarıyla silindi")


def listType(types):
    typelist = ""
    if types.keys():
        for type in types.keys():
            typelist += type + '\n'
        return typelist, True
    else:
        return typelist, False
    
    