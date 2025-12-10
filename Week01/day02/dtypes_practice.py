# list
numbers = [10, 20, 30]

numbers.append(40)
numbers.insert(1, 15)    
numbers.remove(30)       
numbers[0] = 5          
for n in numbers:        
    print(n)

print("final list:", numbers)

# tuple
person = ("Ali", 22, "Lahore")

name = person[0]
age = person[1]

print(name, age)

# sets
fruits = {"apple", "banana", "mango"}

fruits.add("orange")         
fruits.add("apple")          
fruits.discard("banana")     

print("mango" in fruits)
print("fina set:", fruits)

# dict
student = {
    "name": "Tahir",
    "age": 23,
    "city": "Lahore"
}

student["age"] = 24
student["cgpa"] = 3.5

for key, value in student.items():
    print(key, value)

print("final dict:", student)


