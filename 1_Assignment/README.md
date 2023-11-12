# Assigment 1 Research Track 1  

## Andrea Chiappe, matricola 4673275

In this assigment I have to use the robot simulator provided by professor.
In the roobt simulator are present a robot, and some token. In our case we have 6 token. 

The goal of this assignment is to write a python node that controls the robot to out all the golden boxes together.
Here I will put the pseudocode of my controller

for run the code: 
python3 run.py assignment.py 
## Pseudocode  

I need some set and list for consider all teh case 

	marker_found() = [] 	# list of founded mark
	marker_release = set() 	# set of all the marker release
	total_markers = set() 	# set of all total marker present in arena 

	 while(var)
		make the robot rotate 
		find all the token present in arena using R.see() functions
		put all the markers found in found_markers()
		
		after a turn put var= 0 and exit while loop

	 while 1 infinite loop

		if find_token() == -1: # this function find all near token and return -1 if can't find nothing
			make the robot turning
		else:
			dist, rot_Y, token = find_token()
			
	 	# now analize all the possible case we could have
	 	
	 	if token.info.code in marker_release and not in the hand of robot (grab == False):
	 		Robot has already pose in teh correct position that marker
	 		turn(20, 0.5)
	 		
	 	elif grab == True: #the robot has the token in his hand, need to drive to the area near first marker
	 	
	 		if find_token() == -1: 				# obot can't see any token
	 			turn (20, 0.5) 
	 			
	 		else:						 # case where the robot see the token
	 			dist, rot, token = find_token()	
	 			
	 			if token.info.code in marker_release:  	# case when the token the robot can see is in the marker_release set, so I wantoto go there
	 				
	 				if drive_to_token == 1: 	#drive_to_token return 1 when it is near the token was driving to
	 					R.release() 		#release the token 
	 					marker_release.add(marker_found[-1]) #add at the marker_Release set the last value of marker found
	 					total_markers.pop()	#remove a casual element to total_markers, use this set only forstopconditions
	 					grab = False		#robot doesn't have the token in hands more
	 					
	 					make distance from token, in this way the robot desn't touche the token when it will start 
	 			
	 			else:					#case when the token.info.code isn't in the marker_release array
	 				turn(20 0.5)
	 				
	 	elif token.info.code not in marker__release and not(grab)
	 		
	 		if len(markere_release) == 0 			#starting case, robot haven't find any token before, so it will go to take the nearest tolen 
	 			if drive_to_token == 1
	 				marker_found.append(token.info.code)
	 				maker_release.add(token.info.code)
	 				grab = False
	 				total_markers.pop()
	 			
	 		else:						# case when the robot is loking for find a new token 
	 			if drive_to_token == 1
	 				marker_found.aend(token.info.code)
	 				grab = R.grab() 		#set grab to true 
	 				
	 				
	 				
	 				
# Import necessary modules
from __future__ import print_function
import time
from sr.robot import *

# Global variables
- `a_th`: Threshold for controlling orientation
- `d_th`: Threshold for controlling linear distance
- `R`: Robot instance
- `marker_found`: List to store codes of found markers
- `marker_release`: Set to store codes of released markers near the first box
- `total_markers`: Set to keep track of all markers in the environment
- `last_detection_time`: Variable to store the timestamp of the last token detection

## Functions

### `drive(speed, seconds)`
- Set power of left and right motors to `speed`
- Wait for `seconds`
- Set power of left and right motors to 0

### `turn(speed, seconds)`
- Set power of left motor to `speed`
- Set power of right motor to `-speed`
- Wait for `seconds`
- Set power of left and right motors to 0

### `find_token()`
- Initialize distance to a large value
- For each token in the robot's field of view:
  - If token's distance is less than current distance:
    - Update distance and rotation with token's distance and rotation
- If no token is found:
  - Return -1
- Else:
  - Update `last_detection_time` with current timestamp
  - Return distance, rotation, and the detected token

### `find_first_token()`
- Initialize distance to a large value
- For each token in the robot's field of view:
  - If token's distance is less than current distance and greater than `d_th`:
    - Update distance and rotation with token's distance and rotation
- If no suitable token is found:
  - Return -1
- Else:
  - Update `last_detection_time` with current timestamp
  - Return distance, rotation, and the detected token

### `drive_to_token(dist, rot_y, d_thr)`
- If distance to the token is less than `d_th`:
  - Return 1
- Else if robot is well aligned with the token:
  - Call `drive` function with forward speed
- Else if rotation is less than `-a_th`:
  - Call `turn` function with left turn speed
- Else if rotation is greater than `a_th`:
  - Call `turn` function with right turn speed

### `drive_to_first_token(dist, rot_y, d_thr)`
- (Similar to `drive_to_token` function with some modifications)

# Main function
function main():
    Set 'var' to 1
    Set 'count' to 0

    # Initial rotation to gather information about markers
    While 'var':
        Call turn function with a constant speed for a short duration
        For each detected marker:
            Add marker code to the 'total_markers' set
            Increment 'count'
            If 'count' reaches 15:
                Set 'var' to 0
        Set 'grab' to False
    
    While True:
        If 'total_markers' set is empty:
            Print "Work done"
            Exit the loop
        Else:
            # Now, look for other markers
            If no token is detected:
                Print "I can't see any token!!"
                Call turn function with a negative speed
            Else:
                Obtain distance, rotation, and token information

                If token is already released and not grabbed:
                    Print "Already posed, find another token"
                    Call turn function with a negative speed

                If token is grabbed:
                    Call find_first_token function to find the first token
                    If no suitable token is detected:
                        Print "Can't see any token!!"
                        Call turn function with a negative speed
                    Else:
                        Obtain distance, rotation, and token information
                        Print detected token code
                        If token is in the marker release set:
                            Call drive_to_first_token function to drive to the first token
                            If arrived at the first token:
                                Print "Arrived at first token"
                                Print "Release the marker and add to release set"
                                Call R.release() to release the marker
                                Remove one element from 'total_markers' set
                                Add last element of 'marker_found' list to 'marker_release' set
                                Set 'grab' to False
                                Call drive function with reverse speed

                        Else:
                            Call turn function with a negative speed

                If token is not in the marker release set and not grabbed:
                    If marker release set is empty:
                        Print "Drive to the first nearest token"
                        Call drive_to_token function to drive to the first nearest token
                        If arrived at the token:
                            Add token code to 'marker_found' list
                            Set 'grab' to True
                            Call R.release() to release the marker
                            Remove one element from 'total_markers' set
                            Print "Add marker to marker_release set"
                            Add token code to 'marker_release' set
                            Set 'grab' to False
                            Call drive function with reverse speed

                    Else:
                        Call drive_to_token function to drive to the token
                        If arrived at the token:
                            Add token code to 'marker_found' list
                            Set 'grab' to True

                        Update last_detection_time with current timestamp


# Execute the main function if the script is the main module
if __name__ == "__main__":
  main()
