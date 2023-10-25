
dlzka = int(input("Zadaj dlzku: "))
q= 0
for i in range(dlzka):
    print()
    for j in range(dlzka-q):
        if i == 0:
            print("X", end="")
        elif j == 0 or j == (dlzka - q) -1:
            print("X", end="")
        else:
            print(" ", end="")
    q = q + 1    
        
            


