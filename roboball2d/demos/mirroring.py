import math,random,time,multiprocessing,copy,pickle

from roboball2d.physics import B2World
from roboball2d.robot import DefaultRobotConfig
from roboball2d.robot import DefaultRobotState
from roboball2d.ball import BallConfig
from roboball2d.ball_gun import DefaultBallGun


def _parallel_world(data,lock):

    # robot of this function mirrors the robot controlled
    # in the function _run_world (declared below)

    # data and lock : used for sharing of data between
    # _parallel_world and _run_robot

    # _parallel_world and _run_robot need to run in 2 different
    # processes because, for some unknown reason, 2 instances of B2World
    # running in the same processes crash with segfault.

    # setting up the robot and the world
    
    robot_config = DefaultRobotConfig()
    ball_configs = []
    visible_area_width = 6.0
    visual_height = 0.05
    world = B2World(robot_config,
                     ball_configs,
                     visible_area_width)
    robot_init = DefaultRobotState(robot_config)
    world.reset(robot_init)

    # running until the run_robot process stops
    running = True
    while running:

        world_state = None
        
        with lock:
            # getting the world state of the robot
            # running in run robot
            running = data["running"]
            if data["new_data"]:
                world_state_str = data["world_state"]
                world_state = pickle.loads(world_state_str)
                data["new_data"]=False

        if world_state:

            # mirroring the robot
            mirroring_robot_state = world_state.robot
            world_state2 = world.step(None,
                                      mirroring_robot_states=mirroring_robot_state,
                                      current_time=world_state.t)
            with lock:
                # writting the world_state of the mirroring robot
                # for display in the run_world process. Seems like 2 pyglet
                # renders can not run in 2 processes. Yes. 2 world must run in 2 processes,
                # but 2 renderers must not run in 2 processes. How convenient.
                data["world_state2"]=pickle.dumps(world_state2)
            
        else:
            time.sleep(0.001)
            



def _run_world(rendering):

    if rendering:
        from roboball2d.rendering import PygletRenderer
        from roboball2d.rendering import RenderingConfig

    # preparing the robot and renderer
    robot_config = DefaultRobotConfig()
    ball_configs = []
    visible_area_width = 6.0
    visual_height = 0.05
    world = B2World(robot_config,
                     ball_configs,
                     visible_area_width)
    if rendering:
        renderer_config = RenderingConfig(visible_area_width,
                                          visual_height)
        # for this robot
        renderer = PygletRenderer(renderer_config,
                                  robot_config,
                                  ball_configs)
        # for the mirroring robot
        renderer2 = PygletRenderer(renderer_config,
                                   robot_config,
                                   ball_configs)
        
    robot_init = DefaultRobotState(robot_config)

    
    # for sharing data with the parallel_world
    manager = multiprocessing.Manager()
    data = manager.dict()
    data["new_data"]=False
    data["running"]=True
    data["world_state"]=None
    data["world_state2"]=None
    lock = manager.Lock()

    # starting the process that will run the mirroring robot
    parallel_world = multiprocessing.Process(target=_parallel_world, args=(data,lock,))
    parallel_world.start()
    

    increment = 0.01
    torque_root = 0
    
    world.reset(robot_init)

    for iteration in range(400):

        # applying sin and cos torques
        torque_root += increment
        torques = [ math.cos(torque_root),
                    math.sin(torque_root),
                    math.cos(torque_root) ]

        # applying torques to the robot
        world_state = world.step(torques,relative_torques=True)

        # sending the robot world_state to the mirroring robot
        with lock:
            data["new_data"]=True
            data["world_state"]=pickle.dumps(world_state)

        # rendering this robot
        if rendering:
            renderer.render(world_state,time_step=1.0/60.0)

        # rendering the mirroring robot
        if rendering:
            with lock:
                ws2  = data["world_state2"]
                if ws2:
                    world_state2 = pickle.loads(data["world_state2"])
                    if(world_state2 is not None):
                        renderer2.render(world_state2,time_step=1.0/60.0)

    # stopping the mirroring robot
    with lock:
        data["new_data"]=True
        data["running"]=False
    parallel_world.join()


def run(rendering=True):

    """
    Runs the mirroring demo, in which a robot moves according to random
    torques input, while the other robot, running in another process, 
    mirrors it. You may run roboball2d_mirror_demo after install to
    see it in action.

    Parameters
    ----------

    rendering : 
        renders the environment if True
    
    """

    
    _run_world(rendering)
    


