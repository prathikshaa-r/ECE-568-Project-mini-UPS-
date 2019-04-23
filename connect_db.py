from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


Base = automap_base()
engine = create_engine('postgresql://postgres:abc123@127.0.0.1/testdb')
Base.prepare(engine,reflect = True)
session = Session(engine)
Truck = Base.classes.UPS_truck
Warehouse = Base.classes.UPS_warehouse
Package = Base.classes.UPS_package
IncomingSeqWorld = Base.classes.UPS_incomingseqworld
OutgoingSeqWorld = Base.classes.UPS_outgoingseqworld
IncomingSeqUA = Base.classes.UPS_incomingsequa
OutgoingSeqUA = Base.classes.UPS_outgoingsequa

