from connect_db import *

def delete_db():
    session.query(Product).delete()
    session.query(Package).delete()
    session.query(Truck).delete()
    session.query(Warehouse).delete()


    session.query(IncomingSeqWorld).delete()
    session.query(IncomingSeqUA).delete()
    session.query(OutgoingSeqWorld).delete()
    session.query(OutgoingSeqUA).delete()

    session.commit()
    return
