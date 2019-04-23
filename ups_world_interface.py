from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from inter_pb2 import * 

import socket
import pdb
import time

import math

HOST = 'vcm-9314.vm.duke.edu'  # The server's hostname or IP address
WORLD_PORT = 12345
AMAZON_PORT = 34567            # Listen at this port for amazon


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


def sendCommand(command, sock):
    mess = command.SerializeToString()
    sendallMod(mess,sock)
    

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
def add_to_world_command(command, sub_object):
    if sub_object.type is 'uGoPickup':
        command.pickups.extend([sub_object.pickup_request,])
        pass
    elif sub_object.type is 'uGoDeliver':
        command.deliveries.extend([sub_object.delivery_request,])
        pass
    elif sub_object.type is 'uQuery':
        command.queries.extend([sub_object.query,])
    return command

def add_ack_to_world_command(command, ack):
    command.acks.extend([ack,])
    return

# optional
def adj_simspeed(command, simspeed):
    command.simspeed = simspeed
    return
# optional
def disconnect_world(command):
    command.disconnect = True
    return

#------------------sender wrappers----------------#
class PickupFromWarehouse:
    def __init__(self, t_id, w_id, seq_num):
        self.pickup_request = UGoPickup()
        self.pickup_request.truckid = t_id
        self.pickup_request.whid = w_id
        self.pickup_request.seq_num = seq_num

        self.type = 'uGoPickup'
        return
    pass


class DeliveryLocation:
    def __init__(self, p_id, x, y):
        self.delivery_location = UDeliveryLocation()
        self.delivery_location.packageid = p_id
        self.delivery_location.x = x
        self.delivery_location.y = y

        self.type = 'uDeliveryLocation'
        return
    pass

class MakeDelivery:
    def __init__(self, t_id, del_locs, seq_num):
        self.make_delivery = UGoDeliver()
        self.make_delivery.truckid = t_id
        self.make_delivery.packages.extend(del_locs) # enter a list of DeliveryLocation objs
        self.make_delivery.seqnum = seq_num

        self.type = 'uGoDeliver'
        return
    pass

class QueryTruck:
    def __init__(self, t_id, seq_num):
        self.query = UQuery()
        self.query.truckid = t_id
        self.query.seqnum = seq_num

        self.type = 'uQuery'
        return
    pass


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

