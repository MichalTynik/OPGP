class Cas:
    def __init__(self,hodiny,minuty):
        self.hodiny =hodiny
        self.minuty = minuty
        self.slovne = { 24:"dvanast",12:"dvanast",11:"jedenast", 23:"jedenast",10:"desat", 22:"desat",9:"devet", 21:"devat",8:"osem", 20:"osem",7:"sedem", 19:"sedem",6:"sest", 18:"sest",5:"pat", 17:"pat",4:"styri", 16:"styri",3:"tri", 15:"tri",2:"dva", 14:"dva",1:"jenda", 13:"jedenast", 0:"dvanast"}
    def text(self):
        if 30>self.minuty >=15:
            return f"stvrt na {self.slovne[self.hodiny+1]}"
        if 45>self.minuty >=30:
            return f"pol {self.slovne[self.hodiny+1]}ej"
        if 60>self.minuty >=45:
            return f"tri stvrte na {self.slovne[self.hodiny+1]}"
        if 15>self.minuty >= 0:
            return f"{self.slovne[self.hodiny]}"
    def str(self):
        return f"{self.hodiny:02d}:{self.minuty:02d}"
cas = Cas(9,30)
print(cas.text())