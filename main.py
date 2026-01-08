class Student:
    def __init__(self, roll, name, age):
        self.roll = roll
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.roll},{self.name},{self.age}"


def add_student():
    try:
        roll = input("Enter roll number: ")
        name = input("Enter name: ")
        age = input("Enter age: ")

        student = Student(roll, name, age)

        with open("students.txt", "a") as f:
            f.write(str(student) + "\n")

        print("Student added successfully")

    except Exception as e:
        print("Error:", e)


def view_students():
    try:
        with open("students.txt", "r") as f:
            data = f.readlines()
            if not data:
                print("No students found")
            else:
                for line in data:
                    roll, name, age = line.strip().split(",")
                    print(f"Roll: {roll}, Name: {name}, Age: {age}")

    except FileNotFoundError:
        print("File not found")


def delete_student():
    try:
        roll = input("Enter roll number to delete: ")

        with open("students.txt", "r") as f:
            lines = f.readlines()

        with open("students.txt", "w") as f:
            found = False
            for line in lines:
                if not line.startswith(roll + ","):
                    f.write(line)
                else:
                    found = True

        if found:
            print("Student deleted")
        else:
            print("Student not found")

    except Exception as e:
        print("Error:", e)


def update_student():
    try:
        roll = input("Enter roll number to update: ")

        with open("students.txt", "r") as f:
            lines = f.readlines()

        with open("students.txt", "w") as f:
            found = False
            for line in lines:
                if line.startswith(roll + ","):
                    name = input("Enter new name: ")
                    age = input("Enter new age: ")
                    f.write(f"{roll},{name},{age}\n")
                    found = True
                else:
                    f.write(line)

        if found:
            print("Student updated")
        else:
            print("Student not found")

    except Exception as e:
        print("Error:", e)


while True:
    print("\n--- Student Management System ---")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        update_student()
    elif choice == "4":
        delete_student()
    elif choice == "5":
        print("Exiting program")
        break
    else:
        print("Invalid choice")
