from ..item import Item
from ..robot import RobotState

class WorldState:

    """
    An instance of WorldState captures the state of all
    object of a simulation. Returned for example by 
    :py:meth:`roboball2d.physics.b2_world.B2World.reset` and
    :py:meth:`roboball2d.physics.b2_world.B2World.step` and

    Attributes
    ----------

    robot_configs:
        list of the configurations of the robots managed by the simulation
        see :
        py:class:`roboball2d.robot.default_robot_configuration.DefaultRobotConfiguration`
    
    robot_config: 
        instance at index 0 of robot_configs

    ball_configs:
        list of the configurations of the balls managed by the simulation
        see :
        py:class:`roboball2d.ball.ball_configuration.BallConfiguration`

    t: `float`
        current simulation time (in seconds)

    applied_time_step: `float`
        duration of the time step applied (in seconds)

    robots: 
        list of states of robots, 
        see :py:class:`roboball2d.robot.default_robot_state.DefaultRobotState`

    robot: 
        instance at index 0 of robots
    
    balls :
        list of ball items, see :py:class:`roboball2d.item.Item`

    ball :
        instance at index 0 of balls

    balls_hits_floor:
        list of float or None values, one per managed ball.
        None at a given index means the ball at this index did not hit the floor
        during the last simulation step. A float gives the x position at which
        the ball touched the floor.

    ball_hits_floor:
        value at index 0 of balls_hits_floor.

    balls_hits_racket:
        list of index or None values, one per managed ball.
        None at a given index means the ball at this index did not hit any racket
        during the last simulation step. An integer gives the index of the robot
        which racket the ball touched.

    ball_hits_racket:
        value at index 0 of balls_hits_racket

    """
    
    @staticmethod
    def _arraytize(v):
        if v is None:
            return None,[]
        try :
            v = list(v)
            if len(v)==0:
                return None,[]
            return v[0],v
        except :
            return v,[v]
    

    __slots__=["robot_config","robot_configs",
               "robots","robot",
               "ball_config","ball_configs",
               "balls","ball",
               "t","applied_time_step",
               "ball_hits_floor","balls_hits_floor",
               "ball_hits_racket","balls_hits_racket"]
        
    def __init__( self,
                  robot_configs,
                  ball_configs ) :

        # if not already arrays (i.e. 1 entry per robot/ball)
        # transform robot_configs and ball_configs into arrays
        # (i.e. if robot_configs is just 1 instance, then
        # robot_configs=[robot_configs]
        self.robot_config,self.robot_configs = self._arraytize(robot_configs)
        self.ball_config,self.ball_configs = self._arraytize(ball_configs)

        self.robots = []

        self.balls = [Item() for _
                      in self.ball_configs]
        try:
            self.ball = self.balls[0]
        except:
            self.ball = None
        try:
            self.robot = self.robots[0]
        except:
            self.robot = None
        self.t = None
        self.applied_time_step = None
        self.balls_hits_floor = [None for _
                                 in self.ball_configs]
        self.ball_hits_floor = None
        self.balls_hits_racket = [False for _
                                  in self.ball_configs]
        self.ball_hits_racket = False

        
    def __str__(self):

        values = [attr+": "+str(getattr(self,attr))
                  for attr in self.__slots__ ]
        return "world state:\n\t"+"\n\t".join(values)
