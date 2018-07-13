prompt Question 1 - me7
select distinct vehicle_id  
from owner, people
where (owner.owner_id = people.sin and people.addr NOT LIKE 'Edmonton');

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
prompt Question 3 - me7
select dl.licence_no, p.name
from drive_licence dl, people p
where p.sin=dl.sin 
and dl.class<>'nondriving'
minus
select licence_no, name 
from people p, drive_licence d, owner o, vehicle v 
where p.sin = d.sin AND d.class <> 'nondriving' AND p.sin = o.owner_id AND o.vehicle_id = v.serial_no AND v.color = 'red';
prompt Question 4 - me7
select p.name 
from people p, drive_licence d, ticket t, ticket_type tt 
where p.sin = d.sin and d.class <> 'nondriving' and p.sin=t.violator_no and t.vtype = tt.vtype
group by p.sin, p.name
having sum(tt.fine)>ALL (
select sum(tt.fine) / count(distinct d.licence_no)
from people p, drive_licence d,ticket t, ticket_type tt
where p.sin = d.sin and d.class <> 'nondriving' and t.violator_no(+) = p.sin and tt.vtype (+) = t.vtype);

prompt Question 5 - me7
select vt.type, a.s_date,(sum(a.price)/count(distinct v.serial_no)) as avgprice
from   auto_sale a, vehicle v, vehicle_type vt
where  a.vehicle_id = v.serial_no and v.type_id = vt.type_id
group by vt.type, a.s_date
having a.s_date in
(select a.s_date
from auto_sale a
where a.s_date>='01-Jan-2010' and a.s_date<='31-Dec-2013');
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
prompt Question 7 - me7
SELECT p.sin,p.name,p.addr 
from people p, ticket t
where p.sin = t.violator_no and t.vtype <> 'parking' and t.vdate <='11-Feb-2016' and t.vdate>='12-Feb-2015'
group by p.sin,p.name,p.addr
having count(*) = 3;
prompt Question 8 - me7
drop view vehicle_history;
create view vehicle_history 
(vehicle_no, number_sales, average_price, total_tickets)as
select  h.serial_no, count(distinct transaction_id), avg(price), count(distinct t.ticket_no)
from  	vehicle h, auto_sale a, ticket t
where   t.vehicle_id (+) = h.serial_no and a.vehicle_id (+) = h.serial_no
group by h.serial_no;
prompt Question 9 - me7
select distinct sin, name
from people p, owner o, vehicle_history h
where p.sin = o.owner_id and o.vehicle_id = h.vehicle_no and(h.average_price <=all
(select average_price
from vehicle_history)
or (h.number_sales  >= all ( SELECT number_sales from vehicle_history))
or (h.total_tickets >= all ( SELECT total_tickets from vehicle_history )));
