import csv
import time
from definition import *
from manipulation import *

log = open('horadrimLog.csv', 'a', newline="")
writer = csv. writer(log)

def parsing(inputFile, outputFile, types, btrees):
    input = open(inputFile, 'r')
    output = open(outputFile, 'a')

    for line in input.readlines():
        if line == "\n":
            pass
        else:
            parse = line.split()
            if parse[0] == "create":
                if parse[1] == "type":
                    # create type <type-name><number-of-fields><primary-key-order><field1-name><field1-type><field2-name>..
                    name = parse[2]
                    no_fields = parse[3]
                    pk_order = parse[4]

                    # no_fields < pk_order
                    if no_fields < pk_order:
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])
                    elif len(parse)-5 != 2*int(no_fields) :
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])
                    else:
                        fieldHeaders = []
                        for i in range(2*int(no_fields)):
                            fieldHeaders.append(parse[i+5])

                        check = createType(name, int(no_fields), int(pk_order), fieldHeaders, types, btrees)
                        if check:
                            writer.writerow([int(time.time()), line.rstrip(), "success"])
                        else:
                            writer.writerow([int(time.time()), line.rstrip(), "failure"])

                elif parse[1] == "record":
                    # create record <type-name><field1-value><field2-value>... 
                    typename = parse[2]

                    if typename in types.keys():
                        type = types[typename]
                        if len(parse)-3 == int(type.no_fields):
                            fields = []
                            for i in range(type.no_fields):  
                                fields.append(parse[i+3])

                            def checkInt(str):
                                if str[0] in ('-', '+'):
                                    return str[1:].isdigit()
                                return str.isdigit()

                            # type - int error
                            typerror = False
                            for i, header in enumerate(type.fieldHeaders):
                                if i%2==1:
                                    this = parse[(i+1)//2+2]
                                    if header == 'int' and not checkInt(this):
                                        writer.writerow([int(time.time()), line.rstrip(), "failure"])
                                        typerror = True
                                        break
                                        
                            if not typerror:
                                check = type.createRecord(fields, btrees)
                                if check:
                                    writer.writerow([int(time.time()), line.rstrip(), "success"])
                                else:
                                    # pk conflict
                                    writer.writerow([int(time.time()), line.rstrip(), "failure"])
                        else:
                            # required number of fields is not equal to entered fields
                            writer.writerow([int(time.time()), line.rstrip(), "failure"])
                    else:
                        # given type does not exist
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])

                    
            elif parse[0] == "delete":
                if parse[1] == "type":
                    # delete type <type-name> 
                    typename = parse[2]

                    if typename in types.keys():
                        deleteType(typename, types, btrees)
                        writer.writerow([int(time.time()), line.rstrip(), "success"])
                    else:
                        # given type does not exist
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])

                if parse[1] == "record":
                    # delete record <type-name><primary-key>
                    typename = parse[2]
                    pk = parse[3]

                    if typename in types.keys():
                        type = types[typename]
                        check = type.deleteRecord(pk, btrees)

                        if check:
                            writer.writerow([int(time.time()), line.rstrip(), "success"])
                        else:
                            # pk conflict
                            writer.writerow([int(time.time()), line.rstrip(), "failure"])
                    else:
                        # given type does not exist
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])

            elif parse[0] == "list": 
                if parse[1] == "type":
                    # list type
                    check = listType(types)
                    if check[1]:
                        output.write(check[0])
                        writer.writerow([int(time.time()), line.rstrip(), "success"])
                    else:
                        # list is empty
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])
                

                if parse[1] == "record":
                    # list record <type-name>
                    typename = parse[2]
                    if typename in types.keys():
                        type = types[typename]
                        check = type.listRecord(btrees)
                        if check[1]:
                            output.write(check[0])
                            writer.writerow([int(time.time()), line.rstrip(), "success"])
                        else:
                            # there is no record for the given type
                            writer.writerow([int(time.time()), line.rstrip(), "failure"])
                    else:
                        # given type does not exist
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])

            elif parse[0] == "search":
                # search record <type-name><primary-key>
                typename = parse[2]
                pk = parse[3]

                if typename in types.keys():
                    type = types[typename]
                    check = type.searchRecord(pk, btrees)

                    if check[1]:
                        output.write(check[0])
                        writer.writerow([int(time.time()), line.rstrip(), "success"])
                    else:
                        # given pk does not exist
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])
                else:
                    # given type does not exist
                    writer.writerow([int(time.time()), line.rstrip(), "failure"])

            elif parse[0] == "update":
                # update record <type-name><primary-key><field1-value><field2-value>... 
                typename = parse[2]
                pk = parse[3]

                if typename in types.keys():
                    type = types[typename]

                    if len(parse)-4 == int(type.no_fields):
                        fields = []
                        for i in range(type.no_fields):  
                            fields.append(parse[i+4])

                        def checkInt(str):
                            if str[0] in ('-', '+'):
                                return str[1:].isdigit()
                            return str.isdigit()

                        # type - int error
                        typerror = False
                        for i, header in enumerate(type.fieldHeaders):
                            if i%2==1:
                                this = parse[(i+1)//2+3]
                                if header == 'int' and not checkInt(this):
                                    writer.writerow([int(time.time()), line.rstrip(), "failure"])
                                    typerror = True
                                    break
                                        
                        if not typerror:
                            check = type.updateRecord(pk, fields, btrees)
                            if check:
                                writer.writerow([int(time.time()), line.rstrip(), "success"])
                            else:
                                # given pk does not exist
                                writer.writerow([int(time.time()), line.rstrip(), "failure"])
                    else:
                        # required number of fields is not equal to entered fields
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])
                else:
                    # given type does not exist
                    writer.writerow([int(time.time()), line.rstrip(), "failure"])

            elif parse[0] == "filter":   
                # filter record <type-name><condition>
                typename = parse[2]

                if typename in types.keys():
                    condition = ""
                    for i in range(len(parse)-3):
                        condition += parse[i+3]

                    type = types[typename]
                    check = type.filterRecord(condition, btrees)

                    if check[1]:
                        output.write(check[0])
                        writer.writerow([int(time.time()), line.rstrip(), "success"])
                    else:
                        writer.writerow([int(time.time()), line.rstrip(), "failure"])
                else:
                    # if given type does not exist
                    writer.writerow([int(time.time()), line.rstrip(), "failure"])

            else:
                # infeasible keyword
                writer.writerow([int(time.time()), line.rstrip(), "failure"]) 



            

            