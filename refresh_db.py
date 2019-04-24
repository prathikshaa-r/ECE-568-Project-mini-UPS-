from connect_db import session as s
from connect_db import Truck, OutgoingSeqWorld
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from inter_pb2 import *
import communication

def refresh_db(sock):
    trucks_list = session.query(Truck).all()
    seq_num = session.query(OutgoingSeqWorld).count()#New seq num
    if seq_num != 0:
        seq_num = session.query(OutgoingSeqWorld).all()[count-1].sequence_number + 1
        
    for truck in trucks_list:
        query_truck = UCommands(queries = UQuery(truckid = truck.truck_id,seqnum = seq_num))
        ENCODED_MESSAGE = query_truck.SerializeToString()
        communication.sendallMod(ENCODED_MESSAGE,sock)
        encoded_response = communication.recvMod(sock)
        conn_resp = UResponses()
        conn_resp.ParseFromString(encoded_response)
        print("REQUEST :\n {} \n\nRESPONSE\n : {}\n\n".format(query_truck.__str__(),conn_resp.__str__()))
        seq_num += 1
        
