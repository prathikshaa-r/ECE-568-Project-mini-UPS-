from connect_db import *
from google.protobuf.json_format import MessageToJson, Parse

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

def init_or_up_warehouse(wh_id,wh_x,wh_y):
    wh_list = session.query(Warehouse).filter(Warehouse.w_id == wh_id)
    if wh_list.count():
        wh = wh_list.first()
        wh.x = wh_x
        wh.y = wh_y
        session.commit()
    else:
        new_wh = Warehouse(w_id = wh_id, x = wh_x, y = wh_y)
        session.add(new_wh)
        session.commit()

        
import pdb
def find_warehouse(wh_x,wh_y):
#    pdb.set_trace()
    wh = session.query(Warehouse).filter(Warehouse.x == wh_x).filter(Warehouse.y == wh_y).first()
    wh_id = wh.w_id
    return wh_id

        
def init_truck(tr_id,tr_x,tr_y,tr_st):
    if session.query(Truck).filter(Truck.truck_id == tr_id).count() != 0:
        x = 5
        #raise ValueError("Duplicate Truck")
    else:
        new_tr = Truck(truck_id = tr_id, x = tr_x, y = tr_y, status = tr_st)
        session.add(new_tr)
        session.commit()

def init_package(pkg_id, pkg_tr, pkg_wh, username, x, y, status):
    if session.query(Package).filter(Package.packageid == pkg_id).count() != 0:
        raise ValueError("Duplicate Package ID")
    else:
        #This part isn't working, 'truck=pkg_tr'
        user = session.query(User).filter(User.username == username).first()
        user_id = user.id#= 1#user.id
        new_pkg = Package(packageid = pkg_id, truck_id = pkg_tr,
                          warehouse_id = pkg_wh, user_id = user_id,x=x,y=y,status=status)
        session.add(new_pkg)
        session.commit()
        return
    
        
def init_product(product_list,pckg_id):
    num_product = session.query(Product).count() + 1
    for prdct in product_list:
        new_product = Product(id = num_product, productid = prdct.id, description = prdct.description,amount = prdct.amount, package_id = pckg_id)
        session.add(new_product)
        num_product += 1
    session.commit()

        

def find_package(pkg_id):
    pack_list = session.query(Package).filter(Package.packageid == pkg_id)
    if pack_list:
        return pack_list.first()
        
        
def init_incomingseqworld(seq_num):
    if session.query(IncomingSeqWorld).filter(IncomingSeqWorld.sequence_number == seq_num).count() != 0:
        raise ValueError("Duplicate Incoming Seq")
    else:
        new_seq = IncomingSeqWorld(sequence_number = seq_num)
        session.add(new_seq)
        session.commit()
        
def init_outgoingseqworld(seq_num, enc_msg):
    #enc_msg = MessageToJson(enc_msg)
    if session.query(OutgoingSeqWorld).filter(OutgoingSeqWorld.sequence_number == seq_num).count() != 0:
        raise ValueError("Duplicate Outgoing Seq")
    else:
        new_seq = OutgoingSeqWorld(sequence_number = seq_num, acked = False, message = enc_msg)
        session.add(new_seq)
        session.commit()
        
def init_incomingsequa(seq_num):
    if session.query(IncomingSeqUA).filter(IncomingSeqUA.sequence_number == seq_num).count() != 0:
        raise ValueError("Duplicate Incoming UA")
    else:
        new_seq = IncomingSeqUA(sequence_number = seq_num)
        session.add(new_seq)
        session.commit()
        
def init_outgoingsequa(seq_num, enc_msg):
    #enc_msg = enc_msg.decode("utf-8")
    if session.query(OutgoingSeqUA).filter(OutgoingSeqUA.sequence_number == seq_num).count() != 0:
        raise ValueError("Duplicate Outgoing UA")
    else:
        new_seq = OutgoingSeqUA(sequence_number = seq_num, acked = False, message = enc_msg)
        session.add(new_seq)
        session.commit()
        
def idem_check_world(seq_num):
    if session.query(IncomingSeqWorld)\
              .filter(IncomingSeqWorld.sequence_number == seq_num).count() == 0:
        return True
    else:
        return False
    
def idem_check_amazon(seq_num):
    if session.query(IncomingSeqUA)\
                     .filter(IncomingSeqUA.sequence_number == seq_num).count() ==0:
        return True
    else:
        return False
    
def change_truck_stat(tr_id,new_status):
    truck = session.query(Truck).filter(Truck.truck_id == tr_id).first()
    if truck:
        truck.status = new_status
        session.commit()
    else:
        raise(ValueError("Truck Doesn't Exist"))

def change_truck_stat_withXY(tr_id,status, x, y):
    truck = session.query(Truck).filter(Truck.truck_id == tr_id).first()
    print("updating truck with id {}".format(tr_id))
    if truck:
        truck.status = status
        truck.x = x
        truck.y = y
        session.commit()
    else:
        raise(ValueError("Truck Doesn't Exist"))

def change_outgoingsequa(seq_num):
    seq = session.query(OutgoingSeqUA).filter(OutgoingSeqUA.sequence_number == seq_num).first()
    if seq:
        seq.acked = True
        session.commit()
    else:
        raise(ValueError("Seq Doesn't Exist"))


def change_outgoingseqworld(seq_num):
    seq = session.query(OutgoingSeqWorld).filter(OutgoingSeqWorld.sequence_number == seq_num).first()
    if seq:
        seq.acked = True
        session.commit()
    else:
        raise(ValueError("Seq Doesn't Exist"))
    
def choose_truck(wh_id):
    '''
    Preliminary method now(Loop through trucks we have, and try to find available
    '''
    trucks_list = session.query(Truck).all()
    #warehouse = session.query(Warehouse).filter(Warehouse.id == wh_id).first()
    for truck in trucks_list:
        if truck.status == 'IDLE' or truck.status == 'ARRIVING WAREHOUSE' or truck.status == 'DELIVERING':
            return truck.truck_id        
    return False

