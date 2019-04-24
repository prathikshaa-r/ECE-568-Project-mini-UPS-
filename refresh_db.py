from connect_db import session as s
from connect_db import Truck, OutgoingSeqWorld
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

from world_ups_pb2 import *
from inter_pb2 import *
import communication

def refresh_trucks(sock_WORLD):
    trucks_list = session.query(Truck).all()
    seq_num = session.query(OutgoingSeqWorld).count()#New seq num
    if seq_num != 0:
        seq_num = session.query(OutgoingSeqWorld).all()[count-1].sequence_number + 1
    for truck in trucks_list:
        query_truck = UCommands(queries = [UQuery(truckid = truck.truck_id, seqnum = seq_num),])
        ENCODED_MESSAGE = query_truck.SerializeToString()
        communication.sendallMod(ENCODED_MESSAGE,sock_WORLD)
        init_outgoingseqworld(seqnum, ENCODED_MESSAGE)
        seqnum += 1

def resend_unacked_world(sock_WORLD):
    unacked_list = session.query(OutgoingSeqWorld).filter(OutgoingSeqWorld.acked == False)
    for unacked in unacked_list:
        ENCODED_MESSAGE = unacked.message
        communication.sendallMod(ENCODED_MESSAGE,sock_WORLD)

def resend_unacked_amazon(sock_AMZ):
    unacked_list = session.query(OutgoingSeqUA).filter(OutgoingSeqUA.acked == False)
    for unacked in unacked_list:
        ENCODED_MESSAGE = unacked.message
        communication.sendallMod(ENCODED_MESSAGE,sock_AMZ)


def init_trucks(conn_req):
    conn_req.trucks.extend([UInitTruck(id = 1, x = 1, y = 1),])
    return
