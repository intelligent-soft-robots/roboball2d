import copy,time
import numpy as np
import numpy.linalg as linalg

from Box2D import (b2PolygonShape,
                   b2World,
                   b2FixtureDef,
                   b2CircleShape,
                   b2ContactListener)

from .world_state import WorldState
from ..utils import arraytize

class _Contacts:

    __slots__=["balls_hits_racket",
               "balls_hits_floor",
               "_nb_balls"]
    
    def __init__(self,nb_balls):

        self._nb_balls = nb_balls
        self.reset()

    def reset(self):
        
        self.balls_hits_racket = [False]*self._nb_balls
        self.balls_hits_floor = [None]*self._nb_balls


class _ContactListener(b2ContactListener):

    """Contact listener for Box2D that registers ball bouncing on the ground
    as well as off the racket."""

    def __init__(self, world, contacts,
                 balls,robots):
        b2ContactListener.__init__(self)
        # instance of b2_world
        self.world = world
        self.contacts = contacts
        # booleans indicating if the related
        # contacts should be managed
        self.balls = balls
        self.robots = robots
        
    # updates the attribute world.contacts
    # i.e. set world.contacts.ball_hits_racket to True
    #      and world.contacts.ball_hists_floor to
    #      ball.position.x (if contact)
    def BeginContact(self, contact):

        fixtureA = contact.fixtureA
        bodyA = fixtureA.body
        fixtureB = contact.fixtureB
        bodyB = fixtureB.body

        bodies = [bodyA, bodyB]

        if self.balls:
            ground_contact = self.world.ground in bodies
            if ground_contact:
                for index,ball in enumerate(self.world.balls):
                    if ball in bodies :
                        self.contacts.balls_hits_floor[index]=ball.position[0]
                        
        if self.balls and self.robots:
            for robot in self.world.robots:
                racket = robot.racket
                if racket in bodies:
                    for index,ball in enumerate(self.world.balls):
                        if ball in bodies :
                            self.contacts.balls_hits_racket[index] = True
                

# resetting the ball = shooting a new ball with the ball gun
def _reset_ball(ball,ball_gun):

    position,angle,lin_vel,ang_vel = ball_gun.shoot()
    ball.position = np.array(position)
    ball.angle = angle
    ball.linearVelocity = np.array(lin_vel)
    ball.angularVelocty = np.array(ang_vel)
        
class B2World:

    """
    Engine using b2box to update the dynamics of robot(s) and 
    ball(s). 
    """
    
    __slots__=["_vel_iters","_pos_iters","_robot_configs",
               "_ball_configs","_time_step","_t","_time_start",
               "_previous_step_time","_applied_step","_contacts",
               "_b2world","ground","balls","robots","_all_desired_torques"]
    
    def __init__(self,
                 robot_configs,
                 ball_configs,
                 visible_area_width,
                 steps_per_sec=100.0,
                 gravitational_acceleration=-8.0,
                 vel_iters = 10,
                 pos_iters = 8):

        """
        Parameters
        ----------

        robot_configs : 
            instance (or list of instances) 
            of :py:class:`roboball2d.robot.default_robot_config.DefaultRobotConfig`
            If a list of instances is passed, several simulated robots will be created.

        ball_configs : 
            instance (or list of instances) 
            of :py:class:`roboball2d.ball.ball_config.BallConfig` 
            if a list of instances is passed, several simulated balls will be created.

        visible_width_area: `float`
            width of the world ground (width of possible contact between object and floor)

        steps_per_second: `float`

            at each call of :py:meth:`roboball2d.physics.b2_world.B2World.step`, 
            a time step of 1.0 / steps_per_second will be applied 
            (except if an argument `current_time` is passed to step, 
             see :py:meth:`roboball2d.physics.b2_world.B2World.step`.

        gravitational_acceleration: `float`
            gravity

        vel_iters : `int`
            ???

        pos_iters : `int`
            ???
        """
        
        self._vel_iters = vel_iters
        self._pos_iters = pos_iters

        # all non changing parameters of the robots
        self._robot_configs = arraytize(robot_configs) 

        # all non changing parameters of the balls
        self._ball_configs = arraytize(ball_configs)

        # ! not necessarily used, as
        # a time point may be passed as argument
        # to the step function (self._time_step
        # used otherwise)
        self._time_step = 1.0/steps_per_sec 
        self._t = 0
        self._time_start = time.time()
        # to compute time steps if time stamp
        # passed as argument of the step function
        self._previous_step_time = None
        self._applied_step = None
        
        # contact listener will update
        # this instance at each iteration
        # to indicate contact between ball
        # and racket/floor
        self._contacts = _Contacts(len(self._ball_configs))
        self._b2world = b2World(
            gravity = (0.,gravitational_acceleration),
            contactListener = _ContactListener(self,self._contacts,
                                               len(self._ball_configs),
                                               len(self._robot_configs)))

        #####################
        # adding the ground #
        #####################
        
        self.ground = self._b2world.CreateStaticBody(
            position = (visible_area_width/2., -10.), 
            shapes = b2PolygonShape(box = (2.*visible_area_width, 10.)),)

        ####################
        # adding the balls #
        ####################

        def _create_ball(ball_config):
            ball_fixture = b2FixtureDef(
                shape = b2CircleShape(pos = (0., 0.), radius = ball_config.radius),
                density = ball_config.density, 
                restitution = ball_config.restitution
            )
            ball_fixture.filter.groupIndex = -1
            ball = self._b2world.CreateDynamicBody(
                position = (visible_area_width, 4),
                fixtures = ball_fixture
            )
            # turn on continuous collision detection for ball as it might otherwise
            # tunnel through racket if relative velocity is high
            ball.bullet = True
            return ball
            
        self.balls = list( map( lambda config: _create_ball(config),
                                self._ball_configs ) )
            
        #####################
        # adding the robots #
        #####################

        self.robots = []
        for robot_config in self._robot_configs:
            b2robot = robot_config.create_b2_robot(self._b2world, self.ground)
            self.robots.append(b2robot)
            
    # uses all the attributes of this call to create an instance
    # of WorldState, which is a class independant of Box2D
    # gathering all what is known about the state of the world
    # at the current iteration
    def _get_world_state(self):
                
        ws = WorldState(self._robot_configs,
                        self._ball_configs)

        ws.t = self._t
        ws.applied_time_step = self._applied_step
        
        # saving infos about balls
        for ws_ball,ball in zip(ws.balls,self.balls):
            ws_ball.position = [ball.position.x,
                                ball.position.y]
            ws_ball.angle = ball.angle
            ws_ball.linear_velocity = list(ball.linearVelocity)
            ws_ball.angular_velocity = ball.angularVelocity

        # all_desired_torque, which contains the desired torques applied
        # to the robot, may not have been set yet. Initializing with None
        # value then
        if not hasattr(self,"_all_desired_torques") or not self._all_desired_torques:
            self._all_desired_torques = [[None]*3]*len(self.robots)

        # saving infos about robots
        for robot,desired_torques in zip(self.robots, self._all_desired_torques):
            robot_state = robot.get_state(desired_torques, self._applied_step)
            ws.robots.append(robot_state)
            
        # saving infos about contacts
        for index in range(len(self.balls)):
            ws.balls_hits_floor[index] = self._contacts.balls_hits_floor[index]
            ws.balls_hits_racket[index] = self._contacts.balls_hits_racket[index]

        if ws.robots:
            ws.robot = ws.robots[0]
        if ws.balls:
            ws.ball = ws.balls[0]
        if ws.balls_hits_floor:
            ws.ball_hits_floor = ws.balls_hits_floor[0]
        if ws.balls_hits_racket:
            ws.ball_hits_racket = ws.balls_hits_racket[0]

        return ws


    def reset(self,
              init_robot_state=None,
              ball_gun=None,
              reset_time=True):

        """
        Reset the simulation 
        
        Parameters
        ----------
        init_robot_state : 
            if not None, 
            instance of :py:class:`roboball2d.robot.default_robot_state.DefaultRobotState`, 
            speciying the new state of the robot. 
            A list of instance must be passed if several robots are managed.

        ball_gun :
            Instance of an object having a shoot method specifying the new position, 
            velocity and spin of the ball (or list of instance if several balls
            are managed. There must be as many ball_guns as managed balls. None can 
            be passed for balls which should not be reset. An error is thrown otherwise). 
            See for example :py:class:`roboball2d.ball_gun.default_ball_gun.DefaultBallGun`

        reset_time :
            if true, the internal time of the simulation is reset to 0

        Returns
        -------
        An instance of :py:class:`roboball2d.physics.world_state.WorldState`
        which captures the state of all items managed by the simulation (after
        the step).

        """
        
        if reset_time:
            self._t = 0
            self._previous_step_time = None
            
        ball_guns = arraytize(ball_gun)
        init_robot_states = arraytize(init_robot_state)

        # checking we have all the ball guns we need
        if not len(ball_guns) == len(self.balls):
            raise Exception("B2World, reset:",len(self.balls),"balls but",
                            len(ball_guns),"ball guns used for reset.")
        
        # resetting the balls using the ball gun
        if ball_guns:
            for ball,ball_gun in zip(self.balls,ball_guns):
                if ball_gun:
                    _reset_ball(ball,ball_gun)

        # resetting the robots using the
        # init_robot function
        if init_robot_states:
            for robot, robot_state in zip(self.robots, init_robot_states):
                robot.set_state(robot_state)

        # return updated world state
        world_state = self._get_world_state()
        return world_state
        
    
    # calls a step of the simulation,
    # applying the torques to the robot
    def step(self,
             all_torques,
             relative_torques=False,
             current_time=None,
             mirroring_robot_states={}):

        """
        Performs a simulation step. 
        
        Parameters
        ----------

        all_torques : 
            list of 3 torques (for a single robot) or 
            list of list of 3 torques (for several robots) to apply to the joints
        
        relative torques : `Bool`
            if true, the torques specified do not use absolute value, 
            but relative values between -1 and 1 (that will be mapped between
            (-max torque, +max torque)
        
        current_time : `float`
            if provided, the time step will not be based on the step per second 
            (:py:class:`roboball2d.physics.b2_world.B2World` 
            but based on the current_time argument passed during the previous call 
            to step

        mirroring_robot_state: `dict`
            dictionary {index:robot_state}, with robot state being an instance
            of :py:class:`roboball2d.robot.default_robot_state.DefaultRobotState`.
            This will force the robot of the specified index to take the 
            specified state, overwriting all control and dynamics.

        Returns
        -------
        
        An instance of :py:class:`roboball2d.physics.world_state.WorldState`
        which captures the state of all items managed by the simulation (after
        the step).

        """
        
        # the code in this function will use
        # torques, angles and angular_velocities
        # as : [ (v1,v2,v3), (v1,v2,v3) ... ]
        # (several robots supported, 3 values per robot)
        # but the user may choose to pass only [v1,v2,v3]
        # (i.e. values for one robot)
        # Code below "transorms" [v1,v2,v3]
        # into [(v1,v2,v3)]

        if all_torques is not None:
            if len(all_torques)==3 :
                try :
                    list(all_torques[0])
                except:
                    all_torques = [all_torques]

        # will used to save the torques sent to robot
        # (may be different to all_torques, as applied
        # torques may be capped between min and max values)
        # We initialize as copy of all_torques only
        # to makes sure we have the correct shape
        self._all_desired_torques = copy.deepcopy(all_torques)
            
        # mirroring info can be used to force the robot(s) to move
        # according to data passed to the step function rather than
        # by applying the physics. Typically to mirror another robot.
        # expected : either instance of MirroringInfo (see mirroring_info.py)
        # or dict {robot_index:MirroringInfo} if only some of the robot
        # are to be controlled this way.
        if mirroring_robot_states:
            # if mirroring_info is just an instance, transforming it
            # into a dict, for consistancy
            if not isinstance(mirroring_robot_states,dict):
                mirroring_robot_states = {0:mirroring_robot_states}

        # if relative torques, the user did not enter torques directly,
        # but a ratio to the max torque between -1 and 1 
        # converting here this "relative" torque to the value to apply
        if all_torques and relative_torques:
            for index,robot_config in enumerate(self._robot_configs):
                torques = all_torques[index]
                all_torques[index]=[ t*max_t for t,max_t
                                     in zip(torques,
                                            robot_config.max_torques) ]
                
        # increasing time
        # user did not provide a time stamp,
        # using the predefine time step
        if current_time is None:
            self._t += self._time_step
            self._applied_step = self._time_step
        # user did provide a time stamp,
        # computing the time step
        else :
            if self._previous_step_time is None:
                self._previous_step_time = current_time
            self._applied_step = current_time - self._previous_step_time
            self._t += current_time - self._time_start
            self._previous_step_time = current_time

        # updating the robots
        if all_torques:
            for index1,(generalized_torques,robot) in enumerate(zip(all_torques, self.robots)):
                applied_torques = robot.apply_generalized_torques(generalized_torques)
                self._all_desired_torques[index1] = applied_torques

                
        # aerodynamic drag on the balls
        for ball,ball_config in zip(self.balls,self._ball_configs):
            ball.ApplyForce(-ball_config.ball_drag*linalg.norm(
                ball.linearVelocity)*ball.linearVelocity, 
                            ball.position, wake = True)

        self._b2world.Step(self._applied_step,
                           self._vel_iters,
                           self._pos_iters)
        self._b2world.ClearForces()

        # check if robot dynamics are to be overwritten
        # by mirroring information (i.e. mirroring another robot
        # rather than applying control)
        if mirroring_robot_states :
            for index,robot_state in mirroring_robot_states.items():
                # NOTE: I assume that mirroring_infor gives a robot state. This state can easily be obtained
                # by calling the method get_state of a B2Robot. TODO: Adapt mirroring_info
                self.robots[index].set_state(robot_state)

        # updating the world state
        world_state = self._get_world_state()

        # reseting the contacts
        self._contacts.reset()
        
        return world_state

    
        
