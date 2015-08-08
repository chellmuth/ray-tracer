import argparse

from world import World

class Config(object):
    def __init__(self, args):
        self.debug = args.debug
        self.samples = args.samples or 1


def render(debug):
    world = World(debug)
    world.render_scene()
    world.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--samples", type=int)
    config = Config(parser.parse_args())

    render(config)
