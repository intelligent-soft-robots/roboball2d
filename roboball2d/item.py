class Item:

    """
    Data structure for encapsulating the state of various objects.

    Attributes
    ----------

    position : `list of 2 floats`
         (x,y) in meters
    angle : `float`
         in radian
    linear_velocity : `list of 2 floats`
         (vx,vy) in meters per seconds
    angular_velocity: `float`
         in radian per second
    torque : `float`
         measured torque
    desired_torque: `float`
         desired torque as set by control
    anchor : `float`
         ????

    """
    
    __slots__=["position","angle",
               "linear_velocity","angular_velocity",
               "torque","desired_torque","anchor"]

    def __init__(self):
        """
        set all attributes values to 0 (or list of zeros)
        """
        self.position = [0,0]
        self.angle = 0
        self.linear_velocity = [0,0]
        self.angular_velocity = 0
        self.torque = 0 # torques "measured"
        self.desired_torque = 0 # torques applied
        self.anchor = 0

    def __str__(self):
        return "\t\t"+"\n\t\t".join([attr+":\t"+str(getattr(self,attr))
                                 for attr in self.__slots__])
