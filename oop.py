import random
MAX_TIME = 60
class Auto:
    """Auto klasa

    Returns:
        int: speed
        int: distance
    """
    MAX_SPEED = 240
    MAX_ACCELERATION = 5
    MIN_ACCELERATION = -2
    def __str__(self) -> str:
        return f"Name: {self.name}\n Speed: {self.speed}\n Top: {self.top_speed}\n Distance: {self.distance:.2f}"
    def __init__(self, name):
        self.name = name
        self.speed = 0
        self.distance = 0
        self.top_speed = 0
    def acceleration(self, accelerate):
        """Akceleracna metoda
        """
        accelerate = min(accelerate,self.MAX_ACCELERATION)
        accelerate = max(accelerate,self.MIN_ACCELERATION)
        self.speed += accelerate
        self.speed = min(accelerate,self.MAX_SPEED)
        self.speed = max(accelerate, 0)
    def accelerate_random(self):
        accel = random.randint(self.MIN_ACCELERATION, self.MAX_ACCELERATION)
        self.acceleration(accel)
    def step_second(self):
        self.distance += self.speed /3.6
        self.top_speed = max(self.speed, self.top_speed)

cars = ["Toyota", "Honda", "Kia"]
auto1= Auto(cars[0])
auto2= Auto(cars[1])
auto3= Auto(cars[2])
time = 0
while time<MAX_TIME:
    auto1.accelerate_random()
    auto1.step_second()
    auto2.accelerate_random()
    auto2.step_second()
    auto3.accelerate_random()
    auto3.step_second()
    time+=1
print(auto1)
print(auto2)
print(auto3)