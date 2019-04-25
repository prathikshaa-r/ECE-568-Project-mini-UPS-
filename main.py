from __future__ import with_statement

from connect_db import *
from connect_db import session as s
from update_db import *
from connect_db import Truck as dbTruck

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from inter_pb2 import *
import inter_pb2 as pb
import communication

import select
import socket
import pdb
import time

# synchronization
import threading

WORLD_HOST = 'vcm-9314.vm.duke.edu'  # The server's hostname or IP address 'vcm-8252.vm.duke.edu'  # The server's hostname or IP address
WORLD_UPS_PORT = 12345        # The port used by the server
WORLD_AMZ_PORT = 23456
UPS_PORT = 34567

# global sequence numbers
global world_seq_num
global amazon_seq_num
world_seq_num = 1
amazon_seq_num = 1

# locks for sequence numbers
world_seq_lock = threading.Lock()
amazon_seq_lock = threading.Lock()

global sock_WORLD
global sock_AMZ
#----------------------------refresh trucks logic----------------------------#
def refresh_truck_handler(sock_WORLD):
    global sock_WORLD
    global world_seq_num
    trucks_list = session.query(Truck).all()
    for truck in trucks_list:
        with world_seq_lock:
            world_seq_num += 1
            seq_num = world_seq_num
            pass
        query_truck = UCommands(queries = [UQuery(truckid = truck.truck_id, seqnum = seq_num),])
        ENCODED_MESSAGE = query_truck.SerializeToString()
        communication.sendallMod(ENCODED_MESSAGE,sock_WORLD)
        init_outgoingseqworld(seq_num, ENCODED_MESSAGE)

#----------------------------------------------------------------------------#

# todo: Burak
# no seqnum required
def initTrucks(conn_req):
    global world_seq_num
    global amazon_seq_num
    for i in range(1,10):
        #add a truck to the database
        init_truck(i,i,i, "IDLE")
        #extend the connection request to have multiple trucks
        conn_req.trucks.extend([UInitTruck(id = i, x = i, y = i),])
    return

def initWarehouses(conn_req):
    global world_seq_num
    global amazon_seq_num
    for i in range(1,10):
        #add a truck to the database
        init_warehouse(i,i,i)
        #extend the connection request to have multiple trucks
        conn_req.trucks.extend([AInitWarehouse(id = i, x = i, y = i),])
    return

def test_new(sock,isAmazon,creation, newStuff):
    conn_req = AConnect() if isAmazon else UConnect()
    conn_req.isAmazon = isAmazon
    if not creation:
        conn_req.worldid = 8 # config file
    if newStuff and not isAmazon:
        conn_req.trucks.extend([UInitTruck(id = 1, x = 1, y = 1),])
        init_truck(1,1,1, "IDLE")
        #initTrucks(conn_req)
    if newStuff and isAmazon:
        initWarehouses(conn_req)
        #conn_req.initwh.extend([AInitWarehouse(id = 1, x = 1, y = 1),])
    ENCODED_MESSAGE = conn_req.SerializeToString()

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    WORLD_PORT = WORLD_AMZ_PORT if isAmazon else WORLD_UPS_PORT
    sock.connect((WORLD_HOST, WORLD_PORT))

    communication.sendallMod(ENCODED_MESSAGE,sock)
    encoded_response = communication.recvMod(sock)
    conn_resp = AConnected() if isAmazon else UConnected()
    print(conn_req)
    conn_resp.ParseFromString(encoded_response)

#    query_truck = UCommands(queries = [UQuery(truckid = 1, seqnum = 5),])
#    ENCODED_MESSAGE = query_truck.SerializeToString()
#    communication.sendallMod(ENCODED_MESSAGE,sock)
    print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(conn_req.__str__(),conn_resp.__str__()))
    return
        
##        
def wait_aconnect(sock):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((socket.gethostname(), UPS_PORT))
    sock.listen()
    return

##

#-------------------------------from world----------------------------#

# todo: Burak
def truck_status_handler(trucks):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    print("Thanks for the truck status. I'll be sure to ack you all!")
    world_acks=[]
    for truck in trucks:
        world_acks.append(truck.seqnum)
        if not idem_check_world(truck.seqnum):
            continue
        print(truck)
        change_truck_stat_withXY(truck.truckid, truck.status, truck.x, truck.y)
        init_incomingseqworld(truck.seqnum)

        # update to db
        # truck.truckid
        # truck.status
        # truck.x
        # truck.y
        pass
    world_send_acks(world_acks)
    return

def completions_handler(completions):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    print("Thanks for reaching warehouse, will notify amazon now. Also, acks to you.")
    world_acks = []
    #pdb.set_trace()
    for readyTruck in completions:
        world_acks.append(readyTruck.seqnum)
        if not idem_check_world(readyTruck.seqnum):
            continue
        
        print(readyTruck)
        # Truck to amazon
        with amazon_seq_lock:
            amazon_seq_num += 1
            seq_num = amazon_seq_num
            print(seq_num)
            pass

        
        # readyTruck.truckid
        # # use these to lookup warehouse id from warehouse db
        # readyTruck.x
        # readyTruck.y

        # readyTruck.status -- ? why

        #FINDING THE WAREHOUSE ID FROM X AND Y COORDS

        db_lookup_w_id = find_warehouse(readyTruck.x, readyTruck.y)

        pack = session.query(Package).filter(Warehouse.w_id == db_lookup_w_id).filter(dbTruck.truck_id == readyTruck.truckid).first() 

        db_lookup_p_id = pack.packageid
        
        truck = pb.Truck(whid = db_lookup_w_id, truckid = readyTruck.truckid, packageid = db_lookup_p_id, seqnum = seq_num)
        
        send = UACommands(arrived = [truck,])
        # encode and send to amazon
        encoded_msg = send.SerializeToString()
        communication.sendallMod(encoded_msg,sock_AMZ) 
        
        init_outgoingsequa(seq_num,encoded_msg)
        # save seq_num and above encoded msg to outgoing amazon seq db
        pass
    world_send_acks(world_acks)

    return

def delivered_handler(deliveries_made):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    world_acks = []
    print("Thanks for completing delivery, will notify amazon now. Also, acks to you")
    # Delivered to amazon
    for delivered in deliveries_made:
        world_acks.append(delivered.seqnum)
        if not idem_check_world(delivered.seqnum):
            continue

        print(delivered)
        
        # delivered.truckid -- update truck db?
        with amazon_seq_lock:
            amazon_seq_num += 1
            seq_num = amazon_seq_num
            pass
        delivered_msg = Delivered(packageid = delivered.packageid, seqnum = seq_num)
        
        send = UACommands(finish=[delivered_msg,])
        encoded_msg = send.SerializeToString()
        communication.sendallMod(encoded_msg,sock_AMZ)
        
        # encode delivered_msg and send to amazon

        # save seq_num and encoded msg to outgoing amazon seq db

        init_outgoingsequa(seq_num,encoded_msg)

        pass
    world_send_acks(world_acks)
        
    return

def world_send_acks(world_acks):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    send = UCommands(acks = world_acks)
    encoded_msg = send.SerializeToString()
    communication.sendallMod(encoded_msg,sock_WORLD) #JOJO

    return

def world_acks_handler(acks):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    print("Thanks for the acks, will stop sending you the message by updating db")
    # check if ack already updated in db, if not, update
    for ack in acks:
        change_outgoingseqworld(ack)
        print(ack)
    return

def finished_handler():
    global world_seq_num
    global amazon_seq_num
    print("I don't know when the world send a finished. Check and deal with it.")
    return

#-------------------------------from amazon----------------------------#
def pickup_handler(orders):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    print("Ack the request and make a UGoPickup to world")
    amazon_acks = []
    for order in orders:
        amazon_acks.append(order.seqnum)
        if not idem_check_amazon(order.seqnum):
            continue

        print(order)
        #pdb.set_trace()
        
        
        # order.whid
        # # todo: @David delivery addr or package -- save to db
        # order.x
        # order.y

        # order.packageid
        # order.upsusername


        # ADD PRODUCTS LATER FOR NOW JUST ADDING THE PACKAGE 
        # products = order.item
        # products.id
        # products.description
        # products.amount

        
        #find a truck (optimized or not)
        db_lookup_t_id = choose_truck(order.whid)
        init_package(order.packageid, db_lookup_t_id, order.whid, order.upsusername,
                     order.x, order.y)
        
        
        with world_seq_lock:
            world_seq_num += 1
            seq_num = world_seq_num
            pass

        send_pickup = UGoPickup(truckid = db_lookup_t_id, whid = order.whid, seqnum = seq_num)
        send = UCommands(pickups = [send_pickup,])
        print(send)
        encoded_msg = send.SerializeToString()
        print(encoded_msg)
        communication.sendallMod(encoded_msg,sock_WORLD) 
        
        # insert seq_num into db outgoing world seq
        init_outgoingseqworld(seq_num,encoded_msg)
        

        pass
    amazon_send_acks(amazon_acks)
        
    return

def delivery_handler(deliveries):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    print("Ack the request and make a UGoDeliver to world")
    amazon_acks = []
    for delivery in deliveries:
        amazon_acks.append(delivery.seqnum)
        if not idem_check_amazon(delivery.seqnum):
            continue

        print(delivery)
        
        # lookup loation in db and send truck to deliver

        pack_object = find_package(delivery.packageid)
        db_lookup_x = pack_object.x
        db_lookup_y = pack_object.y
        db_lookup_t_id = pack_object.truck_id # pack_object.truck.id???

        
        package = UDeliveryLocation(packageid = delivery.packageid, x = db_lookup_x, y = db_lookup_y)
        with world_seq_lock:
            world_seq_num += 1
            seq_num = world_seq_num
            pass
        
        send_delivery = UGoDeliver(truckid = db_lookup_t_id, packages = [package,], seqnum = seq_num)
        send = UCommands(deliveries = [send_delivery,])
        print(send)
        encoded_msg = send.SerializeToString()
        communication.sendallMod(encoded_msg,sock_WORLD)
        
        # insert seq_num and msg into db outgoing world seq
        init_outgoingseqworld(seq_num,encoded_msg)


        pass
    amazon_send_acks(amazon_acks)
        
    return

def warehouse_info_handler(warehouses):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    print("Ack all! Save info in db")
    acks = []
    for warehouse in warehouses:
        acks.append(warehouse.seqnum)
        if not idem_check_amazon(warehouse.seqnum):
            continue
        
        #init warehouse or update
        init_or_up_warehouse(warehouse.id, warehouse.x, warehouse.y)
        pass
    amazon_send_acks(acks)
    return

def amazon_send_acks(amazon_acks):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    send = UACommands(acks = amazon_acks)
    print(send)
    # encode and send acks to AMZ
    encoded_msg = send.SerializeToString()
    communication.sendallMod(encoded_msg,sock_AMZ) 
    return

def amazon_acks_handler(acks):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    print("Thanks for the acks, will stop sending you the message by updating db")
    # check if ack already updated in db, if not, update
    for ack in acks:
        change_outgoingsequa(ack)
        print(ack)
    return

def selector(inputs, outputs, message_queues):
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num

    while inputs:
#        if time.time() .... : Some time condition, spawn a new thread for each of below
#            refresh_truck_handler(sock,seqnum)
#            resend_unacked_world_handler(sock)
#            resend_unacked_amazon_handler(socK

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
                encoded_response = communication.recvMod(sock_AMZ)
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
                if len(resp.acks) > 0:
                    t8=threading.Thread(target=amazon_acks_handler(resp.acks))
                    t8.start()
                    pass
                pass
            pass
        pass
    return

global sock_WORLD
global sock_AMZ
global world_seq_num
global amazon_seq_num

if __name__ == "__main__":
    global sock_WORLD
    global sock_AMZ
    global world_seq_num
    global amazon_seq_num
    sock_WORLD = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_new(sock_WORLD, isAmazon = False, creation=True,newStuff=True)

    # Uncomment these to activate amazon
    LISTENER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wait_aconnect(LISTENER)
    sock_AMZ, addr = LISTENER.accept()
    #Add amazon to 'inputs' to listen them as well
    inputs = [sock_WORLD, sock_AMZ]
    outputs = []
    message_queues = {}
    
    t=threading.Thread(target=selector(inputs, outputs, message_queues))
    t.start()

    pass
