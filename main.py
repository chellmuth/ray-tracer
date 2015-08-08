import argparse

from world import World

def render(debug):
    world = World(debug)
    world.render_scene()
    world.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    render(debug=args.debug)
