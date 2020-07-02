from roboball2d.physics import B2World
from roboball2d.robot import DefaultRobotConfig
from roboball2d.robot import DefaultRobotState
from roboball2d.ball import BallConfig
from roboball2d.ball_gun import DefaultBallGun



"""
Factory functions for easier instantiations of physic engines and renderers
"""


class Roboball2d:

    """
    Container for instances of roboball2d classes. Typically
    instances of Roboball2d are returned by factory functions, see
    for example py:meth:`.get_default`.

    :param world: see :py:class:`roboball2d.world.b2_world.B2World`

    :param render: see :py:class:`roboball2d.rendering.pyglet_renderer.PygletRenderer`

    :param ball_guns: list of ball guns (one per ball), see :py:class:`roboball2d.ball_gun.default_ball_gun.DefaultBallGun`

    :param ball_gun: instance at the fist index of ball_guns

    :param robot_reinits: list of robot state instances (one per robot), 
     see :py:class:`roboball2d.robot.default_robot_state.DefaultRobotState`, 
     which may be used to reinitialize the world (see :py:meth:`roboball2d.world.b2_world.B2World.reset`)

    :param robot_reinit: instance at the first index of robot_reinit.

    :param robot_configs: list of robot configurations,
     see :py:class:`roboball2d.robot.default_robot_config.DefaultRobotConfig`

    :param robot_config: instance at the first index of robot_configs

    """
    
    __slots__=["world","renderer",
               "ball_guns","robot_reinits",
               "robot_configs"]
    
    def __init__(self):
        self.world = None
        self.renderer = None
        self.ball_guns = []
        self.robot_reinits = []
        self.robot_configs = []

    @property
    def robot_reinit(self):
        return self.robot_reinits[0]

    @property
    def ball_gun(self):
        return self.ball_guns[0]

    @property
    def robot_config(self):
        return self.robot_configs[0]

    
def get_default(nb_robots=1,
                nb_balls=1,
                ball_default_color=[1.0,1.0,1.0],
                ball_colors={},
                background_color=[0.0, 0.1, 0.4],
                ground_color= [0.0, 0.3, 0.0],
                visible_area_width=6.0,
                visual_height=0.05,
                window_size=(1600,800),
                render=True):

    """
    Returns an instance of :py:class:`.Roboball2d` encapsulating instances
    created using default configurations (except for values passed as arguments)

    Parameters
    ----------

    nb_robots: int, number of robors (default:1)

    nb_balls: int, number of balls (default:1)

    ball_default_color: tuple (R,G,B) (values between 0 and 1) (default 1,1,1)

    ball_colors: dict {ball index : tuple (R,G,B)} (default:{})

    background_color: tuple (R,G,B) (default: 0,0.1,0.4)

    ground_color: tuple (R,G,B) (default: 0,0.3,0.0)

    visible_area_width: float (default: 0.6)

    visual_height: float (default:0.05)

    window_size: tuple (width,height), in pixels (default: 1600,800)

    render: if true, the function returns a tuple of an instance of B2World and an instance
            of PygletRenderer, else returns a tuple of an instance of B2World and None 
            (default: True)

    """
    
    r = Roboball2d()

    robot_configs = [DefaultRobotConfig()
                     for _ in range(nb_robots)]
    r.robot_configs = robot_configs
    
    ball_configs = [BallConfig()
                    for _ in range(nb_balls)]

    for ball_config in ball_configs:
        ball_config.color = ball_default_color
        ball_config.line_color = ball_default_color
    for index,color in ball_colors.items():
        color = list(color)
        ball_configs[index].color = color
        ball_configs[index].line_color=color

    r.ball_guns = [DefaultBallGun(ball_config)
                   for ball_config in ball_configs]

    r.world = B2World(robot_configs,
                      ball_configs,
                      visible_area_width)

    r.robot_reinits = [DefaultRobotState(robot_config) for
                       robot_config in robot_configs]

    if(render):
        
        from roboball2d.rendering import PygletRenderer
        from roboball2d.rendering import RenderingConfig
        
        renderer_config = RenderingConfig(visible_area_width,
                                          visual_height)
        background_color = list(background_color)
        background_color.append(1.0)
        renderer_config.background_color = background_color
        renderer_config.ground_color = ground_color

        class Window:
            width = window_size[0]
            height = window_size[1]
        
        renderer_config.window = Window
        r.renderer = PygletRenderer(renderer_config,
                                    robot_configs,
                                    ball_configs)

    return r
        
