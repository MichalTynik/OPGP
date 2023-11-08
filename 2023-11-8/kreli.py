"""
    moj subor
"""
a = int(input("Velkost: "))
b=a
for i in range(a):
    if i !=a-1:
        for o in range(b-1):
            print(" ",end="")
        print("/", end="")
        for j in range(i*2):
            print(" ",end="")
        print("\\")
    if i == a-1:
        print("/", end="")
        for i in range(a*2 - 2):
            print("_", end="")
        print("\\")
    b -= 1
for i in range(a):
    if i != a-1:
        print("|", end="")
        for j in range(a*2-2):
            print(" ",end="")
        print("|")
    if i == a-1:
        print("|", end="")
        for i in range(a*2 - 2):
            print("_", end="")
        print("|")
        