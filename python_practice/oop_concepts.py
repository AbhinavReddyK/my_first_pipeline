# OOP Concepts Practice
# Learned: Classes, Objects, Inheritance

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hi I am {self.name}"

class Student(Person):
    def __init__(self, name, age, course):
        super().__init__(name, age)
        self.course = course

    def study(self):
        return f"{self.name} is studying {self.course}"

p = Student("Abhinav", 24, "Computer Science")
print(p.greet())
print(p.study())
