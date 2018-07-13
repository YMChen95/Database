prompt Question 4 - me7
select p.name 
from people p, drive_licence d, ticket t, ticket_type tt 
where p.sin = d.sin and d.class <> 'nondriving' and p.sin=t.violator_no and t.vtype = tt.vtype
group by p.sin, p.name
having sum(tt.fine)>ALL (
select sum(tt.fine) / count(distinct d.licence_no)
from people p, drive_licence d,ticket t, ticket_type tt
where p.sin = d.sin and d.class <> 'nondriving' and t.violator_no(+) = p.sin and tt.vtype (+) = t.vtype);

