from __future__ import print_function
import string

import time
from sr.robot import *

import os
import timeit

#global variables
a_th = 1.5
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

marker_found = [] 
"""list with all the code of the founded marker"""


marker_release = set()
"""set of all the marker release near the firt box"""

total_markers = set()

#####################################################################################

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

######################################################################################

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

#########################################################################################

def find_token():
    """
    Function to find the closest token
    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the token (-1 if no token is detected)
   
"""
        
    dist = 100
    for token in R.see():
        if token.dist < dist:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1
    else:
        return dist, rot_y, token
    
############################################################################################### 

def find_first_token():
    """
    Function to find the closest token
    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the token (-1 if no token is detected)
   
"""
        
    dist = 100
    for token in R.see():
        if token.dist < dist and token.dist > d_th:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1
    else:
        return dist, rot_y, token
    
############################################################################################### 
  
def drive_to_token(dist, rot_y, d_thr):
    """
    Function that drive the robot to the object
    Input:
    -> The distance from the marker  
    -> the rotaton of robot respect to marker
    -> the object token
    Output:    
    -> return 1 when is near the object
    
    """   
    
    if dist < d_th:
        print("Found it!")    
        return 1          
    elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
        print("Ah, here we are!.")
        drive(100, 0.1)
    #Control the rotation of the robot respect to marker
    elif rot_y < -a_th:  
        print("Left a bit...")
        turn(-2, 0.1)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.1)
        
#################################################################################################################

def drive_to_first_token(dist, rot_y, d_thr):   
    #In this function the only change resoect 

    
    if dist < d_thr:
        print("Found it!")    
        return 1          
    elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
        print("Ah, here we are!.")
        drive(80, 0.1)
    #Control the rotation of the robot respect to marker
    elif rot_y < -a_th:  
        print("Left a bit...")
        turn(-2, 0.1)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.1)
                            
######################################################################################################################
           
def main():
    """The main function has to find the first marker, and then carry to him all the marker presents in arena"""
    """ Consider out of while the case of first token found"""  

   
    
    # turning the robot for searching all the token in the arena
    for i in range(13):
        turn(20, 0.5)
        marker = R.see()
        for m in marker:
            total_markers.add(m.info.code)
        if i == 14:
            break
    
    print ("all the markers in the arena are:")
    print(total_markers)
    # Call the user the possibility of chose one box as reference 
    reference_token = int(input("Chose the reference box: "))
    

    grab = False
    while 1: 
        if(len(total_markers) == 0):
            print("work done")

        else:
            #Now i look for the other marker
            if find_token() == -1: #control that the robot can see the object
                #print("OUTSIDE IF")
                print("I can't see any token!!")
                turn(-20, 0.5)           
            else:
                dist, rot_y, token = find_token() # we look for the nearest marker  
                print("release set")
                print(marker_release)
                print("found set")
                print(marker_found)  
                print("total markers")
                print(total_markers)       
                ################################################################
                ################################################################
                #Part related to the exam
                # I have to find forst the reference token and put in in the release list
                # I checked if i have found the first token
                if marker_release == 0:
                    # In this case I have to find the reference token, and I want to drive to him
                    if token.info.code == reference_token:
                        print("I have found the reference token")
                        if drive_to_token(dist, rot_y, d_th) == 1:
                            marker_found.append(token.info.code)
                            grab = R.grab()
                            R.release()
                            marker_release.add(token.info.code)
                            total_markers.pop()
                            grab = False
                            drive(-20, 1)      
                    else:
                        # Case when the robot can't see the reference token, so I have to find it
                        turn(-20, 0.5)     
                
                ###########################################################################################
                #if the marker is release jet and not grab, entre here if the token is in the correct area
                
                elif token.info.code in marker_release and not(grab):
                    #print("FIRST IF")
                    print("I have already pose this token, need to find an other token")
                    turn(-20, 0.5) #turn because I have founded that marker jet
                
                ############################################################################################
                #if the marker is in the hand of the robot (grab == True)
                
                elif grab: 
                #I take him near the first marker                               
                    #rint("SECOND ELIF")
                    
                    if find_first_token() == -1: #in this case I turn until the robot can't see any token
                        #print("SECOND ELIF")
                        print("I can't see any token!!")
                        turn(-20, 0.5) 
                    else:
                        dist, rot_y, token = find_first_token() 
                        # Check all the markers the robot can see
                        print(token.info.code)
                        
                        if token.info.code in marker_release: 
                            #print("SECOND IF -> if")                        
                            print(token.info.code)
                            if drive_to_first_token(dist, rot_y, 0.5) == 1:
                                print("arrived to first token")
                                print("release the marker amd add to release set")
                                R.release()
                                
                                total_markers.pop() #remove one casua element in this set
                                marker_release.add(marker_found[-1]) #add the last element of the marker_found setin marker_release set
                                grab = False #set the grab value to False, now the robot doesn't have any token in his arm
                                print(grab)
                                drive(-20, 1)
                        else:
                            turn(-20, 0.5)
                                            
                #################################################################################################
                #control if I never release before this object and if the hand of robot are free
                
                elif token.info.code not in marker_release and not(grab) :
                    #print("THIRD ELIF")
                    #print(token.info.code)
                    
                    if len(marker_release) == 0:
                        #print("THIRD IF -> if")
                    #case when I haven't find any token
                        print("drive to the first nearest token")
                        if drive_to_token(dist, rot_y, d_th) ==  1:                            
                            marker_found.append(token.info.code) #put the code of the marker inside the list of founded marker                    
                            grab = R.grab() #set ture the grab value
                            R.release()
                            total_markers.pop() #remove one element in the total_mark set
                            print("add the marker in the marker_Release set")                            
                            marker_release.add(token.info.code) #add the marker in the marker_rrelease se                          
                            grab = False  #set to false the grab value, because I dont have any token in hand
                            
                            drive(-20, 1) #drive back for avoid to hit the marker                            
                        
                    else:
                        #print("THIRD IF ->else")
                        if drive_to_token(dist, rot_y, d_th) == 1:
                            marker_found.append(token.info.code) #Put the marker code inside the list of founded marker                   
                            grab = R.grab() #set to true the grab value

    
                         

main()


