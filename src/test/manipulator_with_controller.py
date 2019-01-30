import pygame
import paramiko
import time

ON = 1
OFF = 0
FPS = 20

axis = {}
button = {}
hat = {}

pygame.init()
pygame.joystick.init()

controller = pygame.joystick.Joystick(0)
controller.init()

for i in range(controller.get_numaxes()):
        axis[i] = 0.0
# Buttons are initialized to False
for i in range(controller.get_numbuttons()):
        button[i] = False
# Hats are initialized to 0
for i in range(controller.get_numhats()):
        hat[i] = (0, 0)

# Labels for DS4 controller axes
AXIS_LEFT_STICK_X = 0
AXIS_LEFT_STICK_Y = 1
AXIS_RIGHT_STICK_X = 3
AXIS_RIGHT_STICK_Y = 4
AXIS_L2 = 2
AXIS_R2 = 5

# Labels for DS4 controller buttons
# Note that there are 14 buttons (0 to 13 for pygame, 1 to 14 for Windows setup)
BUTTON_CROSS = 0
BUTTON_CIRCLE = 1
BUTTON_TRIANGLE = 2
BUTTON_SQUARE = 3

BUTTON_L1 = 4
BUTTON_R1 = 5
BUTTON_L2 = 6
BUTTON_R2 = 7

BUTTON_SHARE = 8
BUTTON_OPTIONS = 9
BUTTON_PS = 10

BUTTON_LEFT_STICK = 11
BUTTON_RIGHT_STICK = 12

#BUTTON_PAD will be the mouse click and track_pad

clock = pygame.time.Clock()

# Labels for DS4 controller hats (Only one hat control)
#HAT = 0

# Hat_value
HAT_RIGHT = (1,0)
HAT_LEFT = (-1,0)
HAT_UP = (0,1)
HAT_DOWN = (0,-1)


def move_hand(angles, c_state):
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Auto login with host_name and password
        ssh.connect('10.232.169.229', port=22, username='ubuntu', password='raspberry')

        stdin, stdout, stderr = ssh.exec_command( "cd /run/shm; echo %s,%s,%s,%s,%s > angles"%(str(angles[0]), str(angles[1]), str(angles[2]), str(angles[3]), str(angles[4])))
        stdin, stdout, stderr = ssh.exec_command( "cd /run/shm; echo %s > ev_on_off"%(c_state) )
        ssh.close()


def change_angle_with_event(a_list):
    if axis[AXIS_LEFT_STICK_Y] > 0.1:
        a_list[0] -= 5
    if axis[AXIS_LEFT_STICK_Y] < -0.1:
        a_list[0] += 5
    if axis[AXIS_RIGHT_STICK_Y] > 0.1:
        a_list[1] -= 5
    if axis[AXIS_RIGHT_STICK_Y] < -0.1:
        a_list[1] += 5
    if hat == HAT_UP:
        a_list[2] += 5
    if hat == HAT_DOWN:
        a_list[2] -= 5
    if hat == HAT_RIGHT:
        a_list[3] += 5
    if hat == HAT_LEFT:
        a_list[3] -= 5
    if button[BUTTON_L1]:
        a_list[4] -= 5
    if button[BUTTON_R1]:
        a_list[4] += 5
    if button[BUTTON_TRIANGLE]:
        for i in range(len(a_list)):
            a_list[i] = 0


if __name__ == '__main__':
    angles_list = [0, 0, 0, 0, 0]
    cylinder_state = OFF

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                axis[event.axis] = round(event.value,3)
            elif event.type == pygame.JOYBUTTONDOWN:
                button[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                button[event.button] = False
            elif event.type == pygame.JOYHATMOTION:
                hat = event.value
            if button[BUTTON_CIRCLE]: 
                cylinder_state = ON
            if button[BUTTON_CROSS]:
                cylinder_state = OFF
            if button[BUTTON_SQUARE]:
                move_hand(angles_list, cylinder_state)
                button[BUTTON_SQUARE] = False

        change_angle_with_event(angles_list)
        print "angles: ", angles_list, "cylinder:", cylinder_state
        clock.tick(FPS)
