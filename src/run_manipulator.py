import cv2
import numpy as np
import paramiko
import time

cap = cv2.VideoCapture(0)

red_thresh = 220 
green_thresh = 150 
blue_thresh = 220 

escape = 27
ON = 1
OFF = 0

def move_hand(angle, s_state):
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Auto login with host_name and password
        ssh.connect('10.232.169.31', port=22, username='ubuntu', password='raspberry')

        stdin, stdout, stderr = ssh.exec_command( "cd /run/shm; echo %s > angles"%(angle) )
        stdin, stdout, stderr = ssh.exec_command( "cd /run/shm; echo %s > ev_on_off"%(state) )
        time.sleep(3)


if __name__ == '__main__':
    manipulator_red_states = [ ('0,0,0,0,0', OFF), 
                               ('0,90,70,-50,0', OFF),
                               ('0,90,70,-50,0', OFF),
                               ('0,90,70,-50,0', ON),
                               ('0,70,40,-20,0', ON),
                               ('90,70,40,-20,0', ON),
                               ('90,70,40,-20,0', ON),
                               ('90,70,40,-20,0', OFF),
                               ('0,70,40,-20,0', OFF),
                               ('0,0,0,0,0', OFF) ]
    while(1):
        res, frame = cap.read()
        cv2.imshow("FRAME", frame)

        height, width, depth = frame.shape

        mid_h, mid_w = int(height/2), int(width/2)
        blue, green, red = frame[mid_h, mid_w]

        if red >= red_thresh: 
            print "RED"
            for angles, state in manipulator_red_states:
                move_hand(angles, state)
        elif green >= green_thresh: 
            print "GREEN"
        elif blue >= blue_thresh: 
            print "BLUE"
        else:
            continue

        key = cv2.waitKey(5)
        if key == escape:
        ¦   break

    cv2.destroyAllWindows()
    cap.release()

