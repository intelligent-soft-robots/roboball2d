import numpy as np

from .robot_config import RobotConfig
from ..physics.default_b2_robot import DefaultB2Robot

class _Rod:

    def __init__(self,joint_limit,length):

        self.joint_limit = joint_limit
        self.length = length
        
class _Racket(_Rod):

    def __init__(self,joint_limit):

        _Rod.__init__(self,joint_limit,0.0)
        
class DefaultRobotConfig:

    """
    Configuration required to render and compute the dynamics of 3 dof robot
    consisting of 2 rods and a racket (and 3 related joints).
    User code may change values of the attributes after instantiation.

    Attributes
    -----------
    
    position:
    x position of the robot (in meters) 
        
    max_torques:
    (3d tuple of floats) max torques that can be applied on joints 
        
    max_motor_speed:
        (float) max motor speed. 
        If using b2world as dynamic engine, it will be the 
        speed the dynamic engine will try to impose on all joints at all time. 
        User control will be  achieved by limiting the maximum torque the engine 
        will be allowed to apply on joints. 
        If the engine can attain this maximum speed without 
        applying the maximum torque set by the user code, 
        then the user code looses the ability to directly control the robot
    
    rod_diameter:
        (float) in meters, will be applied for the 2 rods
        
    rod_length:
        (float) in metters, will be applied for the 2 rods

    rod_density
        (float) applied on the 3 rods. See b2box documentation on density
        
    rod_joint_limit
        (float) angle limit (radian) for the 2 rods 
        (will be between - and + this value)
        
    rods:
        (2d array of Rod) each rod as a rob_joint_limit and a rod_length attribute 

    racket_diameter:
        (float) in meters
        
    racket_thickness:
        (float) in meters
        
    racket_density:
        (float) see box2d documentation on significance of density
        
    racket_restitution:
        (float) see box2d documentation on significance of density
        
    racket_joint_limit:
        (float) racket joint limit in radian (+/- this value)
        
    racket:
        instance of Racket, which has joint_limit attribute
        
    joint_radius:
        (float) in meters

    items:
        Array of 3 instances : 2 Rod, 1 Racket
        
    rod_color:
        (3d tuple of float) color of rods (R,G,B), values between 0 and 1
        
    racket_color:
        (3d tuple of float) color of rods (R,G,B), values between 0 and 1
        
    joint_color:
        (3d tuple of float) color of rods (R,G,B), values between 0 and 1

    linear_damping:
        (float) in [0, infty), higher values cause stronger damping of 
        linear velocity of rods and racket

    angular_damping:
        (float) in [0, infty), higher values cause stronger damping of 
        angular velocity of rods and racket


    """
    
    __slots__=["position","max_torques","max_motor_speed",
               "rod_diameter","rod_length","rod_density",
               "rod_joint_limit","rods","racket_diameter",
               "racket_thickness","racket_density","racket_restitution",
               "racket_joint_limit","joint_radius","items","rod_color",
               "racket","racket_color","joint_color", "linear_damping",
               "angular_damping"]
    
    def __init__(self):

        self.position = 1.0
        self.max_torques = (0.14,
                            0.07,
                            0.03)
        self.max_motor_speed = 200.
        self.rod_diameter = 0.05
        self.rod_length = 0.5
        self.rod_density = 0.1
        self.rod_joint_limit = 0.7*np.pi
        self.rods = [_Rod(self.rod_joint_limit,
                          self.rod_length),
                     _Rod(self.rod_joint_limit,
                          self.rod_length)]
        self.racket_diameter = 0.5
        self.racket_thickness = 0.03
        self.racket_density = 0.1
        self.racket_restitution = 0.75
        self.racket_joint_limit = 0.3*np.pi
        self.racket = _Racket(self.racket_joint_limit)
        self.joint_radius = self.rod_diameter
        self.items = self.rods + [self.racket]
        self.rod_color = (0.8, 0.8, 0.8)
        self.racket_color = (0.8, 0.0, 0.0)
        self.joint_color = (0.3, 0.3, 0.3)
        self.linear_damping = 0.0
        self.angular_damping = 0.0

    def create_b2_robot(self, b2world, ground):
        """
        (Advanced usage)

        This function is not meant to be used directly by the user code. It will
        be called in the constructor of tennis2d.physics.B2World to generate,
        based on this configuration, an instance of an object suitable for
        dynamic update of the robot.

        Parameters
        ----------
        
        b2world : 
            an instance of tennis2d.physics.B2World

        ground (float): 
            y position of the robot

        Returns
        -------
        An instance of :py:class:`roboball2d.physics.default_b2_robot.DefaultB2Robot`

        """
        return DefaultB2Robot(self, b2world, ground)

