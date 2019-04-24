from __future__ import with_statement

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from world_amazon_pb2 import *
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
UPS_HOST = 'vcm-8949.vm.duke.edu'
UPS_PORT = 34567

# global sequence numbers
world_seq_num = 0
amazon_seq_num = 0

# locks for sequence numbers
world_seq_lock = threading.Lock()
amazon_seq_lock = threading.Lock()
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


def buymore(products, sock): # also take seqnum
    #AMAZON SENDS UPS AN ORDER
    conn_resp = AResponses()
    purchaseMore = APurchaseMore(whnum = 1, things = products, seqnum=100)

    buy = ACommands(buy = [purchaseMore,])
    #pdb.set_trace()
    ENCODED_MESSAGE = buy.SerializeToString()
    communication.sendallMod(ENCODED_MESSAGE,sock)
    
    encoded_response = communication.recvMod(sock)
    conn_resp.ParseFromString(encoded_response)
    print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(buy.__str__(),conn_resp.__str__()))
    return


def pack(products, sock):  # also take seqnum
    conn_resp = AResponses()

    pack = APack(whnum = 1, things = products, shipid = 1, seqnum=102)
    
    packcommand = ACommands(topack = [pack,])
    ENCODED_MESSAGE = packcommand.SerializeToString()
    communication.sendallMod(ENCODED_MESSAGE,sock)
    
    encoded_response = communication.recvMod(sock)
    conn_resp.ParseFromString(encoded_response)
    print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(packcommand.__str__(),conn_resp.__str__()))
    




def wait_aconnect(sock):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((socket.gethostname(), UPS_PORT))
    s.listen()
    #Is A sending a message when connecting?
    return

def selector(inputs, outputs, message_queues):

    while inputs:
        readable,writable,exceptional = select.select(inputs,outputs,message_queues)
        for s in readable:
            if s is sock_WORLD:
                 pass
            
            elif s is sock_AMZ:
                conn, addr = s.accept()
                pass
            pass
        pass
    return


if __name__ == "__main__":
    # connect to world
    sock_WORLD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_new(sock_WORLD, isAmazon = True, creation=False,newStuff=False)

    # connect to UPS
    sock_UPS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock_UPS.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDRESS, 1)
    sock_UPS.connect((UPS_HOST, UPS_PORT))
    print("Successfully connected to UPS.")
    

    # Uncomment these to activate amazon
    # sock_AMZ = socket.socket(socket.af_inet, socket.SOCK_STREAM)
    # wait_aconnect(sock_AMZ)
    # conn, addr = sock_AMZ.accept()

    #Add amazon to 'inputs' to listen them as well
    inputs = [sock_WORLD]
    outputs = []
    message_queues = {}

   
    t=threading.Thread(target=selector(inputs, outputs, message_queues))
    t.start()
