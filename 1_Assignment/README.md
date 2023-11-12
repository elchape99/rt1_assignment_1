# Assigment 1 Research Track 1  

## Andrea Chiappe, matricola 4673275

In this assigment I have to use the robot simulator provided by professor.
In the roobt simulator are present a robot, and some token. In our case we have 6 token. 

The goal of this assignment is to write a python node that controls the robot to collect all the golden boxes together.
Here I will put the pseudocode of my controller

for run the code: 
python3 run.py assignment.py 


# Pseudocode  	 				
## Import necessary modules
from __future__ import print_function
import time
from sr.robot import *

## Global variables
- `a_th`: Threshold for controlling orientation
- `d_th`: Threshold for controlling linear distance
- `R`: Robot instance
- `marker_found`: List to store codes of found markers
- `marker_release`: Set to store codes of released markers near the first box
- `total_markers`: Set to keep track of all markers in the environment
- `last_detection_time`: Variable to store the timestamp of the last token detection

### Functions

#### `drive(speed, seconds)`
- Set power of left and right motors to `speed`
- Wait for `seconds`
- Set power of left and right motors to 0

#### `turn(speed, seconds)`
- Set power of left motor to `speed`
- Set power of right motor to `-speed`
- Wait for `seconds`
- Set power of left and right motors to 0

#### `find_token()`
- Initialize distance to a large value
- For each token in the robot's field of view:
  - If token's distance is less than current distance:
    - Update distance and rotation with token's distance and rotation
- If no token is found:
  - Return -1
- Else:
  - Update `last_detection_time` with current timestamp
  - Return distance, rotation, and the detected token

#### `find_first_token()`
- Initialize distance to a large value
- For each token in the robot's field of view:
  - If token's distance is less than current distance and greater than `d_th`:
    - Update distance and rotation with token's distance and rotation
- If no suitable token is found:
  - Return -1
- Else:
  - Update `last_detection_time` with current timestamp
  - Return distance, rotation, and the detected token

#### `drive_to_token(dist, rot_y, d_thr)`
- If distance to the token is less than `d_th`:
  - Return 1
- Else if robot is well aligned with the token:
  - Call `drive` function with forward speed
- Else if rotation is less than `-a_th`:
  - Call `turn` function with left turn speed
- Else if rotation is greater than `a_th`:
  - Call `turn` function with right turn speed

#### `drive_to_first_token(dist, rot_y, d_thr)`
- (Similar to `drive_to_token` function with some modifications)

## Main function
function main():
   
    # Initial rotation to gather information about markers
    For each iteration in the range from 0 to 12:
        Turn the robot with a speed of 20 for 0.5 seconds  # Rotate the robot to scan the surroundings
        Use the robot's vision to detect markers  # Capture the markers in the field of view
        For each detected marker:
            Add the marker's code to the 'total_markers' set  # Record the code of each detected marker

    If the current iteration is the last one (i.e., iteration 12):
        Exit the loop  # Break out of the loop as the required iterations are completed
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


## Execute the main function if the script is the main module
if __name__ == "__main__":
  main()
