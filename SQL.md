table hospitals
id int auto_increment primary key
place_id varchar
name varchar
address varchar
latitude 緯度
longitude 經度
phone varchar
rating float
revie_count int
registration_type tinyint 0: 現場, 1: 預約, 2:混合, 3:未知

table hospitals_hours
id int auto_increment primary key
hospital_id foreign key
day_of_week tinyint 1=周一, 7=週日
open_time time
close_time time