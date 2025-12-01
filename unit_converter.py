def kg_to_pound(kg):
    return kg * 2.20462

def pound_to_kg(pound):
    return pound * 0.453592

def meter_to_km(meter):
    return meter / 1000

def km_to_meter(km):
    return km * 1000

def cm_to_meter(cm):
    return cm / 100

def meter_to_cm(meter):
    return meter * 100


while True:
    print("1. Kg to Pound")
    print("2. Pound to Kg")
    print("3. Meter to Km")
    print("4. Km to Meter")
    print("5. Cm to Meter")
    print("6. Meter to Cm")
    print("0. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 0:
        print("Exited!")
        break

    value = float(input("Enter value to convert: "))

    if choice == 1:
        print(f"{value} kg = {kg_to_pound(value)} pound")
    elif choice == 2:
        print(f"{value} pound = {pound_to_kg(value)} kg")
    elif choice == 3:
        print(f"{value} meter = {meter_to_km(value)} km")
    elif choice == 4:
        print(f"{value} km = {km_to_meter(value)} meter")
    elif choice == 5:
        print(f"{value} cm = {cm_to_meter(value)} meter")
    elif choice == 6:
        print(f"{value} meter = {meter_to_cm(value)} cm")
    else:
        print("Invalid choice.")