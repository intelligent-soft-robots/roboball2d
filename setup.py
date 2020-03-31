from setuptools import setup,find_packages
import sys
from os import path

with open(path.join(path.dirname(__file__), 'VERSION')) as v:
    VERSION = v.readline().strip()


setup(name = "roboball2d",
      packages=find_packages('.'),
      version = VERSION,
      description="A simulated 2d robot playing with balls",
      url="https://github.com/intelligent-soft-robots/roboball2d",
      long_description="see https://roboball2d.readthedocs.io/en/latest/",
      author="Nicolas Guetler, Vincent Berenz",
      author_email="nico.guertler@tuebingen.mpg.de, vberenz@tuebingen.mpg.de",
      scripts=['demos/roboball2d_demo',
               'demos/roboball2d_balls_demo',
               'demos/roboball2d_mirror_demo',
               'demos/roboball2d_rendering_demo'],
      install_requires = ["pyglet", "box2d-py"]
)
