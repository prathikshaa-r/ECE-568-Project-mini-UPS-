from connect_db import *

# Truck = Base.classes.UPS_truck
# Warehouse = Base.classes.UPS_warehouse
# Package = Base.classes.UPS_package
# IncomingSeqWorld = Base.classes.UPS_incomingseqworld
# OutgoingSeqWorld = Base.classes.UPS_outgoingseqworld
# IncomingSeqUA = Base.classes.UPS_incomingsequab
# OutgoingSeqUA = Base.classes.UPS_outgoingsequa

def init_warehouse(wh_id,wh_x,wh_y):
    if session.query(Warehouse).filter(Warehouse.w_id == wh_id).count() != 0:
        raise ValueError("Duplicate Warehouse")
    else:
        new_wh = Warehouse(w_id = wh_id, x = wh_x, y = wh_y)
        session.add(new_wh)
        session.commit()
def init_truck(tr_id,tr_x,tr_y,tr_st):
    if session.query(Truck).filter(Truck.truck_id == tr_id).count() != 0:
        raise ValueError("Duplicate Truck")
    else:
        new_tr = Truck(truck_id = tr_id, x = tr_x, y = tr_y, status = tr_st)
        session.add(new_tr)
        session.commit()
def init_package(pkg_id, pkg_tr):
    if session.query(Package).filter(Package.packageid == pkg_id).count() != 0:
        raise ValueError("Duplicate Package ID")
    else:
        #This part isn't working, 'truck=pkg_tr'
        new_pkg = Package(packageid = pkg_id, truck = pkg_tr)
        session.add(new_pkg)
        session.commit()
def init_incomingseqworld(seq_num):
    if session.query(IncomingSeqWorld).filter(IncomingSeqWorld.sequence_number == seq_num).count() != 0:
        raise ValueError("Duplicate Incoming Seq")
    else:
        new_seq = IncomingSeqWorld(sequence_number = seq_num)
        session.add(new_seq)
        session.commit()
        
def init_outgoingseqworld(seq_num):
    if session.query(OutgoingSeqWorld).filter(OutgoingSeqWorld.sequence_number == seq_num).count() != 0:
        raise ValueError("Duplicate Outgoing Seq")
    else:
        new_seq = OutgoingSeqWorld(sequence_number = seq_num, acked = False)
        session.add(new_seq)
        session.commit()
        
def init_incomingsequa(seq_num):
    if session.query(IncomingSeqUA).filter(IncomingSeqUA.sequence_number == seq_num).count() != 0:
        raise ValueError("Duplicate Incoming UA")
    else:
        new_seq = IncomingSeqUA(sequence_number = seq_num)
        session.add(new_seq)
        session.commit()
        
def init_outgoingsequa(seq_num):
    if session.query(OutgoingSeqUA).filter(OutgoingSeqUA.sequence_number == seq_num).count() != 0:
        raise ValueError("Duplicate Outgoing UA")
    else:
        new_seq = OutgoingSeqUA(sequence_number = seq_num, acked = False)
        session.add(new_seq)
        session.commit()
        
def idem_check_world(seq_num):
    if session.query(IncomingSeqWorld)\
                     .filter(IncomingSeqWorld.sequence_number == seq_num).count() !=0:
        return True
    else:
        return False
    
def idem_check_amazon(seq_num):
    if session.query(IncomingSeqUA)\
                     .filter(IncomingSeqUA.sequence_number == seq_num).count() !=0:
        return True
    else:
        return False
    
def change_truck_stat(tr_id,new_status):
    truck = session.query(Truck).filter(Truck.truck_id == tr_id).first()
    truck.status = new_status
    session.commit()
