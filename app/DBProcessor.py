from app import db
from app.models import *
from datetime import datetime

def availableRooms(checkin_date, checkout_date, n_people):
    avail_list = db.session.query(Room_info, db.func.count(Room.num).label('n_rooms')) \
        .filter(Room_info.id == Room.room_info_id).filter(Room_info.capacity >= 1).group_by(Room_info.id)

    occupied_rooms = []
    idx = 0
    for i in avail_list:
        occupied_rooms.append(db.session.query(db.func.count(Reserve.id))\
            .filter(Reserve.room_info_id == i.Room_info.id)\
            .filter(Guest.id == Reserve.guest_id)\
            .filter(Guest.check_in_date >= checkin_date, Guest.check_in_date <= checkout_date)\
            .first()[0])

        occupied_rooms[idx] += db.session.query(db.func.count(Stay.room_num))\
            .filter(Stay.room_num.in_(\
                        db.session.query(Room.num).filter(Room.room_info_id == i.Room_info.id)\
                        )\
                    )\
            .filter(Guest.id == Stay.guest_id)\
            .filter(Guest.check_out_date >= checkin_date)\
            .first()[0]
        idx += 1



    return avail_list.all(), occupied_rooms
