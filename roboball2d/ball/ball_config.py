import numpy as np

class BallConfig:

    """

    Ball Configuration

    Attributes of balls for both rendering and dynamic simulation.
    The dynamics attributes are the one required for usage by the
    B2World dynamic engine based on python b2box. Please refers
    to b2box documentation for their significance and usage.

    Attributes
    ----------
    
    radius : `float`
        in meters

    density : `float`
        see b2box documentation on the significance of density

    ball_drag : `float`
        see b2box documention on the significance of drag

    restitution : `float`
        see b2box documention on the significance of restitution

    color : `tuple of 3 floats`
        (R,G,B), values between 0 and 1

    line_color: `tuple of 3 floats`
        (R,G,B), values between 0 and 1

    """
    
    __slots__=["radius","density",
               "ball_drag","restitution",
               "color","line_color"]
    
    def __init__(self):

        """construct the configuration class, setting default values to attributes"""
        
        self.radius = 0.05
        # for physic engine
        # TODO: Should we lower the ball density
        # to be closer to table tennis?
        self.density = 0.01
        self.ball_drag = 5e-7
        self.restitution = 0.9
        self.color = (1.0,1.0,1.0)
        self.line_color = (0.3,0.3,0.3)
        
