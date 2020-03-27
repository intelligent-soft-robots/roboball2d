class RobotState:

    """
    Interface a robot state must implement to be used  with
    :py:class:`roboball2d.physics.rendering.pyglet_renderer.PygletRenderer`
    See : :py:class:`roboball2d.robot.default_robot_state.DefaultRobotState
    """
    
    def __init__(self, robot_config, generalized_coordinates = None,
            generalized_velocities = None):
        raise NotImplementedError("__init__ not implemented.")

    def render(self):
        raise NotImplementedError("render not implemented.")
