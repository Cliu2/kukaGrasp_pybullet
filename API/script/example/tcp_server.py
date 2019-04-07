import socket
import sys
import time
sys.path.append("../..")

# from rr.tcp_interface import *

test_speed = [5]
test_accel = [7]
test_delay = [4]

arm_server = None

def server_program():
    # get the hostname
    host = "127.0.0.1"
    port = 10000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))

        # data = raw_input(' -> ')
        conn.send(data.encode())  # send data back to the client

    conn.close()  # close the connection

if __name__ == '__main__':
    # setup TCP connection to the robotarm server
    # address = ('127.0.0.1', 2005)
    # arm_server = TcpInterface(address)
    # arm_server.connect()
    
    # # Config the robot
    # print(arm_server.sendAndRecv("openFreqStatusPort(2005, 1000)"))
    # time.sleep(0.5)
    # print(arm_server.sendAndRecv("motor(1)"))
    # time.sleep(0.5)
    # print(arm_server.sendAndRecv("robot(4,'KENT')\n"))
    # time.sleep(0.5)
    # print(arm_server.sendAndRecv('setMoveSpeed(2)\n'))
    # time.sleep(0.5)
    # print(arm_server.sendAndRecv('setMoveAccel(1)\n'))
    # time.sleep(0.5)
    # print(arm_server.sendAndRecv('getJoints()\n'))
    # time.sleep(0.5)
    
    print("Finnished arm_config")
    
    # est. connection
    while True:
        server_program()


