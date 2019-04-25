from connect_db import *

session.query(Product).delete()
session.query(Package).delete()
session.query(Truck).delete()
session.query(Warehouse).delete()


session.query(IncomingSeqWorld).delete()
session.query(IncomingSeqUA).delete()
session.query(OutgoingSeqWorld).delete()
session.query(OutgoingSeqUA).delete()

session.commit()
