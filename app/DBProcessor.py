from app import db
from app.models import *
from datetime import datetime

def availableRooms(checkin_date, checkout_date, n_people):
    avail_list = db.session.query(Room_info, db.func.count(Room.num).label('n_rooms')) \
        .filter(Room_info.id == Room.room_info_id).filter(Room_info.capacity >= 1).group_by(Room_info.id)

    reserved_rooms = []

    for i in avail_list:
        resreved_rooms.append(db.session.query(db.func.count(Reserve.id))\
            .filter(Reserve.room_info_id == i.Room_info.id).first()[0])
        


    return avail_list,
