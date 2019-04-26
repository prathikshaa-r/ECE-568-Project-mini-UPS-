from connect_db import session, Truck

def choose_truck(wh_x,wh_y):
    '''
    Preliminary method now(Loop through trucks we have, and try to find available
    '''
    trucks_list = session.query(Truck).all()
    for truck in trucks_list:
        if truck.status == 'IDLE' or truck.status == 'ARRIVING WAREHOUSE' or truck.status == 'DELIVERING':
            return truck.truck_id        
    return False
