# class MyClass:
#     # Class variable to hold all instances
#     instances = []

#     def __init__(self, name):
#         self.name = name
#         # Append the new instance to the class variable
#         MyClass.instances.append(self)

#     @classmethod
#     def print_all_instances(cls):
#         for instance in cls.instances:
#             print(instance)

#     def __repr__(self):
#         return f"MyClass(name={self.name})"

# # Example usage
# obj1 = MyClass("Object 1")
# obj2 = MyClass("Object 2")
# obj3 = MyClass("Object 3")

# # Print all instances
# MyClass.print_all_instances()

for i in range (100, 5001, 100):
    for j in range(0, 3):
        print(-i)

            