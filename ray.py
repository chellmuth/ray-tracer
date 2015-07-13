class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def extrapolate(self, t):
        return self.origin + self.direction.mult(t)
