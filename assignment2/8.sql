prompt Question 8 - me7
drop view vehicle_history;
create view vehicle_history 
(vehicle_no, number_sales, average_price, total_tickets)as
select  h.serial_no, count(distinct transaction_id), avg(price), count(distinct t.ticket_no)
from  	vehicle h, auto_sale a, ticket t
where   t.vehicle_id (+) = h.serial_no and a.vehicle_id (+) = h.serial_no
group by h.serial_no;
