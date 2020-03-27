import unittest


class IMPORT_TESTCASE(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_import_pd_controller(self):

        failed = True
        try :
            from roboball2d.robot import PDController
            failed = False
        except :
            pass

        self.assertFalse(failed)
    
    def test_import_ball_config(self):

        failed = True
        try :
            from roboball2d.ball import BallConfig
            failed = False
        except :
            pass

        self.assertFalse(failed)
    
    def test_import_b2robot(self):

        failed = True
        try :
            from roboball2d.physics import B2Robot
            failed = False
        except :
            pass

        self.assertFalse(failed)
    
    def test_import_robot_state(self):

        failed = True
        try :
            from roboball2d.robot import DefaultRobotState
            failed = False
        except :
            pass

        self.assertFalse(failed)
    
    def test_import_world_state(self):

        failed = True
        try :
            from roboball2d.physics import WorldState
            failed = False
        except :
            pass

        self.assertFalse(failed)


        
