import numpy as np

class DropBallGun:

    """
    Drops a ball, with zero initial velocities, from a desired 
    position. See :py:method:`roboball2d.physics.b2_world.B2World.reset`

    Attributes
    ----------

    x : `float`
        horizontal position 

    y : `float`
        vertical position


    """

    __slots__=["_x","_y"]
    
    
    def __init__(self,
                 x,y):

        """
        Args
        ----

        x : `float`
            horizontal position from which the ball will be droped

        y : `float`
            vertical position from which the ball will be droped

        """
        
        self._x = float(x)
        self._y = float(y)

    def shoot(self):

        """
        Returns
        -------
        a list: position (x,y),angle (radian), 
                linear_velocity (vx,vy), angular_velocity (or spin, radian per second). 
                The angle and the velocities will be zeros
        """

        return [self._x,self._y],0.0,[0.0,0.0],0.0
        
