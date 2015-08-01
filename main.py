import Queue as Q
from multiprocessing import Process, Queue

import pyglet

from world import World

def main():
    queue = Queue()



    renderer = Process(target=render, args=(queue,))
    renderer.start()

    config = pyglet.gl.Config(double_buffer=False)
    window = pyglet.window.Window(config=config)
    window.clear()

    def draw_rendering(dt):
        points = []
        colors = []
        count = 0

        def draw_points(points, colors, count):
            pyglet.graphics.draw(count, pyglet.gl.GL_POINTS,
                ('v2i', points),
                ('c3B', colors)
            )

        try:
            while True:
                pixel = queue.get(block=False)
                points.extend([pixel[1], 200-pixel[0]])
                colors.extend([int(pixel[2][0]), int(pixel[2][1]), int(pixel[2][2])])

                count += 1
                if count > 200:
                    draw_points(points, colors, count)
                    count = 0
                    points = []
                    colors = []

        except Q.Empty:
            draw_points(points, colors, count)
            count = 0
            points = []
            colors = []

    pyglet.clock.schedule_interval(draw_rendering, 0.3)

    pyglet.app.run()

def render(queue):
    world = World(queue)
    world.render_scene()
    world.show()

if __name__ == '__main__':
    main()
