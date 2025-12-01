class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        return a / b
    
    def mod(self, a, b):
        return a % b
    
    def sqroot(self, a):
        return a**0.5

calc = Calculator()

while True:
    print("0. Exit")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Mod")
    print("6. Square Root")

    choice = int(input("Enter choice to perform specific operation: "))
    if choice == 0:
        print("Exited!")
        break
    
    if choice == 6:
        a = float(input("Enter value: "))
        print(f"Square root of {a} = {calc.sqroot(a)}")
    else:
        a = float(input("Enter first value: "))
        b = float(input("Enter second value: "))

        if choice == 1:
            print(f"{a} + {b} = {calc.add(a, b)}")
        elif choice == 2:
            print(f"{a} - {b} = {calc.subtract(a, b)}")
        elif choice == 3:
            print(f"{a} * {b} = {calc.multiply(a, b)}")
        elif choice == 4:
            print(f"{a} / {b} = {calc.divide(a, b)}")
        elif choice == 5:
            print(f"{a} % {b} = {calc.mod(a, b)}")
        else:
            print("Invalid choice!!!")