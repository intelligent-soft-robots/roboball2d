import math,random,time

from roboball2d import factory
from roboball2d.item import Item

def run(rendering=True):

    """
    Runs the mirror balls demo, in which the robot moves according to random
    torques as 2 balls are imposed computed trajectories.
    You may run the executable roboball2d_mirror_balls_demo after install.

    Parameters
    ----------

    rendering : 
        renders the environment if True
    
    """


    # default physics and rendering, with 10 balls.
    # The first ball will be pink.
    r2d = factory.get_default(nb_balls=2,
                              ball_colors={0:(1,0.08,0.57),
                                           1:(0.08,1.0,0.57)},
                              render=rendering)
    

    # running 10 episodes, max 3 seconds per episode
    n_episodes = 0

    for episode in range(10):

        # will be used to impose trajectories on the balls
        start_position = [6.0,0.0]
        ball1 = Item()
        ball2 = Item()
        ball1.position = start_position
        ball2.position = start_position
        vy = 0
        
        # tracking the number of times the ball bounced
        n_bounced = 0

        # reset before a new episode
        r2d.world.reset(r2d.robot_reinit,
                        r2d.ball_guns)
        
        while True:

            # imposing velocity on the ball
            vy+=0.01
            ball1.linear_velocity = (-2.0,0.5*math.cos(vy))
            ball2.linear_velocity = (-2.0,0.5*math.sin(vy))

            # random torques
            torques = [random.uniform(-1.0,1.0) for _ in range(3)]

            # returns a snapshot of all the data computed
            # and updated by the physics engine at this
            # iteration 
            world_state = r2d.world.step(torques,relative_torques=True,
                                         mirroring_ball_states={0:ball1,1:ball2})

            # updating position of balls after step
            ball1.position = world_state.balls[0].position
            ball2.position = world_state.balls[1].position
            
            # episode ends 
            # if the number of bounces is 2 or above
            # for the first ball ...
            if world_state.ball_hits_floor :
                n_bounced += 1
                if n_bounced >= 2:
                    break

            # ... or if 3 seconds passed
            if world_state.t > 3:
                break

            # render based on the information provided by
            # the physics engine
            if rendering:
                r2d.renderer.render(world_state,
                                    time_step=1.0/60.0)


