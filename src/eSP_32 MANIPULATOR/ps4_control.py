# ps4 control
import pprint
import pygame
import time
import socket
import serial
sock = socket.socket()
host = "192.168.98.123"  # ESP32 IP in local network
port = 6677  # ESP32 Server Port
sock.connect((host, port))
step1, step2, step3 = 0, 0, 0
drishti_joint, Svnit_joint, gripper_joint = 0.0, 0.0, 0.0
data = "#"


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        global step1
        global step2
        global drishti_joint
        global Svnit_joint
        global gripper_joint
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = 0
        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            time.sleep(0.01)
            for event in pygame.event.get():
                # if event.type == pygame.JOYAXISMOTION:
                #     self.axis_data[event.axis] = round(event.value, 2)
                #     if 5 in self.axis_data:
                #         gripper_joint = self.axis_data[5]
                #         gripper_joint = 3000 + 100 * \
                #             (gripper_joint < 0)+abs(gripper_joint)*99
                #         gripper_joint = "#" + str(gripper_joint)
                #         sock.sendall(gripper_joint.encode('utf-8'))
                #         if(self.axis_data[5] != 0):
                #             sock.sendall(gripper_joint.encode('utf-8'))
                if event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = 1
                    if(self.button_data[0] == 1):  # .......motor2 linear colapse
                        print(self.button_data[0])
                        sock.sendall(b"#40")
                    if(self.button_data[1] == 1):  # .......motor3 linear colapse
                        print(self.button_data[1])
                        sock.sendall(b"#50")
                    if(self.button_data[2] == 1):  # .......motor2 linear expand
                        print(self.button_data[2])
                        sock.sendall(b"#42")
                    if(self.button_data[3] == 1):  # .......motor3 linear expand
                        print(self.button_data[3])
                        sock.sendall(b"#52")
                    if(self.button_data[4] == 1):  # .......motor1 stepper top anti
                        print(self.button_data[4])
                        sock.sendall(b"#30")
                    if(self.button_data[5] == 1):  # .......motor1 stepper top clock
                        print(self.button_data[5])
                        sock.sendall(b"#32")
                    if(self.button_data[8] == 1):  # share->motor speed dec
                        print(self.button_data[8])
                        sock.sendall(b"#90")
                    if(self.button_data[9] == 1):  # options->motor speed inc
                        print(self.button_data[9])
                        sock.sendall(b"#92")
                    if(self.button_data[10] == 1):  # ........STOP
                        print(self.button_data[10])
                        sock.sendall(b"#91")
                if event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = -1
                    if self.button_data[0] == -1:
                        print(self.button_data[0])
                        sock.sendall(b"#41")
                    if self.button_data[1] == -1:
                        print(self.button_data[1])
                        sock.sendall(b"#51")
                    if self.button_data[2] == -1:
                        print(self.button_data[2])
                        sock.sendall(b"#41")
                    if self.button_data[3] == -1:
                        print(self.button_data[3])
                        sock.sendall(b"#51")
                    if self.button_data[4] == -1:
                        print(self.button_data[4])
                        sock.sendall(b"#31")
                    if self.button_data[5] == -1:
                        print(self.button_data[5])
                        sock.sendall(b"#31")

                    self.button_data[0] = 0
                    self.button_data[2] = 0
                    self.button_data[1] = 0
                    self.button_data[3] = 0
                    self.button_data[4] = 0
                    self.button_data[5] = 0
                    # print(self.button_data[1])
                    # print(self.button_data[2])
                    # print(self.button_data[3])
                    # print(self.button_data[4])
                   # print(self.button_data[5])
                if event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value
                    step1 = self.hat_data[0][0]
                    if(step1 > 0):
                        print(self.hat_data[0][0])
                        sock.sendall(b"#72")
                    elif(step1 < 0):
                        print(self.hat_data[0][0])
                        sock.sendall(b"#70")
                    step2 = self.hat_data[0][1]
                    if(step2 > 0):
                        print(self.hat_data[0][1])
                        sock.sendall(b"#82")
                    elif(step2 < 0):
                        print(self.hat_data[0][1])
                        sock.sendall(b"#80")
                # pprint.pprint(self.button_data)
                # pprint.pprint(self.axis_data)
                # pprint.pprint(self.hat_data)
                # print("3="+str(step3),"2="+str(step2),step1)
                # print("drishti_joint="+str(drishti_joint)+"Svnit_joint="+str(Svnit_joint)+"gripper_joint="+str(gripper_joint))


ps4 = PS4Controller()
ps4.init()
ps4.listen()