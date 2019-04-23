from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from inter_pb2 import *

import select
import socket
import pdb
WORLD_HOST = 'vcm-9314.vm.duke.edu'  # The server's hostname or IP address
WORLD_PORT = 12345        # The port used by the server
UPS_HOST = '0.0.0.0'
UPS_PORT = 34567
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

def send_UGoPickUp(t_id, w_id):
    pickup = UGoPickup()
    pickup.truckid = t_id
    pickup.whid = w_id
    command = UCommand()

def sendCommand(command,sock):
    mess = command.SerializeToString()
    sendallMod(mess,sock)
    
def test(socket):
    conn_req = UConnect()
    conn_req.isAmazon = False
    ENCODED_MESSAGE = conn_req.SerializeToString()
    
    with socket as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.connect((WORLD_HOST, WORLD_PORT))
        sendallMod(ENCODED_MESSAGE,s)
        
        encoded_response = recvMod(s)
        conn_resp = UConnected()
        conn_resp.ParseFromString(encoded_response)
        print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(conn_req.__str__(),conn_resp.__str__()))       
        #return s
        #s.close()

def test_new(sock):
    conn_req = UConnect()
    conn_req.isAmazon = False
    ENCODED_MESSAGE = conn_req.SerializeToString()   
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.connect((WORLD_HOST, WORLD_PORT))
    sendallMod(ENCODED_MESSAGE,sock)
        
    # encoded_response = recvMod(sock)
    # conn_resp = UConnected()
    # conn_resp.ParseFromString(encoded_response)
    # print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(conn_req.__str__(),conn_resp.__str__()))
    
        #return s
        #s.close()
        
def wait_aconnect(sock):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((UPS_HOST, UPS_PORT))
    s.listen()
    #Is A sending a message when connecting?


if __name__ == "__main__":
    world_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_new(world_socket)

    #Uncomment these to activate amazon
    #amz_socket = socket.socket(socket.af_inet, socket.SOCK_STREAM)
    #wait_aconnect(amz_socket)
    #conn, addr = amz_socket.accept()

    #Add amazon to 'inputs' to listen them as well
    inputs = [world_socket]
    outputs = []
    message_queues = {}

    while inputs:
        readable,writable,exceptional = select.select(inputs,outputs,message_queues)
        for s in readable:
            if s is world_socket:
                encoded_response = recvMod(s)
                conn_resp = UConnected()
                conn_resp.ParseFromString(encoded_response)
                print("RESPONSE\n : {}\n".format(conn_resp.__str__()))
                pass
            
            elif s is a_socket:
                conn, addr = s.accept()
                pass
            pass 
