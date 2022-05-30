import os

x = "aaaaaaaa"

output = x.ljust(20, ' ')

y ="bbb"

z = "cccccccccccccc"


f = open("demofile.txt", "a")

f.write(x.ljust(20, ' '))
f.write(y.ljust(20, ' '))
f.write(z.ljust(20, ' '))
f.write('\n')

f.close()

f = open("demofile.txt", "r")
f.seek(20)
print(f.read(0))

# get the size of file
size = os.path.getsize('c:/Users/Asus/DBProjects/CMPE321/2018400150_2018400090/demofile.txt') 
print('Size of file is', size, 'bytes')


deneme = [[1,2],[1,4],[1,2,3]]

for i, page in enumerate(deneme):
    # if page is full
    if not page:
        print("asdfasdf")
        pass
    else:
        print(i)
        print(page)
        print("bokadam")


s = "-1"

k = 3

k = str(k)

print(k)

if len(k) ==  1:
    k = '0' + k

print(k)



    


