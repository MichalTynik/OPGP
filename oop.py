class python:
    def __init__(self, vypis):
        self.vypis = vypis
    def dacorob(self):
        return f"{self.vypis} ................"
    def __str__(self):
        return f"Ahoj"

ok = python("Dobry den")
print(ok.dacorob())
print(ok)
