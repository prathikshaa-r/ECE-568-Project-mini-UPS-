from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from world_amazon_pb2 import *
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
#---------------------------amazon to ups---------------------------#
#-----------------------------sender-----------------------------#
"""
add a sub object to command
"""
def add_to_au_command(command, sub_object):
    if sub_object.type is 'order':
        command.order.extend([sub_object.order,])
        pass
    elif sub_object.type is 'deliver':
        command.todeliver.extend([sub_object.request_delivery,])
        pass
    elif sub_object.type is 'warehouse':
        command.whinfo.extend([sub_object.warehouse,])
    return command

def add_ack_to_au_command(command, ack):
    command.acks.extend([ack,])
    return

#------------------sender wrappers----------------#
class ProductWrapper:
    def __init__(self, prod_id, desc, amt):
        self.product = Product()
        self.product.id = prod_id
        self.product.description = desc
        self.product.amount = amt

        self.type = 'product'
        return
    pass


class OrderWrapper:
    def __init__(self, w_id, x, y, p_id, ups_username, products, seq_num):
        products = list(map(lambda p : p.product if type(p) is ProductWrapper else p, products))
        self.order = Order()
        self.order.whid = w_id
        self.order.x = x
        self.order.y = y
        self.order.packageid = p_id
        self.order.upsusername = ups_username

        self.order.item.extend(products)

        self.order.seqnum = seq_num

        self.type = 'order'
        return
    pass

class DeliverWrapper:
    def __init__(self, p_id, seq_num):
        self.request_delivery = Deliver()
        self.request_delivery.packageid = p_id
        self.request_delivery.seqnum = seq_num

        self.type = 'deliver'
        return
    pass

class WarehouseInfo:
    def __init__(self, w_id, x, y, seq_num):
        self.warehouse = AWarehouse()
        self.warehouse.id = w_id
        self.warehouse.x = x
        self.warehouse.y = y
        self.warehouse.seqnum = seq_num

        self.type = 'warehouse'
        return
    pass

def test_au_commands():
    send = AUCommands()
    product1 = ProductWrapper(1,"test_product", 10)
    product2 = ProductWrapper(2, "test2+product", 20)
    product3 = ProductWrapper(1, "test_product", 15)

    products = [product1, product2, product3]
    
    order1 = OrderWrapper(1, 3, 4, 1, "user1", products, 1)

    order2 = OrderWrapper(2, 10, 6, 2, "user2", products, 2)

    warehouse1 = WarehouseInfo(1, 5, 8, 3)
    warehouse2 = WarehouseInfo(2, 3, 8, 4)

    deliver1 = DeliverWrapper(1, 5)
    deliver2 = DeliverWrapper(2, 6)
    
    add_to_au_command(send, order1)
    add_to_au_command(send, order2)
    add_to_au_command(send, warehouse1)
    add_to_au_command(send, warehouse2)
    add_to_au_command(send, deliver1)
    add_to_au_command(send, deliver2)
    
    print(send)

    return

test_au_commands()

#---------------------------amazon to world---------------------------#
#-----------------------------sender-----------------------------#
"""
add a sub object to command
"""
def add_to_amazon_world_command(command, sub_object):
    if sub_object.type is 'order':
        command.order.extend([sub_object.pickup_request,])
        pass
    elif sub_object.type is 'deliver':
        command.todeliver.extend([sub_object.make_delivery,])
        pass
    elif sub_object.type is 'warehouse':
        command.whinfo.extend([sub_object.query,])
    return command

def add_ack_to_amazon_world_command(command, ack):
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


