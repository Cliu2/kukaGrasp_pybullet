import socket
import sys
import time
import pickle
sys.path.append("../..")

from robot_controller_fake import *
class Command_client:

    def __init__(self):
        self.address = None
        self.arm_server = None
        self.robot_ctl = RobotController("123.123.123.123", 6)

        self.cmd_list = {
            "init_robot" : self.init_robot,
            "goPos" : self.robot_ctl.goPos
        }

    def init_robot(self, ip='127.0.0.1', port=2005):
        # setup TCP connection to the robotarm server
        self.address = (ip, port)
        self.arm_server = TcpInterface(address)
        self.arm_server.connect()
        
        # Config the robot

    def call_func(self, cmd_str):
    	cmd_json = pickle.loads(cmd_str)
    	print(cmd_json)

    	# or rasing 'func' no in cmd_json
    	if cmd_json['func'] not in self.cmd_list:
    		raise NotImplementedError(cmd_str)
    	self.cmd_list[cmd_json['func']](*cmd_json['args'])

if __name__ == "__main__":

    cmd_client = Command_client()

    tcp_tx_msg = {
    	'func' : None,
    	'args' : None
    }

    tcp_rx_msg = {
    	'return' : None,
    	'error' : None
    }

    while True:
        # get the cmd
        input_str = raw_input("-->").split(" ")
        print(input_str)
        tcp_tx_msg['func'] = input_str[0]
        tcp_tx_msg['args'] = input_str[1:]
        cmd_str = pickle.dumps(tcp_tx_msg)

        try:
            cmd_client.call_func(cmd_str)
        except Exception as e:
            print(type(e), e)