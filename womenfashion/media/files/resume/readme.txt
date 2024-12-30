Polymorphism with Class Methods 

Polymorphism in class methods allows different classes to define methods with 
the same name but with different implementations.

class Shape: 
 	def description(self): 
 		raise NotImplementedError("Subclass must implement this method") 
class Circle(Shape): 
 	def __init__(self, radius): 
 		self.radius = radius 
 
 	def description(self): 
 		return f"Circle with radius {self.radius}"
class Rectangle(Shape): 
 	def __init__(self, width, height): 
 		self.width = width 
 		self.height = height 
 
 	def description(self): 
 		return f"Rectangle with width {self.width} and height {self.height}" 
class Triangle(Shape): 
 	def __init__(self, base, height): 
 		self.base = base 
 		self.height = height 
 
 	def description(self): 
 		return f"Triangle with base {self.base} and height {self.height}" 

# Function to demonstrate polymorphism 
def print_description(shape): 
 	print(shape.description()) 

# Creating instances of each class 
circle = Circle(5) 
rectangle = Rectangle(4, 6) 
triangle = Triangle(3, 7) 

# Demonstrating polymorphism 
shapes = [circle, rectangle, triangle] 
for shape in shapes: 
 	print_description(shape) 
