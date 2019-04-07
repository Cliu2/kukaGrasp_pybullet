import socket
import sys
import time
import pickle
sys.path.append("../")
import pdb

#from robot_controller_fake import *
from rr.tcp_interface import *
from rr.robot_controller import *

from rr.common_controller import CommonController
from rr.common_controller import MachineType
from rr.common_controller import MachineError
import pydoc

keep_server_on = True

class Command_server:

    def __init__(self):
        self.my_robot = None
        self.init_robot()
    
    def init_robot(self, ip='127.0.0.1', port=2005):
        if self.my_robot != None:
            print("Robot already initialized")
            return "Robot already initialized"
        # setup TCP connection to the robotarm server
        self.address = (ip, port)
        self.my_robot = RobotController(self.address, machineType=MachineType.SIX_AXIS_KEN)
        self.my_robot.connect()
        time.sleep(0.1)
        self.my_robot.setSpeed(3)
        self.my_robot.setAccel(4)
        self.my_robot.setHandMode('left')
        self.my_robot._sendAndRecvData("openFreqStatusPort(2005, 1000)", dataKey='ret', debug=True)
        
        self.cmd_dict = {
            "init_robot" : self.init_robot,
            "getCurPos" : self.my_robot.getCurPos,
            "goPos" : self.my_robot.goPos,
            "goDeltaPos": self.my_robot.goDeltaPos,
            "getCurJointAngle": self.my_robot.getCurJointAngle,
            "goJointAngle": self.my_robot.goJointAngle,
            "goDeltaJointAngle": self.my_robot.goDeltaJointAngle,
            "setSpeed": self.my_robot.setSpeed,
            "setAccel": self.my_robot.setAccel,
            "setHandMode": self.my_robot.setHandMode,
            "waitMoveDone": self.my_robot.waitMoveDone,
            "checkTargetOK": self.my_robot.checkTargetOK,
            #"solveIK": self.my_robot.solveIK,
            #"solveFK": self.my_robot.solveFK,
            "stop": self.my_robot.stop,
            "close_robot": self.close_robot,
            "help": self.help
        }
        
        ret = "curPos: " + str(self.my_robot.getCurPos())
        print(ret)
        # pdb.set_trace()
        return ret
   
    def help(self):
        # helper function, return the list of cmd_dict
        return [k for k in self.cmd_dict]
        
    def close_robot(self):
        self.my_robot.stop()
        self.my_robot.close()
        self.my_robot = None
        return "Robot closed"

    def call_func(self, cmd_json, tcp_rx_msg):
    	# maybe rasing 'func' no in cmd_json
    	start_t = time.time()
    	if cmd_json['func'] not in self.cmd_dict:
    	    tcp_rx_msg['return'] = None
    	    tcp_rx_msg['error'] = "Not implemented functions"
    	    tcp_rx_msg['used_time'] = time.time() - start_t
    	    return
    	
    	try:
    	    ret = self.cmd_dict[cmd_json['func']](*cmd_json['args'])
            tcp_rx_msg['return'] = ret
            tcp_rx_msg['error'] = None
            tcp_rx_msg['used_time'] = time.time() - start_t
            return
        except Exception as e:
            tcp_rx_msg['return'] = None
            tcp_rx_msg['error'] = str((type(e),e))
            tcp_rx_msg['used_time'] = time.time() - start_t
            return
    
def tcp_server():
    cmd_client = Command_server()

    # get the hostname
    host = "192.168.2.100"
    port = 10000  # initiate port no above 1024
    
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server binded with %s:%d"%(host, port))
    
    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    tcp_tx_msg = {
    	'func' : None,
    	'args' : None
    }

    tcp_rx_msg = {
    	'return' : None,
    	'error' : None,
    	'used_time': None
    }
    
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data_str = conn.recv(2048)
        if not data_str:
            # if data is not received 
            print("No data is recevied")
            break
        elif data_str == "close_server":
            print("Get close server request")
            global keep_server_on
            keep_server_on = False
            break
        cmd_json = pickle.loads(data_str)
        print("From connected user: ", cmd_json)
        
        # calling the function
        cmd_client.call_func(cmd_json, tcp_rx_msg)
        
        # send back reply 
        print("Sending reply: ", tcp_rx_msg)  
        conn.send(pickle.dumps(tcp_rx_msg))  # send data back to the client
    
    print("Closing the server and disconnected from the robot") 
    cmd_client.close_robot()
    server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    conn.close()  # close the connection

if __name__ == "__main__":
    
    while keep_server_on:
        tcp_server()
        time.sleep(0.5)
