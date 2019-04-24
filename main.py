from __future__ import with_statement

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from inter_pb2 import *
import communication

import select
import socket
import pdb
import time

# synchronization
import threading

WORLD_HOST = 'vcm-9314.vm.duke.edu'  # The server's hostname or IP address
WORLD_UPS_PORT = 12345        # The port used by the server
WORLD_AMZ_PORT = 23456
UPS_PORT = 34567

# global sequence numbers
world_seq_num = 0
amazon_seq_num = 0

# locks for sequence numbers
world_seq_lock = threading.Lock()
amazon_seq_lock = threading.Lock()

# todo: Burak
# no seqnum required
def init_trucks(conn_req):
    conn_req.trucks.extend([UInitTruck(id = 1, x = 1, y = 1),])
    return

def test_new(sock,isAmazon,creation, newStuff):
    conn_req = AConnect() if isAmazon else UConnect()
    conn_req.isAmazon = isAmazon
    if not creation:
        conn_req.worldid = 4 # config file
    if newStuff and not isAmazon:
        init_trucks(conn_req)
    if newStuff and isAmazon:
        conn_req.initwh.extend([AInitWarehouse(id = 1, x = 1, y = 1),])
    ENCODED_MESSAGE = conn_req.SerializeToString()

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    WORLD_PORT = WORLD_AMZ_PORT if isAmazon else WORLD_UPS_PORT
    sock.connect((WORLD_HOST, WORLD_PORT))
    
    communication.sendallMod(ENCODED_MESSAGE,sock)
    encoded_response = communication.recvMod(sock)
    conn_resp = AConnected() if isAmazon else UConnected()
    conn_resp.ParseFromString(encoded_response)
    print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(conn_req.__str__(),conn_resp.__str__()))
    return
        
##        
def wait_aconnect(sock):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((socket.gethostname(), UPS_PORT))
    sock.listen()
    return

##
def selector(inputs, outputs, message_queues):
    while inputs:
        readable,writable,exceptional = select.select(inputs,outputs,message_queues)
        for s in readable:
            if s is sock_WORLD:
                print("sock_world")
                pass
            
            elif s is sock_AMZ:
                print("sock_amazon")
                pass
            pass
        pass
    return


if __name__ == "__main__":
    sock_WORLD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_new(sock_WORLD, isAmazon = False, creation=False,newStuff=False)

    # Uncomment these to activate amazon
    sock_AMZ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wait_aconnect(sock_AMZ)
    conn, addr = sock_AMZ.accept()

    #Add amazon to 'inputs' to listen them as well
    inputs = [sock_WORLD, sock_AMZ]
    outputs = []
    message_queues = {}
    
    t=threading.Thread(target=selector(inputs, outputs, message_queues))
    t.start()
