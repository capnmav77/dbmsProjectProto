CREATE DATABASE IF NOT EXISTS hang_out;
USE hang_out;

create table users(
    username varchar(10) not null unique, 
    email_id varchar(30) not null unique, 
    street VARCHAR(30),
    city VARCHAR(30),
    state VARCHAR(30),
    gender enum("Male","Female","Prefer not to say") default "Prefer not to say", 
    password varchar(20) not null,
    about varchar(50) ,
    profile_picture blob,
    is_pro_member bool default false ,
    PRIMARY KEY (username)
);
insert into users values('Ramesh','rameshwar77411@gmail.com','cambridge road','bangalore','karnataka','Male','bananas123','nothing much to say', null,true);

create table interests(
    interest_id varchar(10) not null unique,
    interest_name varchar(10) not null,
    interest_desc varchar(50),
    primary key (interest_id)
);
drop table interests;
insert into interests values('I001','general','a general place to visit');

create table ho_group(
	ho_group_id varchar(10) not null, 
    ho_group_name varchar(10) not null, 
    ho_group_desc varchar(50) , 
    admin_name varchar(10) not null , 
    date_created date, 
    member_count int default 1 not null,
    previously_visited_loc varchar(10),
    primary key (ho_group_id),
    foreign key (admin_name ) references users(username)
);

insert into ho_group values('G00001','Test-group','just a test group','Ramesh', '2023-10-23', 1,null);
    
create table vis_locations(
	location_name varchar(20) not null unique, 
    location_type varchar(10) default 'I001' not null , #should refer a type of interest
    street VARCHAR(30),
    city VARCHAR(30),
    state VARCHAR(30),
    location_contact varchar(30) ,
    location_desc varchar(50), 
    location_rating int not null,  
    location_img blob,
    primary key (location_name),
	foreign key (location_type) references interests(interest_id) on update cascade 
);

insert into vis_locations values('Rameshs_house','I001', 'your','fav','home', 'rameshwar77411@gmail.com','its a friendly neighbourhood home' , 5,null);



create table planned_event(
	event_id varchar(10) not null, 
	event_name varchar(30) not null, 
	group_id varchar(10) not NULL,
    location_name varchar(20) not NULL, 
	event_date date,
    event_time time,
    event_desc varchar(50),
    pollx int default 0 not null, 
    change_location int default 0 not null, 
    primary key (event_id,group_id), 
    foreign key (location_name) references vis_locations(location_name) on delete cascade,
    foreign key (group_id) references ho_group(ho_group_id) on delete CASCADE
);

create table user_groups(
	member_name varchar(10) not null, 
    group_id varchar(10) not null,
    date_joined date,
    is_admin bool default false,
    primary key (member_name,group_id),
    foreign key (member_name) references users(username) on delete cascade,
    foreign key (group_id) references ho_group(ho_group_id) on delete cascade 
);
    
create table group_interests(
	group_id varchar(10) not NULL, 
    interest_id varchar(10) not NULL, 
    primary key (group_id,interest_id),
    foreign key (group_id) references ho_group(ho_group_id) on delete cascade,
    foreign key (interest_id) references interests(interest_id) on delete cascade
);
    


-- a function to check if the corresponding username's password matches the given password and return a authorise or unauthorise response
DELIMITER $$
CREATE FUNCTION check_password( username varchar(10), password varchar(20)) RETURNS BOOLEAN
READS SQL DATA
BEGIN
    DECLARE pass varchar(20);
    SELECT users.password INTO pass FROM users WHERE users.username = username;
    IF pass = password THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END$$
DELIMITER ;


-- a function to check if the username exists in the database or not for sign up COMMENT
DELIMITER $$
CREATE FUNCTION username_exists(username_to_check VARCHAR(10)) RETURNS BOOLEAN
READS SQL DATA
BEGIN
    DECLARE username_count INT;
    SELECT COUNT(*) INTO username_count FROM users WHERE username = username_to_check;
    IF username_count > 0 THEN
        RETURN TRUE; -- Username exists
    ELSE
        RETURN FALSE; -- Username doesn't exist
    END IF;
END$$
DELIMITER ;



