from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from amazon_ups_interface import *
from ups_world_interface import *
from amazon_mock_interface import * 
import communication
WORLD_HOST = 'vcm-9314.vm.duke.edu'  # The server's hostname or IP address
WORLD_UPS_PORT = 12345
WORLD_AMZ_PORT = 23456
AMAZON_PORT = 34567            # Listen at this port for amazon


def test_new(sock,isAmazon,creation, newStuff):
    conn_req = AConnect() if isAmazon else UConnect()
    #pdb.set_trace()
    conn_req.isAmazon = isAmazon
    if not creation:
        conn_req.worldid = 4
    if newStuff and not isAmazon:
        trucks = [InitializeTruck(x,0,0) for x in range(0,10)]
        trucks = [x.init_truck for x in trucks]
        conn_req.trucks.extend(trucks)
    if newStuff and isAmazon:
        x = 0
        conn_req.initwh.extend([AInitWarehouse(id = 1, x = 1, y = 1),])
        #warehouses = [InitializeWarehouse(x,0,0) for x in range(0,10)]
        #warehouses = [x.init_warehouse for x in trucks]
        #conn_req.warehouses.extend(trucks)
        
    ENCODED_MESSAGE = conn_req.SerializeToString()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    WORLD_PORT = WORLD_AMZ_PORT if isAmazon else WORLD_UPS_PORT
    
    sock.connect((WORLD_HOST, WORLD_PORT))
    
    communication.sendallMod(ENCODED_MESSAGE,sock)
    #pdb.set_trace()
    encoded_response = communication.recvMod(sock)
    if isAmazon:
        conn_resp = AConnected()
    else:
        conn_resp = UConnected()
    conn_resp.ParseFromString(encoded_response)
    print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(conn_req.__str__(),conn_resp.__str__()))
    return
## amazon to world

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
    


######################################################################################################

if __name__ == '__main__':
    #UPS AND AMZ CONNECT TO WORLD
    sockUPS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockAMZ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_new(sockUPS, isAmazon = False, creation=False,newStuff=False)
    test_new(sockAMZ, isAmazon = True, creation=False,newStuff= False)

    prod1 = AProduct(id = 1, description = "Tea", count = 10)
    products = [prod1,]

    buymore(products, sockAMZ)
    pack(products, sockAMZ)
     
    '''
    APack
      required int32 whnum = 1;
      repeated AProduct things = 2;
      required int64 shipid = 3;
      required int64 seqnum = 4;
    AProduct
      required int64 id = 1;
      required string description = 2;
      required int32 count = 3;
'''    
    
'''UPS connects to world
       UConnect()
       UInitTruck() list
<=========>
Amazon Connects to World
       Aconnect()
       AInittWarehouse() list
---------------------------------------------wait
Amazon Connects to UPS

UPS - socket accept
nothing
---------------------------------------------wait
Amazon gets a Buy Request
---------------------------------------------wait
Amazon sends a Buy request to UPS (internal)
       Order()
       Product() List
---------------------------------------------wait
Amazon sends request to world to pack package
       APack()
       AProduct() list   (id, description, count)

World Responds with package ready
      APacked()
<========>

UPS sends pickup request for truck
      UGoPickup()
World responds with truck at warehouse
      UFinished()
---------------------------------------------wait
UPS sends truck to amazon
    Truck()
---------------------------------------------wait
Amazon loads packages onto truck
      APutOnTruck()
World tells amazon packages are loaded
      ALoaded()
---------------------------------------------wait
Amazon tells UPS the packages are loaded
       Deliver()
---------------------------------------------wait
UPS tells world UGo Deliver
World tells ups delivered!
      UDeliveryMade()
UPS tells Amazon delivery complete
      Delivered()
'''
