from app import db
from app.models import Job,Language,Room,Room_info

j = Job(desc="식음료부")
j1 = Job(desc="조리부")
j2 = Job(desc="객실부")
j3 = Job(desc="객실관리부")
j4 = Job(desc="사무직")

db.session.add(j)
db.session.add(j1)
db.session.add(j2)
db.session.add(j3)
db.session.add(j4)

l = Language(lang = "English")
l1 = Language(lang = "Korean")
l2 = Language(lang = "japanese")
l3 = Language(lang = "chinese")

db.session.add(l)
db.session.add(l1)
db.session.add(l2)
db.session.add(l3)


ri=Room_info(room_type="Double",room_class="Standard",fee=180000,capacity=2)
ri1=Room_info(room_type="Single",room_class="Superior",fee=140000,capacity=1)
ri2=Room_info(room_type="Family",room_class="Suite",fee=500000,capacity=5)
ri3=Room_info(room_type="Twin",room_class="Deluxe",fee=200000,capacity=2)



r1 = Room(num=211)
ri.rooms.append(r1)

r2 = Room(num=311)
ri1.rooms.append(r2)

r3 = Room(num=411)
ri2.rooms.append(r3)

r4 = Room(num=511)
r5 = Room(num=512)
ri3.rooms.append(r4)
ri3.rooms.append(r5)

db.session.add(ri)
db.session.add(ri1)
db.session.add(ri2)
db.session.add(ri3)
db.session.commit()



db.session.commit()
