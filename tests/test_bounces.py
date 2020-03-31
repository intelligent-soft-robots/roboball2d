import unittest,time

from roboball2d.ball_gun import DropBallGun
from roboball2d.physics import B2World
from roboball2d.robot import DefaultRobotConfig
from roboball2d.robot import DefaultRobotState
from roboball2d.ball import BallConfig


class BOUNCES_TESTCASE(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_vertical_drop_over_ground(self):

        # droping a ball, and checking the ball
        # is reported at touching the floor at the
        # expected position

        x = 4.0
        y = 1.0

        ball_gun = DropBallGun(x,y)

        world = B2World([], # no robot
                        BallConfig(),
                        6.0)

        world.reset(None, # no robot
                    ball_gun)

        time_start = time.time()

        ball_bounce_x = None

        # running for a max time of 1 seconds
        while time.time()-time_start < 1 :

            world_state = world.step(None) # None: no robot

            bounce = world_state.ball_hits_floor
            if bounce:
                ball_bounce_x = bounce
                break

        # the ball did not bounce
        self.assertTrue(ball_bounce_x is not None)

        # the ball should have bounced after dropping vertically
        self.assertEqual(ball_bounce_x,x)

    def test_vertical_drops_over_ground(self):

        # droping 2 balls, and checking the balls
        # are reported at touching the floor at the
        # expected position

        pos1 = [4,1]
        pos2 = [5,1]
        positions = [pos1,pos2]
        
        ball_guns = [DropBallGun(*pos)
                     for pos in positions]

        world = B2World([], # no robot
                        [BallConfig(),BallConfig()],
                        6.0)

        world.reset(None, # no robot
                    ball_guns)

        time_start = time.time()

        balls_bounce_x = [None]*2

        # running for a max time of 1 seconds
        while time.time()-time_start < 1 :

            world_state = world.step(None) # None: no robot

            bounces = world_state.balls_hits_floor

            for index,bounce in enumerate(bounces):
                if bounce:
                    balls_bounce_x[index]=bounce

            if all([b is not None for b in balls_bounce_x]):
                break

        for index, bounce in enumerate(balls_bounce_x):
            
            # the ball did not bounce
            self.assertTrue(bounce is not None)
            
            # the ball should have bounced after dropping vertically
            self.assertEqual(bounce,positions[index][0])


    def test_vertical_drops_over_robot(self):

        # droping 3 balls, 2 above robot and
        # 1 somewhere else. Checking the 2 first balls
        # do bounce on the racket, and 3rd one does not

        robot_base = 4.0
        pos1 = [4.05,1.0]
        pos2 = [3.95,1.0]
        pos3 = [7.0,1.0]
        positions = [pos1,pos2,pos3]
        
        ball_guns = [DropBallGun(*pos)
                     for pos in positions]

        robot_config = DefaultRobotConfig()
        robot_config.position = robot_base
        init_robot_state = DefaultRobotState(robot_config,
                                             [0.0 for _ in positions],
                                             [0.0 for _ in positions])
        
        world = B2World(DefaultRobotConfig(),
                        [BallConfig() for _ in positions],
                        6.0)

        world.reset(init_robot_state, 
                    ball_guns)

        time_start = time.time()

        touched_racket = [False]*3

        while time.time()-time_start < 0.5 :

            world_state = world.step(None) 

            bounces = world_state.balls_hits_racket

            for index,bounce in enumerate(bounces):
                if bounce : touched_racket[index]=True

        self.assertTrue(touched_racket[0])
        self.assertTrue(touched_racket[1])
        self.assertFalse(touched_racket[2])
        
            
        
