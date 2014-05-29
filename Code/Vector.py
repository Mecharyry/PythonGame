import math

class Vector(object):

    # Vector Constructor defines how the vector should be created
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    # Creates a new Vector object from two points
    @classmethod
    def from_points(cls,P1, P2):
        return cls(P2[0] - P1[0], P2[1] - P1[1])

    # ToString method that prints the vector as a string
    def __str__(self):
        return "(%s, %s)"%(self.x, self.y)

    # Getter to get the x coordinate of the vector
    def get_x(self):
        return self.x

    # Getter to get the y coordinate of the vector
    def get_y(self):
        return self.y

    # Setter to set the x coordinate of the vector
    def set_x(self, x):
        self.x = x
        
    # Setter to set the y coordinate of the vector
    def set_y(self, y):
        self.y = y
        
    # Distance between two points
    def get_magnitude(self):
        if(math.sqrt(self.x**2 + self.y**2) == 0):
            return 1
        else:
        # self.x**2 is the same as self.x*self.x (squaring)
            return math.sqrt(self.x**2 + self.y**2)


    # Distance to Destination
    def get_distance_to(self, point):
        return math.sqrt((point.x - self.x)**2 + (point.y - self.y)**2)

    # Used to give a heading (think ship)
    def normalise(self):
        magnitude = self.get_magnitude()
        (self.x) /=  magnitude
        (self.y) /=  magnitude

    def compare_to(self, another):
        if (self.x == another.x and self.y == another.y):
            return True
        else:
            return False



#-------------------- Basic Mathmatical Structures for Vectors ------------------

    # Adding two vectors together and constructing a new Vector object
    def __add__(self, rhs):
        return Vector(self.x + rhs.x, self.y + rhs.y)

    # Subtracting two vectors and constructing a new Vector Object
    def __sub__(self, rhs):
        return Vector(self.x - rhs.x, self.y - rhs.y)

    # Negating a vector to get back to starting point!
    def __neg__(self):
        return Vector2(-self.x, -self.y)

    # Multiplying two vectors and constructing a new Vector Object
    def __mul__(self, scaler):
        return Vector(self.x * scaler, self.y * scaler)

    # Dividing two vectors and constructing a new Vector Object
    def __div__(self, scaler):
        return Vector(self.x / scaler, self.y / scaler)

#------------------ Make Vector Class Support Indexing -------------------------

    def __setitem__(self, key, value):
        if(key == 0):
            self.x = value
        elif(key == 1):
            self.y = value
        else:
            raise Exception ("Invalid key to vector")

    def __getitem__(self, key):
        if( key == 0):
                return self.x
        elif( key == 1):
                return self.y
        else:
                raise Exception("Invalid key to Point")
