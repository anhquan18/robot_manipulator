import time
import numpy as np
import paramiko

cap = cv2.VideoCapture(0)

escape = 27

def move_hand(angle, s_state):
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Auto login with host_name and password
        ssh.connect('10.232.169.31', port=22, username='ubuntu', password='raspberry')

        stdin, stdout, stderr = ssh.exec_command( "cd /run/shm; echo %s > angles"%(angle) )
        stdin, stdout, stderr = ssh.exec_command( "cd /run/shm; echo %s > ev_on_off"%(state) )

manipulator_states_list = ['0, 90, 45, 0, 0', 1]

if __name__ == '__main__':
    while(1):
        res, frame = cap.read()

        height, width, depth = frame.shape

        mid_h, mid_w = int(height/2), int(width/2)
        blue, green, red = frame[mid_h, mid_w]

            for i in range(1):
                angles, state = manipulator_states_list
                print angles
                print state
                move_hand(angles, state)
                time.sleep(5)
