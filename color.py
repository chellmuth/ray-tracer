class RGBColor(object):
    @classmethod
    def Red(cls):
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def Blue(cls):
        return cls(0.0, 0.0, 1.0)

    @classmethod
    def Black(cls):
        return cls(0.0, 0.0, 0.0)

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        return RGBColor(self.r + other.r, self.g + other.g, self.b + other.b)

    def __div__(self, n):
        return RGBColor(self.r / n, self.g / n, self.b / n)

    def to_list(self):
        return [self.r * 255.0, self.g * 255.0, self.b * 255.0]
