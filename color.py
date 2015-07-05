class RGBColor(object):
    @classmethod
    def Red(cls):
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def Black(cls):
        return cls(0.0, 0.0, 0.0)

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


    def to_list(self):
        return [self.r * 255.0, self.g * 255.0, self.b * 255.0]
