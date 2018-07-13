prompt Question 2 - me7
select distinct p.name, p.addr
from people p, owner o1, owner o2, owner o3, vehicle v1, vehicle v2, vehicle v3
where(p.sin=o1.owner_id 
and p.sin=o2.owner_id 
and p.sin=o3.owner_id
and o1.is_primary_owner='y'
and o2.is_primary_owner='y'
and o3.is_primary_owner='y'
and o1.vehicle_id=v1.serial_no
and o2.vehicle_id=v2.serial_no
and o3.vehicle_id=v3.serial_no
and v1.serial_no<>v2.serial_no
and v2.serial_no<>v3.serial_no
and v1.serial_no<>v3.serial_no
and v1.type_id=1
and v2.type_id=1
and v3.type_id=1);
