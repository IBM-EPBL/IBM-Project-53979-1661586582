
create table accounts(
id int(13) not null auto_increment,
username varchar(50) not null,
password varchar(240) not null,
rollno number(20) not null,
email varchar(110) not null,
)engine=InnoDB auto_increment=2 default charset=utf8;