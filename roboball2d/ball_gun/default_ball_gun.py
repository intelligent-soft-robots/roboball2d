import numpy as np

class DefaultBallGun:

    """
    A ball gun provides, via its method 'shoot', an initial ball
    position (x,y), angle (radian), linear velocity (vx,vy) and 
    angular velocity (or spin). Users can use an instance of
    DefaultBallGun, as documented here, or create new ball guns objects
    (which just need to implement a 'shoot' method).

    DefaultBallGun initialize balls by sampling normal distribution to 
    determine the balls initial positions and velocities. 
    User code may change the values of the attributes after construction
    to match his/her need

    Attributes
    ----------
    
    initial_pos_x  : `float`
        in meters

    initial_height_mean : `float`
        in meters

    initial_height_std : `float`
        in meters

    speed_mean : `float`
        in meters per second

    speed_std : `float`
        in meters per second

    spin_std : `float`
        in radians per second

    vel_angle_min : `float`
        in radians per second

    vel_angle_max : `float`
        in radians per second
   
    """
    
    __slots__=["_radius","initial_pos_x","initial_height_mean",
               "initial_height_std","speed_mean","speed_std",
               "spin_std","vel_angle_min","vel_angle_max"]
    
    
    def __init__(self,
                 ball_config):

        """
        Creates an instance of ball gun setting default values to all 
        attributes.

        Args
        ----

        ball_config : :py:class:`roboball2d.ball.BallConfig`
            used to set the radius of the ball that will be shot
        """
        
        self._radius = ball_config.radius

        self.initial_pos_x = 6.0
        self.initial_height_mean = 1.2
        self.initial_height_std = 0.1
        self.speed_mean = 5.4
        self.speed_std = 0.2
        self.spin_std = 5.0
        self.vel_angle_min = -np.pi*0.1
        self.vel_angle_max = np.pi*0.1
        

    def shoot(self):

        """
        Returns
        -------
        a list: position (x,y),angle (radian), 
                linear_velocity (vx,vy), angular_velocity (or spin, radian per second). 
                These values are created by sampling the normal distributions.
        
        """

        position = [self.initial_pos_x,
                    max(np.random.normal(
                        self.initial_height_mean,
                        self.initial_height_std),
                        4.0*self._radius)]
        
        angle = 0.
    
        speed = np.random.normal(self.speed_mean,
                                      self.speed_std)
        phi = np.random.uniform(self.vel_angle_min,
                                     self.vel_angle_max)

        linear_velocity = [-speed*np.cos(phi),
                           speed*np.sin(phi)]
        angular_velocity = np.random.normal(0.0,
                                            self.spin_std)
        
        return position,angle,linear_velocity,angular_velocity
