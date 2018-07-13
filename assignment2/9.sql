prompt Question 9 - me7
select distinct sin, name
from people p, owner o, vehicle_history h
where p.sin = o.owner_id and o.vehicle_id = h.vehicle_no and(h.average_price <=all
(select average_price
from vehicle_history)
or (h.number_sales  >= all ( SELECT number_sales from vehicle_history))
or (h.total_tickets >= all ( SELECT total_tickets from vehicle_history )));
