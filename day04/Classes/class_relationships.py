# Class Relationships
"""
1. Association (Weakest relationship) > one class using another class temp
"""
from pyclbr import Class


class Teacher:
    def teach(self, subject):
        print(f"Teacher teachs {subject}")

class Student:
    def learn(self, teacher):
        teacher.teach("English")
        print("Student is learning.")

my_teacher = Teacher()
std = Student()
std.learn(my_teacher)


"""
2. Aggregation (Weak Ownership) > one class hold other but not for lifetime
"""
class Students:
    def __init__(self, name):
        self.name = name
    
class ClassRoom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

std1 = Students(name="Ali")
std2 = Students(name='Ahmad')
room = ClassRoom()
room.add_student(std1)
room.add_student(std2)
print(f"student in room: {room.students[0].name} and {room.students[1].name}")
# with destrucion of room obj, the student list will stil exist
del room
print(f"students still available: {std1.name} and {std2.name}")


"""
3. Composition (Strong ownership) > one class is made of other classes
    if main class destroyed, internal objs also will be vanished.
"""
class Engine:
    def __init__(self, hp):
        self.hp = hp
    
class Car:
    def __init__(self, model):
        self.model = model
        self.engine = Engine(2000)

car = Car(2020)
print(f"car model is {car.model} having horsepower {car.engine.hp}")
# del car    >> will delete the engine as well.