import numpy as np


class Box:

    """
    Convenience class for creating gym spaces Box
    from a dictionary : 
    {key:(min value,max value)}
    Once an instance of Box created, this instance
    has read/write attributes corresponding to the
    keys. For example::

        d = {"a":(1,2),
             "b":(-1,1)}

        box = Box(d)

        box.a = 1.2
        box.b = 0.1
    
    The get_space and get_box methods can be used
    to get respecively the gym space or the 
    numpy arrays of attributes

    """
    
    
    # d : dictionary {attr:(min,max)}
    def __init__(self,
                 d,
                 dtype=np.float32,
                 shape=None):

        """
        Parameters
        ----------
          
        d : 
            dictionary of attributes (keys) associated
            to a tuple of related min and max values

        """
        
        self._attributes = sorted(d.keys())

        mins = [d[attr][0]
                for attr in self._attributes ]
        maxes = [d[attr][1]
                 for attr in self._attributes ]

        self.box = spaces.Box(
            low = np.array(mins),
            high = np.array(maxes),
            shape=shape,
            dtype=dtype)

        for attr in self._attributes:
            setattr(self,attr,None)

    def get_space(self):
        """
        returns the corresponding gym space
        """
        return self.box
            
    def get_box(self):
        """
        returns the corresponding numpy array
        """
        return np.array([getattr(self,attr)
                         for attr in self._attributes])
                



def arraytize(v):
    """
    convenience function that "transforms" its arguments
    into a list. If the argument is already a list, returns
    it. If the argument is None, returns an empty list. 
    Otherwise returns [argument].
    """
    if v is None:
        return []
    try :
        return list(v)
    except :
        return [v]
