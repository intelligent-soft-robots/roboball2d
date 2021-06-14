import numpy as np

from Box2D import (b2PolygonShape,
                   b2World,
                   b2FixtureDef,
                   b2ContactListener)

from ..robot.default_robot_state import DefaultRobotState
from .b2_robot import B2Robot

class DefaultB2Robot(B2Robot):

    """
    (Advanced usage)

    Instances of DefaultB2Robot will be created internally by 
    :py:class:`roboball2d.physics.b2_world.B2World` based on the 
    attributes of the instane of `roboball2d.robot.default_robot_config.DefaultRobotConfig`
    passed to its constructor.

    Users code is not expected to create new instances of DefaultB2Robot.

    Advanced users may create new robot configuration object and new B2Robot object
    (inheriting from :py:class:`robotball2d.physics.b2_robot.B2Robot`) to fine tune
    how B2World manages the dynamics of robots.
    """
    
    def __init__(self, robot_config, b2_world, ground):

        self.robot_config = robot_config
        self._robot_state = DefaultRobotState(self.robot_config)

        # adding the rods

        rod_fixture = b2FixtureDef(
            shape = b2PolygonShape(box = (0.5*robot_config.rod_diameter,
                                          0.5*robot_config.rod_length)),
            density = robot_config.rod_density)
        rod_fixture.filter.groupIndex = -1

        self.rods = []

        y_pos = 0.5*robot_config.rod_length
        for _ in range(2):
            b2_rod = b2_world.CreateDynamicBody(
                position = (robot_config.position, y_pos),
                fixtures = rod_fixture
            )
            b2_rod.linearDamping = robot_config.linear_damping
            b2_rod.angularDamping = robot_config.angular_damping
            self.rods.append(b2_rod)
            y_pos += robot_config.rod_length

        # adding the rackets

        racket_fixture = b2FixtureDef(
            shape = b2PolygonShape(box = (0.5*robot_config.racket_diameter,
                                          0.5*robot_config.racket_thickness ) ),
            density = robot_config.racket_density,
            restitution = robot_config.racket_restitution)

        self.racket = b2_world.CreateDynamicBody(
            position = (robot_config.position,
                        2.*robot_config.rod_length + 0.5*robot_config.racket_thickness),
            fixtures = racket_fixture)
        self.racket.linearDamping = robot_config.linear_damping
        self.racket.angularDamping = robot_config.angular_damping
        
        # adding joints

        self.joints = [None,None,None]

        # items : rods + racket
        dyn_items = self.rods+[self.racket]
        previous_dyn_item = ground
        previous_length = 0

        for index,(robot_item,
                   dyn_item) in enumerate(zip(robot_config.items,
                                              dyn_items)):

            self.joints[index] = b2_world.CreateRevoluteJoint(
                bodyA = previous_dyn_item, 
                bodyB = dyn_item, 
                anchor = (robot_config.position, previous_length),
                lowerAngle = -robot_item.joint_limit,
                upperAngle = +robot_item.joint_limit,
                enableLimit = True,
                enableMotor = True)

            previous_length = previous_length + robot_item.length
            previous_dyn_item = dyn_item

    def set_state(self, robot_state):
        for state_rod,world_rod in zip(robot_state.rods,self.rods):
            world_rod.position = state_rod.position
            world_rod.angle = state_rod.angle
            world_rod.linearVelocity = state_rod.linear_velocity
            world_rod.angularVelocity = state_rod.angular_velocity

        self.racket.position = robot_state.racket.position
        self.racket.angle = robot_state.racket.angle
        self.racket.linearVelocity = robot_state.racket.linear_velocity
        self.racket.angularVelocity = robot_state.racket.angular_velocity

        for joint in self.joints:
            joint.maxMotorTorque = 0
            joint.motorSpeed = 0

    def get_state(self, desired_torques, applied_step = None):

        for state_joint, world_joint, desired_torque in zip(self._robot_state.joints,
                                                           self.joints,
                                                           desired_torques):
            state_joint.desired_torque = desired_torque
            state_joint.angle = world_joint.angle
            state_joint.angular_velocity = world_joint.speed
            state_joint.anchor = list(world_joint.anchorA)
            if applied_step is not None and applied_step != 0: 
                state_joint.torque = world_joint.GetMotorTorque(1.0/applied_step)
            else:
                state_joint.torque = None

        for state_rod,world_rod in zip(self._robot_state.rods,self.rods):
            state_rod.position=list(world_rod.position)
            state_rod.angle=world_rod.angle
            state_rod.linear_velocity = list(world_rod.linearVelocity)
            state_rod.angular_velocity = world_rod.angularVelocity
            state_rod.desired_torque = None

        self._robot_state.racket.position = list(self.racket.position)
        self._robot_state.racket.angle = self.racket.angle
        self._robot_state.racket.linear_velocity = list(self.racket.linearVelocity)
        self._robot_state.racket.angular_velocity = self.racket.angularVelocity
        self._robot_state.racket.desired_torque = None
        
        return self._robot_state

    def apply_generalized_torques(self, generalized_torques):
        applied_torques = []
        for (joint,
                    torque,
                    max_torque) in zip(self.joints,
                                                 generalized_torques,
                                                 self.robot_config.max_torques):
            
            # robot will apply maxMotorTorque to achieve 
            # a motor speed which is seed to a very high value
            # (effectively implementing torque control)
            s = np.sign(torque)*self.robot_config.max_motor_speed
            joint.motorSpeed = s
            # clip torque by maximum motor torque
            t = min(abs(torque),max_torque)
            joint.maxMotorTorque = t
            # saving applied torques
            applied_torques.append(t)
        return applied_torques

