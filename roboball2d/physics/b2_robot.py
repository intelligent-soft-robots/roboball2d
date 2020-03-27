class B2Robot:

    """
    Specifies the interface required by :py:class:`roboball2d.physics.B2World`
    to update the state of a robot. See :py:class:`roboball2d.physics.DefaultB2Robot`
    for an example of a class inherating from B2Robot. 
    """
    
    def __init__(self, robot, b2_world, ground):
        raise NotImplementedError("__init__ not implemented.")

    def set_state(self, robot):
        raise NotImplementedError("set_state not implemented.")

    def get_state(self):
        raise NotImplementedError("get_state not implemented.")

    def apply_generalized_torques(self, generalized_torques):
        """Apply generalized torques and return actually applied generalized
        torques."""
        raise NotImplementedError("apply_generalized_torques not implemented.")
