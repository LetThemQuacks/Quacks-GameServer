import random

class Test1:
    def __new__(cls):
        return random.random()

print(Test1())
print(Test1())
print(Test1())
print(Test1())
print(Test1())
print(Test1())
