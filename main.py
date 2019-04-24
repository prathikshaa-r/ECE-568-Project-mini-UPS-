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
                encoded_response = communication.recvMod(sock_WORLD)
                resp = UResponses()
                resp.ParseFromString(encoded_response)
                print(resp)

                if len(resp.truckstatus) > 0:
                    t1=threading.Thread(target=truck_status_handler(resp.truckstatus))
                    t1.start()
                    pass
                if len(resp.completions) > 0:
                    print("deal with completions")
                    t2=threading.Thread(target=completions_handler(resp.completions))
                    t2.start()
                    pass
                if len(resp.delivered) > 0:
                    print("deal with deliveries")
                    t3=threading.Thread(target=delivered_handler(resp.delivered))
                    t3.start()
                    pass
                if len(resp.acks) > 0:
                    print("deal with acks")
                    t4=threading.Thread(target=world_acks_handler(resp.acks))
                    t4.start()
                pass
            
            elif s is sock_AMZ:
                print("sock_amazon")
                encoded_response = communication.recvMod(sock_WORLD)
                resp = AUCommands()
                resp.ParseFromString(encoded_response)
                print(resp)

                if len(resp.order) > 0:
                    orders = resp.order
                    t5=threading.Thread(target=pickup_handler(orders))
                    t5.start()
                    pass
                if len(resp.todeliver) > 0:
                    deliveries = resp.todeliver
                    t6=threading.Thread(target=delivery_handler(deliveries))
                    t6.start()
                    pass
                if len(resp.whinfo) > 0:
                    warehouses = resp.whinfo
                    t7=threading.Thread(target=warehouse_info_handler(warehouses))
                    t7.start()
                    pass
                if len(acks) > 0:
                    t8=threading.Thread(target=amazon_acks_handler(acks))
                    t8.start()
                    pass
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

    pass

#-------------------------------from world----------------------------#

# todo: Burak
def truck_status_handler(trucks):
    print("Thanks for the truck status. I'll be sure to ack you all!")
    world_acks=[]
    for truck in trucks:
        print(truck)

        # update to db
        # truck.truckid
        # truck.status
        # truck.x
        # truck.y
        
        world_acks.append(truck.seqnum)
        pass
    world_send_acks(world_acks)
    return

def completions_handler(completions):
    print("Thanks for reaching warehouse, will notify amazon now. Also, acks to you.")
    world_acks = []
    for readyTruck in completions:
        print(readyTruck)
        # Truck to amazon
        with amazon_seq_lock:
            seq_num = ++amazon_seq_num
            pass
        
        # readyTruck.truckid
        # # use these to lookup warehouse id from warehouse db
        # readyTruck.x
        # readyTruck.y

        # readyTruck.status -- ? why

        world_acks.append(readyTruck.seqnum)
        with amazon_seq_lock:
            seq_num = ++amazon_seq_num
            pass
        
        truck = Truck(whid = db_lookup_w_id, truckid = readyTruck.truckid, packageid = db_lookup_p_id, seqnum = seq_num)
        send = UACommands(arrived = [truck,])
        # encode and send to amazon
        # save seq_num and above encoded msg to outgoing amazon seq db
        pass
    world_send_acks(world_acks)

    return

def delivered_handler(deliveries_made):
    world_acks = []
    print("Thanks for completing delivery, will notify amazon now. Also, acks to you")
    # Delivered to amazon
    for delivered in deliveries_made:
        print(delivered)
        
        # delivered.truckid -- update truck db?
        with amazon_seq_lock:
            seq_num = ++amazon_seq_lock
            pass
        delivered_msg = Delivered(packageid = delivered.packageid, seqnum = seq_num)
        send = UACommands(finish=[delivered_msg,])
        # encode delivered_msg and send to amazon
        # save seq_num and encoded msg to outgoing amazon seq db
        
        world_acks.append(delivered.seqnum)
        pass
    world_send_acks(world_acks)
        
    return

def world_send_acks(world_acks):
    send = UCommands(acks = world_acks)
    # encode and send acks to world
    return

def world_acks_handler(acks):
    print("Thanks for the acks, will stop sending you the message by updating db")
    # check if ack already updated in db, if not, update
    for ack in acks:
        print(ack)
    return

def finished_handler():
    print("I don't know when the world send a finished. Check and deal with it.")
    return

#-------------------------------from amazon----------------------------#
def pickup_handler(orders):
    print("Ack the request and make a UGoPickup to world")
    amazon_acks = []
    for order in orders:
        print(order)

        # order.whid
        # # todo: @David delivery addr or package -- save to db
        # order.x
        # order.y

        # order.packageid
        # order.upsusername
        # products = order.item
        # products.id
        # products.description
        # products.amount

        with world_seq_lock:
            seq_num = ++world_seq_num
            pass
        send_pickup = UGoPickup(truckid = db_lookup_t_id, whid = order.whid, seqnum = seq_num)
        send = UCommands(pickups = [send_pickup,])
        # insert seq_num into db outgoing world seq
        
        amazon_acks.append(order.seqnum)
        pass
    amazon_send_acks(amazon_acks)
        
    return

def delivery_handler(deliveries):
    print("Ack the request and make a UGoDeliver to world")
    amazon_acks = []
    for delivery in deliveries:
        print(delivery)
        
        # lookup lcoation in db and send truck to deliver
        package = UDeliveryLocation(packageid = delivery.packageid, x = db_lookup_x, y = db_lookup_y)
        with world_seq_lock:
            seq_num = ++world_seq_num
            pass
        
        send_delivery = UGoDeliver(truckid = db_lookup_t_id, packages = [package,], seqnum = seq_num)
        send = UCommands(deliveries = [send_delivery,])
        # insert seq_num and msg into db outgoing world seq

        amazon_acks.append(delivery.seqnum)
        pass
    amazon_send_acks(amazon_acks)
        
    return

def warehouse_info_handler(warehouses):
    print("Ack all! Save info in db")
    acks = []
    for warehouse in warehouses:
        acks.append(warehouse.seqnum)
        pass
    return

def amazon_send_acks(amazon_acks):
    send = UACommands(acks = amazon_acks)
    # encode and send acks to world
    return

def amazon_acks_handler(acks):
    print("Thanks for the acks, will stop sending you the message by updating db")
    # check if ack already updated in db, if not, update
    for ack in acks:
        print(ack)
    return