import unittest


class IMPORT_TESTCASE(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_import_world_state(self):

        failed = True
        try :
            from roboball2d.physics.world_state import WorldState
            failed = False
        except :
            pass

        self.assertFalse(failed)
