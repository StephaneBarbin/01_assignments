#******************************************************************************
# content     = Classes
#
# date        = 2024-11-12
# author      = Stephane Barbin
#******************************************************************************

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""


class Cube:
    def __init__(self, name):
        self.name = name
        self.translation = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scale_factors = [1.0, 1.0, 1.0]
        self.color_rgb = [1.0, 1.0, 1.0]

    def translate(self, x, y, z):
        self.translation = [x, y, z]
        print(f"Translated to: {self.translation}")

    def rotate(self, x, y, z):
        self.rotation = [x, y, z]
        print(f"Rotated to: {self.rotation}")

    def scale(self, x, y, z):
        self.scale_factors = [x, y, z]
        print(f"Scaled to: {self.scale_factors}")

    def color(self, R, G, B):
        self.color_rgb = [R, G, B]
        print(f"Color set to: {self.color_rgb}")

    def print_status(self):
        print(f"------ {self.name} Status ------")
        print(f"Translation: {self.translation}")
        print(f"Rotation:    {self.rotation}")
        print(f"Scale:       {self.scale_factors}")
        print(f"Color:       {self.color_rgb}")
        print("----------------------------")

    def update_transform(self, ttype, value):
        transform_methods = {"translate": self.translate,
                             "rotate":    self.rotate,
                             "scale":     self.scale
                            }
        transform_methods[ttype](*value)



# TESTING
# Creating 3 cubes
first_cube = Cube("Cube001")
second_cube = Cube("Cube002")
third_cube = Cube("Cube003")

# Printing third_cube print_status
third_cube.print_status()

# Testing update_transform function with second_cube
second_cube.update_transform("translate", [1, 2, 3])
second_cube.update_transform("rotate", [45, 0, 90])
second_cube.update_transform("scale", [2, 2, 2])



# Creating "Object" parent class and updating "Cube" class
# -------------------------------------------------------------------------------


class Object:
    def __init__(self, name):
        self.name = name
        self.translation = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scale_factors = [1.0, 1.0, 1.0]

    def translate(self, x, y, z):
        self.translation = [x, y, z]
        print(f"{self.name} translated to: {self.translation}")

    def rotate(self, x, y, z):
        self.rotation = [x, y, z]
        print(f"{self.name} rotated to: {self.rotation}")

    def scale(self, x, y, z):
        self.scale_factors = [x, y, z]
        print(f"{self.name} scaled to: {self.scale_factors}")

    
    def print_status(self):
        pass


class Cube(Object):
    def __init__(self, name):
        super().__init__(name)
        self.color_rgb = [1.0, 1.0, 1.0]

    def color(self, R, G, B):
        self.color_rgb = [R, G, B]
        print(f"{self.name} color set to: {self.color_rgb}")

    def print_status(self):
        print(f"--- {self.name} Status ---")
        print(f"Translation: {self.translation}")
        print(f"Rotation: {self.rotation}")
        print(f"Scale: {self.scale_factors}")
        print(f"Color: {self.color_rgb}")
        print("----------------------------")

    def update_transform(self, ttype, value):
        transform_methods = {"translate": self.translate,
                             "rotate":    self.rotate,
                             "scale":     self.scale
                            }
        transform_methods[ttype](*value)



# TESTING
first_cube = Cube("Cube001")
first_cube.update_transform("translate", [6, 8, 2])
first_cube.update_transform("rotate", [35, 180, 95])
first_cube.update_transform("scale", [5, 5, 5])
first_cube.color(0.9, 1.0, 0.8)
first_cube.print_status()
