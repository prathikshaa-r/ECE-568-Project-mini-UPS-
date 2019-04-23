from connect_db import *

def handle_seq(session,seq_num):
    #Already exists, return ack
    if session.query(IncomingSeqWorld)\
              .filter(IncomingSeqWorld.sequence_number == seq_num).count() !=0:
        print("Already exists")
    else:
        print("Does not exist")
