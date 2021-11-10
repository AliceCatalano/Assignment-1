from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py solutions/exercise3_solution.py

"""


a_th = 2.0
""" float: Threshold for the control of the linear orientation of the silver token alignment"""
s_th= 60.0
"""float: Threshold for the control of linear orientation for the silver token perception """
d_th = 0.7
""" float: Threshold for the control of the distance from the silver token"""
dist_th=0.8
""" float: Threshold for the control of the distance from the golden token"""
ang_th= 80.0
""" float: Threshold for the control of the linear orientation of the golden token alignment"""
silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""
R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Args:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist= 100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100: 
    	return -1, -1
    else:
   	return dist, rot_y

def gold_manage(dist, rot_y):
    """
    Function to manage the behaviour of the robot when a golden token is seen in its threshold
    
    Args:
    	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    if dist<dist_th:
        print("WARNING!")
    	
    	if -ang_th<= rot_y <= ang_th:
            sideView()
    	else:
            print("Still safe")
            drive(50, 0.25)    
    else:
        drive(50,0.25)

def traj_adjustment(rot_y): 
    """
    Function to adjust the orientation of the robot toward the nearest silver token
    
    Args:
        rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    while rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-10, 0.5)
        dist, rot_y = find_silver_token()
        
    while rot_y > a_th:
        print("Right a bit...")
        turn(+10, 0.5)
        dist, rot_y = find_silver_token()
    print("Ah, that'll do.")
    drive(50, 0.25)

def changeBool(dist, silver):
    """
    Function to change the Boolean value of the silver token
    
    Args:
        dist (float): distance of the closest golden token (-1 if no golden token is detected)
        silver (boolean): boolean value of the silver token (True when the robot has to search it, False if not)
    """
    if silver== False :
        if dist > d_th:
            silver= True
    else:
        print("cond not verified")       
    return silver 
    
def sideView():
    """
    Function to check on the side  of the robot and choose the side without near golden token
    """
    dist_right= 100
    dist_left= 100
    
    for token in R.see():    
        if token.info.marker_type is MARKER_TOKEN_GOLD:   #if the token seen is golden, check the side
            if 80<=token.rot_y<=110:
                if token.dist<=dist_right:
                    dist_right= token.dist 
                
            if -110<=token.rot_y<=-80: 
                if token.dist<=dist_left:
                    dist_left= token.dist
    
    if dist_right < dist_left:   #compare the side distances and go toward the further one
        turn(-10,0.5)
    elif dist_right > dist_left:
        turn(+10,0.5)
    
while 1:
    distg, rotg_y = find_golden_token()
    gold_manage(distg, rotg_y)
    if silver == True: # if silver is True, than we look for a silver token, otherwise for a golden one
	dist, rot_y = find_silver_token()
	if dist <= d_th and -s_th<=rot_y<=s_th: #if we are close to the token and with the right orientation, we try grab it.
            print("Found it!")
            if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
                print("Gotcha!")
	        turn(30, 2)
	        R.release()
	        turn(-30,2)
	        silver = not silver # we modify the value of the variable silver, so that in the next step we will look for the other type of token
	    else:
	        traj_adjustment(rot_y)
        else:
            print("Aww, I'm not close enough.")
            
    else:
	print ("going to silver")
	dist, rot_y = find_silver_token()
	changeBool(dist, silver)    
	silver = changeBool(dist, silver)
	
	
	
	
  
    
    
           
            
    
    
    
  
    
    
        

    
	
