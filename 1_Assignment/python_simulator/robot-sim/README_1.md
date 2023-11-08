# Assigment 1 Research Track 1  

## Andrea Chiappe, matricola 4673275

In this assigment I have to use the robot simulator provided by professor.
In the roobt simulator are present a robot, and some token. In our case we have 6 token. 

The goal of this assignment is to write a python node that controls the robot to out all the golden boxes together.
Here I will put the pseudocode of my controller

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
 		
 	if grab == True :
 		 
				

