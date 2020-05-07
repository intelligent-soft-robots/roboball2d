import unittest

class DEMOS_TESTCASE(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _run_demo(self,run):

        success = True

        try :
            run(rendering=False)
        except Exception as e:
            print()
            print(e)
            print()
            success = False

        self.assertTrue(success)
    
    def test_simple(self):
        
        from roboball2d.demos.simple import run
        self._run_demo(run)
        
    def test_rendering_callback(self):

        from roboball2d.demos.rendering_callback import run
        self._run_demo(run)

    def test_mirroring(self):

        from roboball2d.demos.mirroring import run
        self._run_demo(run)

    def test_balls(self):

        from roboball2d.demos.balls import run
        self._run_demo(run)

    def test_mirror_balls(self):

        from roboball2d.demos.mirror_balls import run
        self._run_demo(run)

    
