import math
import random

from point import Point2

class Sampler(object):
    def __init__(self, sample_count):
        self.sample_count = sample_count

    def generate_samples(self):
        samples_per_axis = int(math.sqrt(self.sample_count))

        samples = []
        for row in range(samples_per_axis):
            for col in range(samples_per_axis):
                x = (col + random.random()) / samples_per_axis
                y = (row + random.random()) / samples_per_axis
                samples.append(Point2(x, y))

        return samples
