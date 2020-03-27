

class PDController:

    """
    
    PDController : a simple PD controller for 3dofs robot 
    
    """

    
    __slots__=["_kp","_kd"]
    
    def __init__(self,
                 kp=[2.0,1.0,0.5],
                 kd=[0.35,0.2,0.05]):
        """
        Parameters
        ----------
            kp (3d array of floats) : 
                 proportional gains

            kd (3d array of floats) : 
                 derivative gains
        """

        self._kp = kp
        self._kd = kd

    def get(self,
            references,
            angles,
            angular_velocities):
        """
        Parameters
        ----------

        references: 
            3d list of desired angle values

        angles: 
            3d list of current angle values

        angular_velocities: 
            3d list of current angular velocities


        Returns
        -------

        a 3d list of torques
        
        """

        def _compute(kp,kd,
                    ref,angle,
                    angular_velocity):

            error = ref-angle
            return kp*error -kd*angular_velocity

        return list(map(lambda kp,kd,r,a,av:_compute(kp,kd,
                                                     r,a,av),
                        self._kp,self._kd,
                        references,
                        angles,angular_velocities))

    
