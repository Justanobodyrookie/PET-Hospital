create table hospitals(
id int auto_increment primary key,
place_id varchar(50),
name varchar(50),
address varchar(100),
location point,
phone varchar(20),
rating float,
review_count int,
registration_type tinyint comment '0: 現場, 1: 預約, 2:混合, 3:未知',
unique (place_id));

create table hospitals_hours(
id int auto_increment primary key,
hospital_id int,
day_of_week tinyint comment' 1=周一, 7=週日',
open_time time,
close_time time,
foreign key (hospital_id) references hospitals (id));