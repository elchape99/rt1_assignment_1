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
	 					
 		 
				

