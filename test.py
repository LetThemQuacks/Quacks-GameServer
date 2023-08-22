class Iterator:
    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < 10:
            self.i += 1
            return self.i 
        else:
            raise StopIteration

for x in Iterator():
    print(x)

print(5 in Iterator())
print(11 in Iterator())
