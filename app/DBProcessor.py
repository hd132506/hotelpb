from app import tempData
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
            .filter(Guest.check_out_date >= checkin_date, Guest.check_out_date <= checkout_date)\
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

def make_reservation():
    g = Guest(first_name=tempData.CustomerData.first_name,\
                last_name=tempData.CustomerData.last_name,\
                check_in_date=tempData.CustomerData.checkin_date,\
                check_out_date=tempData.CustomerData.checkout_date,\
                head_cnt=tempData.CustomerData.n_people,\
                birthday=tempData.CustomerData.birthday,\
                phone=tempData.CustomerData.phone_number,\
                email=tempData.CustomerData.email)
    r = Reserve(room_info_id=tempData.RoomData.room_info_id, paid=False)
    g.reserve.append(r)
    db.session.add(g)
    db.session.commit()

def add_new_staff():
    # s = Employee(\
    #         first_name=,\
    #         last_name=,\
    #         job=,\
    #         phone=,\
    #         username=,\
    # )
    # db.session.add.(s)
    # db.session.commit()
    pass

def add_new_task():
    # t = Task()
    # db.session.add(t)
    # db.session.commit()
    pass

def remove_task():
    # db.session.delete()
    # db.session.commit()
    pass

def assign_staff():
    db.session.commit()
    pass
