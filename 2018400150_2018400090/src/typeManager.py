import os

len_recordHeader = 1
len_pageHeader = 13
len_page_bytes = 256
no_pages_in_file = 32


class Type:
    def __init__(self, name, no_fields, pk_order):
        self.name = name
        self.no_fields = no_fields
        self.pk_order = pk_order
        #self.fieldHeaders = fieldHeaders 
        self.pages = [] # keeping index of available record spots
        self.filename = name + ".txt"
        self.record_length = (len_recordHeader + no_fields*20 + 2)
        self.residual = (len_page_bytes - len_pageHeader) % self.record_length
        self.max_records = (len_page_bytes - len_pageHeader) // self.record_length

    # each type has exactly one base file
    # if the current file gets full then new file should be opened

    def findAvailableIndex(self):
        
        for pageno, index in enumerate(self.pages):
            # if page is full
            print(self.pages)
            if index == -1:
                pass
            else:
                
                #search in the corresponding page
                f = open(self.filename, 'r+')
                startbyte = len_page_bytes*(pageno)
                f.seek(startbyte)
                header = f.read(len_pageHeader)
                currentrecord = header[3:5]
                maxrecord = header[6:8]

                

                if int(currentrecord) + 1 == int(maxrecord):
                    # after an insertion page will be full
                    currentrecord = int(currentrecord) + 1
                    currentrecord = str(currentrecord)
                    if len(currentrecord) == 1:
                        currentrecord = '0' + currentrecord

                    f.seek(startbyte+3)
                    f.write(currentrecord)

                    self.pages[pageno] = -1
                    f.seek(startbyte+9)
                    f.write("-1")
                    f.close()
                    
                else: 
                    # searching for the next available spot starting from current available spot + 1
                    
                    byteptr = startbyte + len_pageHeader + index*self.record_length
                    count = index + 1
                    while True:
                        f.seek(byteptr)
                        if f.read(1) == '1':
                            byteptr += self.record_length
                            count += 1
                        else:

                            # append new available spot for the page
                            self.pages[pageno] = index + 1

                            # update record header for new sessions

                            currentrecord = int(currentrecord) + 1
                            currentrecord = str(currentrecord)
                            if len(currentrecord) == 1:
                                currentrecord = '0' + currentrecord

                            f.seek(startbyte+3)
                            f.write(currentrecord)


                            count = str(count)
                            if len(count) == 1:
                                count = '0' + count

                            f.seek(startbyte+9)
                            f.write(count)
                            f.close()
                            break


                return pageno+1, index
        
        if len(self.pages) == no_pages_in_file: # current file is full
            pass
            # new file and new page
        else:
            f = open(self.filename, 'r+')
            startbyte = len_page_bytes*(len(self.pages))

            if len(self.pages) > 0:
                #filling residual part from the previous page (for visual purposes)
                f.seek(startbyte-self.residual)
                f.write(' '*(self.residual-2))
                f.write('\n')

            #creating new page

            f.seek(startbyte)
            pageno = str(len(self.pages) + 1)
            currentrecord = "01"
            maxrecord = str(self.max_records)
            availablerecord = "02"

            if len(pageno) == 1:
                pageno = '0' + pageno

            if len(maxrecord) == 1:
                maxrecord = '0' + maxrecord

            f.write(pageno + ' ' + currentrecord + ' ' + maxrecord + ' ' + availablerecord + '\n')
            f.close()

            # 1st index will be taken and 2nd index will be the next available spot
            self.pages.append(2)
            #print(self.pages)
            return len(self.pages), 1



    # this is used to create record
    def createRecord(self, fields, btrees):
        f = open(self.filename, 'r+')

        # bunu nereye yazacaz --> file manager
        address = self.findAvailableIndex()
        pageno = address[0]
        index = address[1]

        startbyte = len_page_bytes*(pageno-1) + len_pageHeader + self.record_length*(index-1)
        f.seek(startbyte)
        # manuel record header entry
        f.write("1")

        for field in fields:
            f.write(field.ljust(20))

        f.write("\n")
        f.close()

        #rid = 
        # open bplustree from the corresponding file
        # angel.json load
        # build the tree from scratch with regard to information in the file

        # new insert
        pk = fields[self.pk_order-1]

        # inserting <key, value: closest starting byte to the beginning of the file>
        btrees[self.name].insert(pk, startbyte)


    #returns page no and record no from byte location
    def getLocation(self, address):
        pageno = address // len_page_bytes + 1
        index = (address % len_page_bytes - len_pageHeader) // self.record_length + 1

        return pageno, index

    # be careful about page and index --> check if they are 0 indexed or 1 indexed
    def deleteRecord(self, pk, btrees):
        address = btrees[self.name].find(pk)[pk]
        location = self.getLocation(address)
        pageno = location[0]
        index = location[1]

        #print(location)

        f = open(self.filename, 'r+')

        startbyte = len_page_bytes*(pageno-1)
        f.seek(startbyte)
        header = f.read(len_pageHeader)
        currentrecord = header[3:5]
        availablerecord = header[9:11]

        

        currentrecord = int(currentrecord) - 1
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

            # updating pages list 
            self.pages[pageno-1] = int(index)

        
        # adding 0 in record header
        index = int(index)
        byteptr = startbyte + len_pageHeader + (index-1)*self.record_length
        f.seek(byteptr)
        f.write('0')

        f.close()

        print(self.pages)

        # deleting from b+ tree
        btrees[self.name].delete(pk)

        # checking if file is empty, if so delete the file
        # remove from the system catalog as well
        check = True
        for i in self.pages:
            if i != 1:
                check = False
                break
        
        if check:
            if os.path.exists(self.filename):
                os.remove(self.filename)
                print(self.filename + " has been deleted successfully")
            else:
                print(self.filename + " does not exist!")

    # update hatası burada da verilebilir parselarken de 
    # hangisi kolaysa ona göre implementasyon
    # delete ve create için de geçerli bu durum
    def updateRecord(self, pk, fields, btrees):
        address = btrees[self.name].find(pk)[pk]
        location = self.getLocation(address)
        pageno = location[0]
        index = location[1]

        # veri düzgün ise sırasıyla verilmiştir
        # fieldları stringify edelim ve tree aracılığıyla gittiğimiz yeri güncelleyelim

        f = open(self.filename, 'r+')

        startbyte = len_page_bytes*(pageno-1) + len_pageHeader + self.record_length*(index-1)
        f.seek(startbyte)
        f.write("1")

        for field in fields:
            f.write(field.ljust(20))

        f.write("\n")
        f.close()

    # treeden arayıp olup olmadığını bilebiliriz
    # hata bastırmak için tree kullanmak mantıklı (parselarken zor tespit edilecek hatalar için)
    def searchRecord(self, pk, btrees):
        address = btrees[self.name].find(pk)[pk]
        location = self.getLocation(address)
        pageno = location[0]
        index = location[1]


        # aranana şeyin var olduğu durum
        f = open(self.filename, 'r+')
        startbyte = len_page_bytes*(pageno-1) + len_pageHeader + self.record_length*(index-1)
        f.seek(startbyte)
        record = f.read(self.record_length-1)[1:]
        record = ' '.join(record.split())

        print(record)

        f.close()

    
    def listRecord(self, btrees):
        pks = btrees[self.name].getItems()

        for pk in pks:
            self.searchRecord(pk, btrees)

    















    










    
