class Animal:
    def __init__(self, name):
        # parent class
        self.name = name

    def move(self):
        print(f"{self.name} is moving.")

class Dog(Animal):
    """child class, Dog: inherit from Animal (Parent)"""
    def speak(self):
        # This method overrides the parent's speak method >> Method overriding
        return "Woof!"

class Cat(Animal):
    """child class, cat: inherit from Animal (Parent)"""
    def speak(self):
        # This method overrides the parent's speak method  >> method overrding
        return "Meow!"

my_dog = Dog("Buddy")
my_cat = Cat("catie")

print(f"{my_dog.name} says: {my_dog.speak()}")
my_dog.move()

print(f"{my_cat.name} says: {my_cat.speak()}")
my_cat.move()