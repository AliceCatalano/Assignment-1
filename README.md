# Assignment-1
first assignment solution
Python Robotics Simulator 
===========================

This is a simple, portable robot simulator modified by me from the exercise given by [CarmineD8] (https://github.com/CarmineD8/python_simulator).

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

The Arena
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names.
The robot has to drive across the whole [arena](Arena.jpg), in which the golden token reperesent an obstacle to avoid and the silver token the target to move. 

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

### Behaviour Management ###
After that the robot sees the token, based on the `marker_type`, it has to run different actions, as described in the [flowchart](flowchart.pdf). For this reason, 2 sets of functions are used.

* Actions for the silver token:
  * `find_silver token` : Function to find the closest silver token.
  * `traj_adjustment(rot_y)` : Function to adjust the orientation of the robot toward the nearest silver token, takes as argument the orientation about the Y axis in degrees.
  * `changeBool(dist, silver)` : Function to change the boolean value of the silver token.
* To this set of functions the following variables are related:
  * `a_th=2.0` : (float) Threshold for the control of the linear orientation of the silver token alignment.
  * `d_th= 0.7`: (float) Threshold for the control of the distance from the silver token.
  * `s_th=60.0` : (float) Threshold for the control of linear orientation for the silver token perception.
  * `silver=True` : (boolean) Variable for letting the robot know if it has to look for a silver or for a golden marker.

* Actions for the golden token:
  * `find_golden token` : Function to find the closest golden token.
  * `gold_manage(dist, rot_y)` : Function to manage the behaviour of the robot when a golden token  is seen in its threshold, takes as argument the distance of the closest golden token and the orientation about the Y axis in degrees.
  * `sideView()` : Function to check on the side  of the robot and choose the side without near golden token.
* To this set of functions the following variables are related:
  * `ang_th= 80.0` : (float) Threshold for the control of the linear orientation of the golden token alignment.
  * `dist_th=0.8`: (float) Threshold for the control of the distance from the golden token.


