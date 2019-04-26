from connect_db import engine
from sqlalchemy.orm import Session

from connect_db import Truck, OutgoingSeqWorld, OutgoingSeqUA
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
from google.protobuf.json_format import MessageToJson, Parse

from world_ups_pb2 import *
from inter_pb2 import *
import communication

session = Session(engine)

def resend_unacked_world(sock_WORLD):
    unacked_list = session.query(OutgoingSeqWorld).filter(OutgoingSeqWorld.acked == False)
    for unacked in unacked_list:
        #ENCODED_MESSAGE = unacked.message.encode('utf-8')
        tempCommand = UCommands()
        Parse(unacked.message, tempCommand)
        ENCODED_MESSAGE = tempCommand.SerializeToString()
        print(ENCODED_MESSAGE)
        communication.sendallMod(ENCODED_MESSAGE,sock_WORLD)

def resend_unacked_amazon(sock_AMZ):
    unacked_list = session.query(OutgoingSeqUA).filter(OutgoingSeqUA.acked == False)
    for unacked in unacked_list:
        tempCommand = UACommands()
        Parse(unacked.message, tempCommand)
        ENCODED_MESSAGE = tempCommand.SerializeToString()
        print(ENCODED_MESSAGE)
        communication.sendallMod(ENCODED_MESSAGE,sock_AMZ)


def init_trucks(conn_req):
    conn_req.trucks.extend([UInitTruck(id = 1, x = 1, y = 1),])
    return
