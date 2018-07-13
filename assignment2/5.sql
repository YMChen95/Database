prompt Question 5 - me7
select vt.type, a.s_date,(sum(a.price)/count(distinct v.serial_no)) as avgprice
from   auto_sale a, vehicle v, vehicle_type vt
where  a.vehicle_id = v.serial_no and v.type_id = vt.type_id
group by vt.type, a.s_date
having a.s_date in
(select a.s_date
from auto_sale a
where a.s_date>='01-Jan-2010' and a.s_date<='31-Dec-2013');
