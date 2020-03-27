import numpy as np

        
class RobotConfig:

    """
    Interface a robot configuration must implement to be used 
    with :py:class:`roboball2d.physics.b2_world.B2World` and
    :py:class:`roboball2d.physics.rendering.pyglet_renderer.PygletRenderer`
    See : :py:class:`roboball2d.robot.default_robot_config.DefaultRobotConfig
    """
    
    def __init__(self):
        raise NotImplementedError("__init__ not implemented.")

    def create_b2_robot(self, world, ground):
        raise NotImplementedError("__init__ not implemented.")

