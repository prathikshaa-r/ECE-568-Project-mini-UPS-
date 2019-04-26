from connect_db import session, Truck
from amazon_ups_interface import location, distance
import sys
def imp_choose_truck(wh_x,wh_y):
    '''
    Preliminary method now(Loop through trucks we have, and try to find available
    '''
    wh_point = location(wh_x, wh_y)
    trucks_list = session.query(Truck).all()
    closest_truck_id = False #So if 1st is not available, no mistake there
    closest_distance = sys.maxsize
    
    for truck in trucks_list:
        if truck.status == 'IDLE' or truck.status == 'ARRIVING WAREHOUSE' or truck.status == 'DELIVERING':
            new_distance = distance(wh_point, location(truck.x, truck.y)).getDistance()
            if new_distance < closest_distance:
                closest_distance = new_distance
                closest_truck_id = truck.truck_id
                  
    return closest_truck_id
