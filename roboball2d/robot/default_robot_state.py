from copy import copy

import numpy as np

from ..item import Item
from .robot_state import RobotState

class DefaultRobotState(RobotState):

    """
    An instance of robot state fully describes the state of a 3dof robot
    (2 rodes and a racket, with 3 corresponding joints). It is used for example
    in :py:class:`roboball2d.physics.world_state.WorldState`.

    Attributes
    ----------

    robot_config:
         configuration of the robot used to update its dynamics or for rendering
         it. See :py:class:`roboball2d.robot.default_robot_config.DefaultRobotConfig`

    rods:
         list of two :py:class:`roboball2d.item.Item` 

    racket
         an instance of :py:class:`roboball2d.item.Item` 

    joints
         list of three instances of :py:class:`roboball2d.item.Item` 

    """

    __slots__=["robot_config","rods",
               "racket","joints"]
    
    def __init__(self, robot_config, generalized_coordinates = None,
                 generalized_velocities = None):

        """
        Parameters
        ----------

        robot_config:
            configuration of the robot used to update its dynamics or for rendering
            it. See :py:class:`roboball2d.robot.default_robot_config.DefaultRobotConfig`

        generalized_coordinates: list of floats
            angles (in radian) of the three joints. Angles will be set to 0 
            if None

        generalized_velocities: list of floats
            angular velocities of the three joints, which will be set to 0
            if None
        """
        
        self.robot_config = robot_config

        if generalized_coordinates is None:
            j_angles = [0.0 for _ in range(3)]
        else:
            j_angles = generalized_coordinates

        if generalized_velocities is None:
            j_angular_vel = [0.0 for _ in range(3)]
        else:
            j_angular_vel = generalized_velocities

        self.rods = [Item() for _ in range(2)]
        self.racket = Item()
        self.joints = [Item() for _ in range(3)]

        self._forward_kinematics(j_angles, j_angular_vel)

    def _forward_kinematics(self, joint_angles, joint_angular_vel):
        # Compute position, orientation, linear and angular velocity
        # of robot parts from joint angles and angular velocities

        x = self.robot_config.position
        rl = self.robot_config.rod_length
        rt = self.robot_config.racket_thickness

        items = self.rods+[self.racket]

        lengths = [rl, rl, rt]
        position = [x, 0.0]
        angle = 0.0
        velocity = [0.0, 0.0]
        ang_velocity = 0.0

        angles = []
        centers = []

        counter = 0

        assert len(joint_angles) == 3 and len(joint_angular_vel) ==3

        # calculate center and angles of rods and racket
        # as well as linear and angular velocities
        for item, joint, length, joint_angle, joint_ang_vel \
                in zip(items, self.joints, lengths, joint_angles, joint_angular_vel):
            angle += -joint_angle

            joint.anchor = copy(position)

            position_increment = [0.5*length*np.sin(angle), 
                    0.5*length*np.cos(angle)]
            position = [x + dx for x, dx in zip(position, position_increment)]
            item.position = copy(position)
            item.angle = -copy(angle)
            position = [x + dx for x, dx in zip(position, position_increment)]

            ang_velocity += -joint_ang_vel
            item.angular_velocity = -copy(ang_velocity)

            velocity_increment = [0.5*length*np.cos(angle)*ang_velocity, 
                0.5*length*np.sin(angle)*ang_velocity]
            velocity = [v + dv for v, dv in zip(velocity, velocity_increment)]
            item.linear_velocity = copy(position)
            velocity = [v + dv for v, dv in zip(velocity, velocity_increment)]

            counter += 1

    def render(self, color = None):
        from ..rendering.pyglet_utils import draw_rod, draw_racket, draw_circle_sector
        for rod in self.rods: 
            draw_rod(rod.position,
                     rod.angle,
                     self.robot_config.rod_diameter,
                     self.robot_config.rod_length,
                     self.robot_config.rod_color if color is None else color)
        draw_racket(self.racket.position,
                    self.racket.angle,
                    self.robot_config.racket_diameter,
                    self.robot_config.racket_thickness,
                    self.robot_config.racket_color if color is None else color)
        centers = [joint.anchor for joint in self.joints]
        angles = [0., self.rods[0].angle, self.racket.angle + np.pi]
        triangles_to_draw = [8, 16, 8]
        for center, angle, m in zip(centers, angles, triangles_to_draw):
            draw_circle_sector(
                    center = center, 
                    angle = angle, 
                    radius = self.robot_config.joint_radius, 
                    n = 16, 
                    color = self.robot_config.joint_color if color is None else color, 
                    triangles_to_draw = m)


    def __str__(self):
        rods = ["rod "+str(n)+":\n"+str(rod) for n,rod in enumerate(self.rods)]
        joints = ["joint "+str(n)+":\n"+str(joint)
                  for n,joint in enumerate(self.joints)]
        return "\n\t"+"\n\t".join(joints)+"\n\tracket:\n"+str(self.racket)+"\n\t".join(rods)
