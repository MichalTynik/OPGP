WIDTH = 15
HEIGHT = 10

for i in range(1,HEIGHT+1):
    for j in range(1,WIDTH+1):
        if i == 0 and j == 0:
            break
        print(f"{i*j:3d}|", end="")
    print()