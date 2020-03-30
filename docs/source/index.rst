.. roboball2d documentation master file, created by
   sphinx-quickstart on Thu Mar 26 14:17:22 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Roboball2d
==========

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



What this is
------------

Roboball2d is a lightweight python API to simulated 3 dofs torque controlled robot(s) and ball(s),
along with a renderer.
It is based on Box2d and pyglet. It can be used for anything you want,
but was created with reinforcement learning in mind.

.. figure::  ../images/roboball2d.png
   :align:   center
	     
		          roboball2d


Installation
------------

``pip install roboball2d``

to check things work, you may start one of the demo by simply typing
in a terminal:

``roboball2d_demo``

``roboball2d_balls_demo``

``roboball2d_mirror_demo``

``roboball2d_rendering_demo``

How it works
------------

Here the source code of roboball2d_demo :

.. literalinclude:: ../../roboball2d/demos/simple.py
   :language: python


Authors and maintainers
-----------------------

Nicolas Guetler and Vincent Berenz

Copyrights
----------

2020, Max Planck Gesellschaft
