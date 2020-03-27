

class RenderingConfig:

    """
    Provides rendering configuration. User code may change values
    of the attribute after instantiation.

    Parameters
    ----------

    visible_area_width: `float`
        how much width (in meters) will be displayed

    visual_height: `float`
        how much height (in meters) will be displayed

    Attributes
    ----------
    
    background_color:
        (R,G,B) (values between 0 and 1)

    ground_color:
        (R,G,B) (values between 0 and 1)

    window :
        instance with 2 attributes: width and height (in pixels)
    
    location:
        (x,y) desired location of the window, in pixels.
        (note that renderers may or may not be able to impose it)

    """

    __slots__=["background_color","ground_color",
               "window","visual_height","visible_area_width",
               "location"]
    
    def __init__(self,
                 visible_area_width,
                 visual_height):

        
        
        class Window:
            def __init__(self):
                self.width=1600
                self.height=800
                
        self.background_color = (0.0, 0.1, 0.4, 1.0)
        self.ground_color = (0.0, 0.3, 0.0)
        self.window = Window()
        self.visual_height = visual_height
        self.visible_area_width = visible_area_width
        self.location = [0,0]
                
