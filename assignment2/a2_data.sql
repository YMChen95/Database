insert into people values
('0001','alpha',180.00,62.50,'brown','black','Edmonton','m','22-Jan-1995');
insert into people values
('0002','beta',175.25,68.59,'blue','golden','Calgary','f','02-Feb-1996');
insert into people values
('0003','theta',188.88,78.69,'black','grey','Red deer','m','15-Mar-1965');
insert into people values
('0004','omega',163.13,47.12,'white','black','Red deer','m','27-Apr-1988');
insert into people values
('0005','delta',155.80,50.15,'brown','brown','Edmonton','f','03-May-1973');
insert into people values
('0006','gamma',169.70,45.99,'green','pink','Vancouvour','f','23-Jun-1995');

insert into drive_licence values
('111','0001','5',null,'01-Jan-2015','01-Jan-2025');
insert into drive_licence values
('222','0002','5',null,'01-Jan-2015','01-Jan-2025');
insert into drive_licence values
('333','0003','5',null,'01-Jan-2015','01-Jan-2025');

INSERT INTO driving_condition values
 (1,'aaaaaaaa');
INSERT INTO driving_condition values
 (2,'bbbbbbb');
 

insert into vehicle_type values
(1,'SUV');
insert into vehicle_type values
(2,'Car');

insert into vehicle values
('0a','Audi','A4',2015,'white',2);
insert into vehicle values
('0b','BMW','X5','2008','black',1);
insert into vehicle values
('0c','BMW','X3','2012','black',1);
insert into vehicle values
('0d','BMW','325','2010','grey',2);
insert into vehicle values
('0e','Jeep','Cherokee','2016','red',1);
insert into vehicle values
('0f','Nissan','Juke','2007','orange',1);


insert into owner values
('0001','0a','n');
insert into owner values
('0001','0b','y');
insert into owner values
('0001','0c','y');
insert into owner values
('0001','0e','y');
insert into owner values
('0002','0a','n');
insert into owner values
('0003','0b','n');
insert into owner values
('0004','0c','n');
insert into owner values
('0005','0d','y');
insert into owner values
('0005','0f','y');

insert into auto_sale values
(1,'0003','0001','0a','1-Jan-2011',10000.);
insert into auto_sale values
(2,'0004','0001','0b','1-Jan-2012',20000.);
insert into auto_sale values
(3,'0005','0001','0e','1-Jan-2009',30000);
insert into auto_sale values
(4,'0002','0001','0b','1-Jan-2011',30000);
insert into auto_sale values
(5,'0001','0003','0e','1-Jan-2012',30000);

insert into ticket_type values
('parking',10.01);
insert into ticket_type values
('b',10.02);
insert into ticket_type values
('c',10.04);

insert into ticket values
('01','0001','0b','0006','parking','02-Jan-2015','zxc','vbn');
insert into ticket values
('02','0004','0c','0006','b','01-Jun-2015','asd','fgh');
insert into ticket values
('03','0005','0d','0006','c','01-Jun-2015','qwe','rty');
insert into ticket values
('04','0004','0c','0006','b','03-Jun-2015','zxc','vbn');
insert into ticket values
('05','0004','0c','0006','b','04-Jun-2015','zxc','vbn');