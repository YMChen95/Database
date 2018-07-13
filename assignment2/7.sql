prompt Question 7 - me7
SELECT p.sin,p.name,p.addr 
from people p, ticket t
where p.sin = t.violator_no and t.vtype <> 'parking' and t.vdate <='11-Feb-2016' and t.vdate>='12-Feb-2015'
group by p.sin,p.name,p.addr
having count(*) = 3;
