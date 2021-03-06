from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from inter_pb2 import * 

import socket
import pdb
import time

import math
from communication import * 

HOST = 'vcm-9314.vm.duke.edu'  # The server's hostname or IP address
WORLD_PORT = 12345
AMAZON_PORT = 34567            # Listen at this port for amazon
    

def test():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket.gethostname(), AMAZON_PORT))
        print("Listening on port: {} for Amazon.".format(AMAZON_PORT))
        
        s.close()

if __name__ == "__main__":
    test()
    pass

#-----------------------------sender-----------------------------#
"""
add a sub object to command
"""
def add_to_uacommand(command, sub_object):
    if sub_object.type is 'truck':
        command.arrived.extend([sub_object.truck,])
        pass
    elif sub_object.type is 'delivered':
        command.finish.extend([sub_object.delivered_msg,])
        pass
    return command


class TruckWrapper:
    def __init__(self, wh_id, t_id, p_id, seq_num):
        self.truck = Truck()
        self.truck.whid = wh_id
        self.truck.truckid = t_id
        self.truck.packageid = p_id
        self.truck.seqnum = seq_num

        self.type = 'truck'
        return
    pass

class DeliveredWrapper:
    def __init__(self, p_id, seq_num):
        self.delivered_msg = Delivered()
        self.delivered_msg.packageid = p_id
        self.delivered_msg.seqnum = seq_num

        self.type = 'delivered'
        return
    pass

def test_uacommand():
    delivered = DeliveredWrapper(1, 2)
    truckSent = TruckWrapper(1, 2, 3, 3)
    send = UACommands()
    add_to_uacommand(send, truckSent)
    add_to_uacommand(send, truckSent)
    add_to_uacommand(send, delivered)

    print(send)
    
    return

test_uacommand()

#-----------------------receiver-------------------------#





#----------------------locations------------------------#
class location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        return

class distance:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        return

    def __repr__(self):
        print("Point 1: ({}, {})".format(self.point1.x, self.point1.y))
        print("Point 2: ({}, {})".format(self.point2.x, self.point2.y))
        return ""

    def setStart(self, point1):
        self.point1 = point1
        return

    def setEnd(self, point2):
        self.point2 = point2

    def getDistance(self):
        self.distance = math.sqrt((self.point2.x - self.point1.x)**2 + (self.point2.y - self.point1.y)**2 )
        return self.distance

    pass

def test_distance():
    point1 = location(1,2)
    point2 = location(3,4)

    dist = distance(point1, point2)
    print(dist)
    print(dist.getDistance())
    return
