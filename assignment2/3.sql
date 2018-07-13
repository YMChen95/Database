prompt Question 3 - me7
select dl.licence_no, p.name
from drive_licence dl, people p
where p.sin=dl.sin 
and dl.class<>'nondriving'
minus
select licence_no, name 
from people p, drive_licence d, owner o, vehicle v 
where p.sin = d.sin AND d.class <> 'nondriving' AND p.sin = o.owner_id AND o.vehicle_id = v.serial_no AND v.color = 'red';
