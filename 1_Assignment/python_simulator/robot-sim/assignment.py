
from __future__ import print_function
import string

import time
from sr.robot import *

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

  
def drive_to_token(dist, rot_y):
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
        drive(80, 0.1)
    #Control the rotation of the robot respect to marker
    elif rot_y < -a_th:  
        print("Left a bit...")
        turn(-2, 0.1)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.1)
        
#################################################################################################################

def drive_to_first_token(dist, rot_y):   

    
    if dist < 0.5:
        print("Found it!")    
        return 1          
    elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
        print("Ah, here we are!.")
        drive(30, 0.1)
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
    grab = False
    var  = 1 # the variable for first while lopp useful for find the first marker
    while 1:   
        
        #find the nearest marker, it will be the first markers and will carry all token near him
        while(var):
            
            if find_token() == -1: #in this case I turn until the robot can't see any token
                print("I can't see any token!!")
                turn(20, 0.5) 
            else:
                print("drive to the first nearest token")
                dist_1, rot_y_1, token = find_token() 
                if drive_to_token(dist_1, rot_y_1) ==  1:
                    print("add the token in the merker_found list")
                    
                    marker_found.append(token.info.code) #put the code of the marker inside the list of founded marker                    
                    grab = R.grab()
                    print("found marker: ")
                    print(marker_found)
                                    
                    R.release()
                    print("add the marker in the marker_Release set")
                    marker_release.add(token.info.code) #add the marker in the 
                    print("now the release marker are: ")
                    print(marker_release)
                    
                    grab = False  #set to false the grab value, because I dont have any token in hand
                    
                    drive(-20, 1) #drive back for avoid to hit the marker 
                    turn(-40, 0.5) #turn on right because I want to carry now the marker on the right 
                
                    var = 0     # close the while loop 
                
        #Now i look for the other marker
        if find_token() == -1: #control that the robot can see the object
            print("OUTSIDE IF")
            print("I can't see any token!!")
            turn(-20, 0.5)           
        else:
            dist, rot_y, token = find_token() # we look for the nearest marker
            
            print("outside the for cycle")
            print("near token")
            print(token.info.code)  
            print("release set")
            print(marker_release)
            print("found set")
            print(marker_found)                    
        
            ###########################################################################################
            #if the marker is release jet and not grab, entre here if the token is in the correct area
            
            if token.info.code in marker_release and not(grab):
                print("FIRST IF")
                print("I have already pose this token, need to find an other token")
                turn(-20, 0.5) #turn because I have founded that marker jet
            
            ############################################################################################
            #if the marker is in the hand of the robot (grab == True)
            
            elif grab: 
            #I take him near the first marker                               
                print("SECOND ELIF")
                
                if find_first_token() == -1: #in this case I turn until the robot can't see any token
                    print("SECOND ELIF")
                    print("I can't see any token!!")
                    turn(-20, 0.5) 
                else:
                    dist, rot_y, token = find_first_token() 
                    # Check all the markers the robot can see
                    print(token.info.code)
                    
                    if token.info.code in marker_release: 
                        print("SECOND IF -> if")                        
                        print(token.info.code)
                        if drive_to_first_token(dist, rot_y) == 1:
                            print("arrived to first token")
                            print("release the marker amd add to release set")
                            R.release()
                            #add the last element of the marker_found setin marker_release set
                            marker_release.add(marker_found[-1]) 
                            grab = False #set the grab value to False, now the robot doesn't have any token in his arm
                            print(grab)
                            drive(-20, 1)
                    else:
                        turn(-20, 0.5)
                                           
            #################################################################################################
            #control if I never release before this object and if the hand of robot are free
            
            elif token.info.code not in marker_release and not(grab) :
                print("THIRD ELIF")
                print(token.info.code)
                if drive_to_token(dist, rot_y) == 1:
                    marker_found.append(token.info.code) #Put the marker code inside the list of founded marker                   
                    print("found another marker: ")
                    print(marker_found)  
                    print(marker_release)
                    grab = R.grab() #set to true the grab value
                        
                        
                        
                      
              
                         
      

main()







