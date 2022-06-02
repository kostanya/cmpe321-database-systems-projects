import os

len_recordHeader = 1
len_pageHeader = 13
len_page_bytes = 2048
no_pages_in_file = 8


class Type:
    def __init__(self, name, no_fields, pk_order, fieldHeaders):
        self.name = name
        self.no_fields = no_fields
        self.pk_order = pk_order
        self.fieldHeaders = fieldHeaders
        self.pk_header = fieldHeaders[2*pk_order-2]
        self.available = [] # keeping index of available record spots # keeping page header information to not to scan memory over and over 
        self.no_records = [] # number of records per page
        self.files = []
        self.record_length = (len_recordHeader + no_fields*20 + 2)
        self.residual = (len_page_bytes - len_pageHeader) % self.record_length
        self.max_records_page = (len_page_bytes - len_pageHeader) // self.record_length
        self.max_records_file = self.max_records_page * no_pages_in_file 

    # each type has exactly one base file
    # if the current file gets full then new file should be opened

    def findAvailableIndex(self):
        
        for pageno, index in enumerate(self.available):
            # careful pageno here is 0 indexed
            if index == -1:
                pass
            else:
                dosyadi = self.files[pageno // no_pages_in_file]
            
                #search in the corresponding page
                f = open(dosyadi, 'r+')
                startbyte = len_page_bytes*(pageno % no_pages_in_file)
                f.seek(startbyte)
                header = f.read(len_pageHeader)
                currentrecord = header[3:5]
                maxrecord = header[6:8]

                
                if int(currentrecord) + 1 == int(maxrecord):
                    # after an insertion page will be full
                    currentrecord = int(currentrecord) + 1
                    self.no_records[pageno] = currentrecord

                    currentrecord = str(currentrecord)
                    if len(currentrecord) == 1:
                        currentrecord = '0' + currentrecord

                    f.seek(startbyte+3)
                    f.write(currentrecord)

                    self.available[pageno] = -1
                    f.seek(startbyte+9)
                    f.write("-1")
                    f.close()
                    
                else: 
                    # searching for the next available spot starting from current available spot + 1
                    
                    byteptr = startbyte + len_pageHeader + index*self.record_length
                    newindex = index + 1
                    while True:
                        f.seek(byteptr)
                        if f.read(1) == '1':
                            byteptr += self.record_length
                            newindex += 1
                        else:

                            # append new available spot for the page
                            self.available[pageno] = newindex 

                            # update record header for new sessions

                            currentrecord = int(currentrecord) + 1
                            self.no_records[pageno] = currentrecord

                            currentrecord = str(currentrecord)
                            if len(currentrecord) == 1:
                                currentrecord = '0' + currentrecord

                            f.seek(startbyte+3)
                            f.write(currentrecord)


                            newindex = str(newindex)
                            if len(newindex) == 1:
                                newindex = '0' + newindex

                            f.seek(startbyte+9)
                            f.write(newindex)
                            f.close()
                            break

                # returns the address that has just been occupied by the new record         
                return pageno // no_pages_in_file + 1, pageno % no_pages_in_file + 1, index

        
        def createPage(dosyadi):
            
            f = open(dosyadi, 'r+')
            startbyte = len_page_bytes*(len(self.available) % no_pages_in_file)

            if len(self.available) % no_pages_in_file > 0:
                #filling residual part from the previous page (for visual purposes)
                f.seek(startbyte-self.residual)
                f.write(' '*(self.residual-2))
                f.write('\n')

            #creating new page

            f.seek(startbyte)
            pageno = str(len(self.available) % no_pages_in_file + 1)
            currentrecord = "01"
            maxrecord = str(self.max_records_page)
            availablerecord = "02"

            if len(pageno) == 1:
                pageno = '0' + pageno

            if len(maxrecord) == 1:
                maxrecord = '0' + maxrecord

            f.write(pageno + ' ' + currentrecord + ' ' + maxrecord + ' ' + availablerecord + '\n')
            f.close()

           
            # 1st index will be taken and 2nd index will be the next available spot
            self.available.append(2)
            self.no_records.append(1)
            #print(self.pages)
            return (len(self.available)-1) // no_pages_in_file + 1, (len(self.available)-1) % no_pages_in_file + 1, 1

        
        print("++++++++++++++++++++++++")
        print(len(self.available))
        # need to open a new file and a new page
        if len(self.no_records) % no_pages_in_file == 0:
            newfile = self.name + str(len(self.available) // no_pages_in_file + 1) + ".txt"

            # creating the file as r+ does not create a file if it does not exist
            f = open(newfile, 'w')
            f.close()

            self.files.append(newfile)
            return createPage(newfile)

        # need to open a new page
        else:
            dosyadi = self.files[len(self.available) // no_pages_in_file]
            return createPage(dosyadi)



    # this is used to create record
    def createRecord(self, fields, btrees):

        # new insert
        pk = fields[self.pk_order-1]

        # converting pk from string to int if its type is int
        if self.fieldHeaders[2*self.pk_order-1] == 'int':
            try:
                pk = int(pk)
            except:
                return False

        # insert only if the pk does not exist in the tree
        if btrees[self.name].query(pk) is None:

            address = self.findAvailableIndex()
            fileno = address[0]
            pageno = address[1]
            index = address[2]

            print("pk: " + str(pk) + ' ' +  str(index))

            dosyadi = self.files[fileno-1]

            f = open(dosyadi, 'r+')

            startbyte = len_page_bytes*(pageno-1) + len_pageHeader + self.record_length*(index-1)
            f.seek(startbyte)
            # manuel record header entry
            f.write("1")

            for field in fields:
                f.write(field.ljust(20))

            f.write("\n")
            f.close()

            # inserting <key, value: closest starting byte to the beginning of the file>
            filebytes = len_page_bytes * no_pages_in_file
            byteaddress = filebytes*(fileno-1) + startbyte
            btrees[self.name].insert(pk, byteaddress)

            print(self.available)
            print(self.no_records)
            print("---------------------------")
            print(self.name + ": record insertü başarılı")
            return True
        else:
            print(self.name + ": bu pk zaten var amcık seni")
            return False



    #returns page no and record no from byte location
    def getLocation(self, address):
        filebytes = len_page_bytes * no_pages_in_file
        fileno = address // filebytes + 1 
        offset = address % filebytes
        pageno = offset // len_page_bytes + 1
        index = (offset % len_page_bytes - len_pageHeader) // self.record_length + 1

        return fileno, pageno, index

    # be careful about page and index --> check if they are 0 indexed or 1 indexed
    def deleteRecord(self, pk, btrees):

        # converting pk from string to int if its type is int
        if self.fieldHeaders[2*self.pk_order-1] == 'int':
            try:
                pk = int(pk)
            except:
                return False
        
        address = btrees[self.name].query(pk) # if does not exist, returns None
        if address:
            location = self.getLocation(address)
            fileno = location[0]
            pageno = location[1]
            index = location[2]

            print(pk, fileno)

            dosyadi = self.files[fileno-1]

            f = open(dosyadi, 'r+')

            startbyte = len_page_bytes*(pageno-1)
            f.seek(startbyte)
            header = f.read(len_pageHeader)
            currentrecord = header[3:5]
            availablerecord = header[9:11]

            
            currentrecord = int(currentrecord) - 1
            self.no_records[(fileno-1)*no_pages_in_file + pageno-1] = currentrecord

            currentrecord = str(currentrecord)
            if len(currentrecord) == 1:
                currentrecord = '0' + currentrecord

            f.seek(startbyte+3)
            f.write(currentrecord)

            availablerecord = int(availablerecord)
            f.seek(startbyte+9)
            if availablerecord == -1 or index < availablerecord:
                # updating available section in page header
                index = str(index)
                if len(index) == 1:
                    index = '0' + index
                f.write(index)

                # updating available list 
                self.available[(fileno-1)*no_pages_in_file + pageno-1] = int(index)

            
            # adding 0 in record header
            index = int(index)
            byteptr = startbyte + len_pageHeader + (index-1)*self.record_length
            f.seek(byteptr)
            f.write('0')
            f.close()

            # deleting from b+ tree
            btrees[self.name].delete(pk)

            
            print(self.available)
            print(self.no_records)
            print("---------------------------")

            # checking if file is empty, if so delete the file
            check = True
            start = (fileno-1) * no_pages_in_file
            end = min(fileno * no_pages_in_file, len(self.no_records))

            for i in self.no_records[start:end]:
                if i != 0:
                    check = False
                    break
            
            if check:
                # emptying pages as well
                if fileno *  no_pages_in_file > len(self.no_records):
                    self.no_records[start:end] = [0]*(end-start)
                    self.available[start:end] = [-1]*(end-start)
                    self.no_records.extend([0]*(fileno * no_pages_in_file - len(self.no_records)))
                    self.available.extend([-1]*(fileno * no_pages_in_file - len(self.available)))
                else:
                    self.no_records[start:end] = [0]*(end-start)
                    self.available[start:end] = [-1]*(end-start)


                if os.path.exists(dosyadi):
                    os.remove(dosyadi)
                    print(dosyadi + " has been deleted successfully")
                else:
                    print(dosyadi + " does not exist!")

            return True
        else:
            # pk is not in tree
            return False

    # update hatası burada da verilebilir parselarken de 
    # hangisi kolaysa ona göre implementasyon
    # delete ve create için de geçerli bu durum
    def updateRecord(self, pk, fields, btrees):

        # converting pk from string to int if its type is int
        if self.fieldHeaders[2*self.pk_order-1] == 'int':
            try:
                pk = int(pk)
            except:
                return False
        
        address = btrees[self.name].query(pk)
        if address:
            location = self.getLocation(address)
            fileno = location[0]
            pageno = location[1]
            index = location[2]

            dosyadi = self.files[fileno-1]

            f = open(dosyadi, 'r+')

            startbyte = len_page_bytes*(pageno-1) + len_pageHeader + self.record_length*(index-1)
            f.seek(startbyte)
            f.write("1")

            for field in fields:
                f.write(field.ljust(20))

            f.write("\n")
            f.close()

            print(self.name + ": record updatei başarılı")
            return True
        else:
            return False


    # For the listing, searching, and filtering operations, 
    # if the output of the operation is empty, it must be considered as failure
    # and logged accordingly.

    # treeden arayıp olup olmadığını bilebiliriz
    # hata bastırmak için tree kullanmak mantıklı (parselarken zor tespit edilecek hatalar için)
    def searchRecord(self, pk, btrees):
        record = ""

        # converting pk from string to int if its type is int
        if self.fieldHeaders[2*self.pk_order-1] == 'int':
            try:
                pk = int(pk)
            except:
                return record, False
        
        address = btrees[self.name].query(pk)

        if address:
            location = self.getLocation(address)
            fileno = location[0]
            pageno = location[1]
            index = location[2]

            dosyadi = self.files[fileno-1]

            f = open(dosyadi, 'r+')

            startbyte = len_page_bytes*(pageno-1) + len_pageHeader + self.record_length*(index-1)
            f.seek(startbyte)
            record = f.read(self.record_length-1)[1:] 
            record = ' '.join(record.split())
            record += '\n'

            f.close()

            return record, True
        else:
            return record, False
           

    
    def listRecord(self, btrees, pk = "", mode = 0):

        # converting pk from string to int if its type is int

        records = ""
        
        if mode == 0:
            pks = btrees[self.name].getItems()
        if mode == -1:
            # converting pk from string to int if its type is int
            if self.fieldHeaders[2*self.pk_order-1] == 'int':
                try:
                    pk = int(pk)
                except:
                    return records, False

            pks = btrees[self.name].getLeft(pk)
        if mode == 1:
            # converting pk from string to int if its type is int
            if self.fieldHeaders[2*self.pk_order-1] == 'int':
                try:
                    pk = int(pk)
                except:
                    return records, False

            pks = btrees[self.name].getRight(pk)

        # if nothing is in tree
        if not pks:
            return records, False
        else:
            for pk in pks:
                records += self.searchRecord(pk, btrees)[0]

            return records, True


    # condition = {'<', '>', '='}, key might be on the left
    def filterRecord(self, condition, btrees):
        
        records = ""
        cond = ""
        lhs = ""
        rhs = ""

        # checking if condition proper
        for ch in condition:
            if ch in (' ', '/t'):
                continue

            if not ch.isalnum():
                cond += ch

        if cond not in ("<", ">", "="):
            return records, False

        # getting lhs and rhs
        sides = condition.split(cond)
        lhs = sides[0]
        rhs = sides[1]

        if lhs != self.pk_header and rhs != self.pk_header:
            return records, False

        if lhs == self.pk_header and rhs == self.pk_header:
            return records, False

        if lhs == self.pk_header:
            pk = rhs
            if cond == '=':
                return self.searchRecord(pk, btrees)
                
            elif cond == '<':
                return self.listRecord(btrees, pk, -1)

            elif cond == '>':
                return self.listRecord(btrees, pk, 1)

        elif rhs == self.pk_header:
            pk = lhs
            if cond == '=':
                return self.searchRecord(pk, btrees)
                
            elif cond == '<':
                return self.listRecord(btrees, pk, 1)

            elif cond == '>':
                return self.listRecord(btrees, pk, -1)

                


    