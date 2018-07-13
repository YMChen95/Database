prompt Question 6 - me7
select name 
from people p
where p.sin not in
(select p.sin
from people p, owner o, vehicle v
where  p.sin = o.owner_id and o.vehicle_id = v.serial_no and v.type_id in 
(select  v1.type_id
from vehicle v1 
group by v1.type_id,v1.year
having count(*)>=all(
select count(*)
from vehicle v2
where v2.year=v1.year
and v1.type_id<>v2.type_id)));
