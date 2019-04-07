#!/usr/bin/env python3
import socket
import pickle
import pdb
from pprint import pprint
import numpy as np

class RR_interface():

    def __init__(self, address=("192.168.2.100", 10000), debug=True, speed=3,
        accel=4, zLimit=110, home_pos=[254.2, 1.54, 437.934, -25, 0, -180]):
        self.tcp_tx_msg = {
            'func': None,
            'args': None
        }
        self.tcp_address = address

        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect(address)  # connect to the server

        self.debug = debug

        self.init_robot()
        self.setSpeed(speed)
        self.setAccel(accel)

        self.cur_pos = None
        self.getCurPos() # get the current position

        self.zLimit = zLimit
        self.home_pos = home_pos

    def _send_cmd(self, func, args=[]):
        # sending a command out
        self.tcp_tx_msg['func'] = func
        self.tcp_tx_msg['args'] = args

        cmd_str = pickle.dumps(self.tcp_tx_msg, protocol=2)
        if self.debug:
            print("Msg to send: ")
            pprint(self.tcp_tx_msg)
            print(cmd_str)
            for arg in args:
                print(type(arg), arg)
        self.client_socket.send(cmd_str)

        # get and process the return
        res = self.client_socket.recv(2048)
        res = pickle.loads(res, encoding='latin1')

        if self.debug:
            print("Msg received: ")
            pprint(res)  # show in terminal

        # raise debug msg if error occurs
        if res['error'] != None:
            # command failed
            raise UserWarning(res['error'])
        else:
            return res['return'], res['used_time']

    def close_connection(self):
        self.client_socket.close()
        return True, None

    def close_server(self):
        self.client_socket.send("close_server".encode())
        if self.debug:
            print("closing the server")
        self.client_socket.close()
        return True, None

    def init_robot(self):
        ret = self._send_cmd("init_robot")
        self.setSpeed(3)
        self.setAccel(4)
        return ret

    def getCurPos(self):
        ret, used_time = self._send_cmd("getCurPos")
        self.cur_pos = np.around(ret.reshape(-1), decimals=3)
        return self.cur_pos, used_time # usually takes 2ms

    def goPos(self, pos, error=1, move_type="move", timeout=30, handModeFlag=None):
        # restricting the height
        if pos[2] < self.zLimit:
            raise ValueError("height is too low and may break the arm!")

        return self._send_cmd("goPos", [pos, error, move_type])

    def goDeltaPos(self, deltaPos, error=1, move_type="move", timeout=30):
        # restricting the hight
        # print("=================updating the current position")
        self.getCurPos() # update the current position
        # print("=================updated the current position")
        if self.cur_pos[2]+deltaPos[2] < self.zLimit:
            raise ValueError("Reached height limit!")
        #     # print("Warning: the height is clipped, cannot be lower than the limit!")
        #     deltaPos[2] = 0
        return self._send_cmd("goDeltaPos", [deltaPos, error, move_type])

    def getCurJointAngle(self):
        return self._send_cmd("getCurJointAngle")

    def goJointAngle(self, jointAngle_deg, error=1, timeout=30):
        return self._send_cmd("goJointAngle", [jointAngle_deg, error])

    def goDeltaJointAngle(self, deltaAngle_deg, error=1, timeout=30):
        return self._send_cmd("goDeltaJointAngle", [deltaAngle_deg, error])

    def setSpeed(self, speed):
        return self._send_cmd("setSpeed", [speed])

    def setAccel(self, accel):
        return self._send_cmd("setAccel", [accel])

    def setHandMode(self, flag):
        return self._send_cmd("setHandMode", [flag])

    def waitMoveDone(self, timeout=30):
        return self._send_cmd("waitMoveDone")

    def checkTargetOK(self, pos):
        return self._send_cmd("checkTargetOK")

    def stop(self):
        return self._send_cmd("stop")

    def close_robot(self):
        return self._send_cmd("close_robot")

    def help(self):
        return self._send_cmd("help")

    def goHome(self):
        self.stop()
        return self.goPos(self.home_pos, error=1)


if __name__ == "__main__":
    rr = RR_interface()
    pdb.set_trace()
    # rr.close_connection()
