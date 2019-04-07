import socket, pickle, pdb
from pprint import pprint

def tcp_client():
    #host = socket.gethostname()  # as both code is running on same pc
    host = "192.168.2.100"
    port = 10000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    tcp_tx_msg = {
        'func' : None,
        'args' : None
    }
    tcp_rx_msg = {
        'return' : None,
        'error' : None,
        'used_time': None
    }
    input_str = raw_input("-->")  # take input

    while input_str.lower().strip() != 'bye':

        if input_str.lower().strip() == 'close_server':
            # closing the server
            client_socket.send(input_str.encode())
            print("closing the server")
            break

        # warpping the command and send it out
        input_str = input_str.split(" ")
        tcp_tx_msg['func'] = input_str[0]
        tcp_tx_msg['args'] = input_str[1:]

        print("Msg to send: ")
        pprint(tcp_tx_msg)
        cmd_str = pickle.dumps(tcp_tx_msg)

        client_socket.send(cmd_str.encode())  # send message

        # get the returns from the server
        response = client_socket.recv(1024).decode()  # receive response
        response = pickle.loads(response)

        print("Msg received: ")
        pprint(response)  # show in terminal

        # get the next input
        input_str = raw_input("-->")

    client_socket.close()  # close the connection

if __name__ == '__main__':
    tcp_client()

