from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from inter_pb2 import * 

import socket
import pdb
import time

import math
import io
from communication import * 
WORLD_HOST = 'vcm-9314.vm.duke.edu'  # The server's hostname or IP address
WORLD_PORT = 12345
AMAZON_PORT = 34567            # Listen at this port for amazon
import pdb


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
        command.deliveries.extend([sub_object.make_delivery,])
        pass
    elif sub_object.type is 'uQuery':
        command.queries.extend([sub_object.query,])
    elif sub_object.type is 'uInitTruck':
        command.queries.extend([sub_object.init_truck,])
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
        self.pickup_request.seqnum = seq_num

        self.type = 'uGoPickup'
        return
    pass

class InitializeTruck:
    def __init__(self,t_id,x,y):
        self.init_truck = UInitTruck()
        self.init_truck.id = t_id
        self.init_truck.x = x
        self.init_truck.y = y
        self.type = 'uInitTruck'
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
        '''        for del_loc in del_locs:
            if type(del_loc) is DeliveryLocation:
                del_loc = del_loc.delivery_location'''
        del_locs = list(map(lambda d : d.delivery_location if type(d) is DeliveryLocation else d, del_locs))
        print(del_locs)
        self.make_delivery = UGoDeliver()
        self.make_delivery.truckid = t_id
        self.make_delivery.packages.extend(del_locs) # enter a list of DeliveryLocation objs
        self.make_delivery.seqnum = seq_num

        self.type = 'uGoDeliver'
        return

    def AddDeliveryLocation(del_loc):
        self.make_delivery.packages.extend([del_loc,])
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

def test_world_commands():
    send = UCommands()
    pickup = PickupFromWarehouse(1,1,1)
    delivery_location = DeliveryLocation(10, 3, 4)
    del_locs = [delivery_location,]
    #del_locs = [d.delivery_location for d in del_locs]
    make_delivery = MakeDelivery(9, del_locs, 5)

    query = QueryTruck(100, 6)
    add_to_world_command(send, pickup)
    add_to_world_command(send, pickup)
    add_to_world_command(send, make_delivery)
    add_to_world_command(send, query)

    print(send)

    return


def test_new(sock):
    conn_req = UConnect()
    conn_req.isAmazon = False
    conn_req.worldid = 13
    #trucks = [InitializeTruck(x,0,0) for x in range(0,10)]
    #trucks = [x.init_truck for x in trucks]
    #conn_req.trucks.extend(trucks)

    ENCODED_MESSAGE = conn_req.SerializeToString()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.connect((WORLD_HOST, WORLD_PORT))
    sendallMod(ENCODED_MESSAGE,sock)

    encoded_response = recvMod(sock)
    conn_resp = UConnected()
    conn_resp.ParseFromString(encoded_response)
    print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(conn_req.__str__(),conn_resp.__str__()))
    

def test_command(sock):
    send = UCommands()
    pickup = PickupFromWarehouse(1,1,1)
    delivery_location = DeliveryLocation(10, 3, 4)
    del_locs = [delivery_location,]
    #del_locs = [d.delivery_location for d in del_locs]
    make_delivery = MakeDelivery(9, del_locs, 5)

    query = QueryTruck(2, 6)
    add_to_world_command(send, pickup)
    add_to_world_command(send, pickup)
    add_to_world_command(send, make_delivery)
    add_to_world_command(send, query)
    ENCODED_MESSAGE = send.SerializeToString()
    sendallMod(ENCODED_MESSAGE,sock)
    encoded_response = recvMod(sock)
    conn_resp = UResponses()
    conn_resp.ParseFromString(encoded_response)
    print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(send.__str__(),conn_resp.__str__()))


def test_command(sock):
    send = UCommands()
    pickup = PickupFromWarehouse(2,1,1)
    delivery_location = DeliveryLocation(10, 3, 4)
    del_locs = [delivery_location,]
    #del_locs = [d.delivery_location for d in del_locs]
    make_delivery = MakeDelivery(9, del_locs, 5)

    query = QueryTruck(2, 6)
    add_to_world_command(send, pickup)
    add_to_world_command(send, pickup)
    add_to_world_command(send, make_delivery)
    add_to_world_command(send, query)
    ENCODED_MESSAGE = send.SerializeToString()
    sendallMod(ENCODED_MESSAGE,sock)
    encoded_response = recvMod(sock)
    conn_resp = UResponses()
    conn_resp.ParseFromString(encoded_response)
    print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(send.__str__(),conn_resp.__str__()))

def test_init(sock):

    pickup = PickupFromWarehouse(1,1,1)
    delivery_location = DeliveryLocation(10, 3, 4)
    del_locs = [delivery_location,]
    #del_locs = [d.delivery_location for d in del_locs]
    make_delivery = MakeDelivery(9, del_locs, 5)

    query = QueryTruck(100, 6)
    add_to_world_command(send, pickup)
    add_to_world_command(send, pickup)
    add_to_world_command(send, make_delivery)
    add_to_world_command(send, query)
    ENCODED_MESSAGE = send.SerializeToString()
    sendallMod(ENCODED_MESSAGE,sock)
    encoded_response = recvMod(sock)
    conn_resp = UResponses()
    conn_resp.ParseFromString(encoded_response)
    print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(send.__str__(),conn_resp.__str__()))
    
    

    
#test_world_commands()



'''send = UCommands()
pickup = PickupFromWarehouse(1,1,1)
delivery_location = DeliveryLocation(10, 3, 4)
del_locs = [delivery_location,]
#del_locs = [d.delivery_location for d in del_locs]
make_delivery = MakeDelivery(9, del_locs, 5)

query = QueryTruck(100, 6)
add_to_world_command(send, pickup)
add_to_world_command(send, pickup)
add_to_world_command(send, make_delivery)
add_to_world_command(send, query)

print(send)
'''

#-----------------------receiver-------------------------#

