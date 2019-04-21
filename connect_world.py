from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from inter_pb2 import * 

import socket
import pdb
HOST = 'vcm-9314.vm.duke.edu'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
import time

def recvMod(sock):
    var_int_buff = []
    while True:
        buf = sock.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_message = sock.recv(msg_len)
    return whole_message

def sendallMod(mess,sock):
    _EncodeVarint(sock.send, len(mess), None)
    sock.sendall(mess)
    return


def sendCommand(command,sock):
    mess = command.SerializeToString()
    sendallMod(mess,sock)
    

def test():

    conn_req = UConnect()
    conn_req.isAmazon = False
    ENCODED_MESSAGE = conn_req.SerializeToString()
    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        sendallMod(ENCODED_MESSAGE,s)
        encoded_response = recvMod(s)
        conn_resp = UConnected()
        conn_resp.ParseFromString(encoded_response)
        
        print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(conn_req.__str__(),conn_resp.__str__()))
        s.close()

if __name__ == "__main__":
    test()
