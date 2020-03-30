from setuptools import setup

setup(name = "roboball2d",
      packages=['roboball2d',
                'roboball2d/physics',
                'roboball2d/rendering',
                'roboball2d/robot',
                'roboball2d/ball',
                'roboball2d/ball_gun',
                'roboball2d/demos'],
      version = "0.1.0",
      scripts=['demos/roboball2d_demo',
               'demos/roboball2d_balls_demo',
               'demos/roboball2d_mirror_demo',
               'demos/roboball2d_rendering_demo'],
      install_requires = ["pyglet", "Box2D","box2d-py"]
)
