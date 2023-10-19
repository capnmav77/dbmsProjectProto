CREATE DATABASE IF NOT EXISTS hang_out;
USE hang_out;

create table users(
	user_id varchar(10) not NULL,
    username varchar(10) not null, 
    email_id varchar(10) not null , 
    location varchar(20) , 
    gender enum("Male","Female","Prefer not to say") default "Prefer not to say", 
    about varchar(50) ,
    profile_picture blob,
    is_pro_member bool default false ,
    PRIMARY KEY (user_id)
);
    
create table interests(
    interest_id varchar(10),
    interest_name varchar(10),
    primary key (interest_id)
);

create table ho_group(
	ho_group_id varchar(10) not null, 
    ho_group_name varchar(10) not null, 
    ho_group_desc varchar(50) , 
    admin_id varchar(10) not null, 
    date_created date, 
    member_count int default 1 not null,
    previously_visited_loc varchar(10),
    primary key (ho_group_id)
);
    
create table vis_locations(
	location_id varchar(10) not null,
    location_name varchar(20) not null, 
    location_type varchar(10) , #should refer a type of interest
    location_address varchar(30) not null,
    location_contact varchar(30) ,
    location_desc varchar(50), 
    location_rating int not null,  
    location_img blob,
    primary key (location_id),
	foreign key (location_type) references interests(interest_id)
);

create table planned_event(
	event_id varchar(10) not null, 
	event_name varchar(30) not null, 
	group_id varchar(10) not NULL,
    location_id varchar(10) not NULL, 
	event_date date,
    event_time time,
    event_desc varchar(50),
    pollx int default 0 not null, 
    change_location int default 0 not null, 
    primary key (event_id,group_id), 
    foreign key (location_id) references vis_locations(location_id) on delete cascade,
    foreign key (group_id) references ho_group(ho_group_id) on delete CASCADE
);

create table user_groups(
	member_id varchar(10) not null, 
    group_id varchar(10) not null,
    date_joined date,
    is_admin bool default false,
    primary key (member_id,group_id),
    foreign key (member_id) references users(user_id) on delete cascade,
    foreign key (group_id) references ho_group(ho_group_id) on delete cascade 
);
    
create table group_interests(
	group_id varchar(10) not NULL, 
    interest_id varchar(10) not NULL, 
    primary key (group_id,interest_id),
    foreign key (group_id) references ho_groups(ho_group_id) on delete cascade,
    foreign key (interest_id) references interests(interest_id) on delete cascade
);
    


--procedure for removing a user from the group
DELIMITER $$
CREATE PROCEDURE remove_user_from_group(IN member_id varchar(10), IN group_id varchar(10))
BEGIN
    -- check if the user is a admin 
    if (select is_admin from user_groups where member_id=member_id and group_id=group_id) then
        -- if admin then delete the group
        delete from ho_group where ho_group_id=group_id;
    end if;
    delete from user_groups where member_id=member_id and group_id=group_id ;
    update ho_group set member_count=member_count-1 where ho_group_id=group_id;
END$$
DELIMITER ;


--procedure for adding a user to the group
DELIMITER $$
CREATE PROCEDURE add_user_to_group(IN member_id varchar(10), IN group_id varchar(10))
BEGIN
    insert into user_groups values(member_id,group_id,curdate());
    update ho_group set member_count=member_count+1 where ho_group_id=group_id;
END$$
DELIMITER ; 

-- -- trigger to increment the pollx when a user votes
-- DELIMITER $$
-- CREATE TRIGGER increment_pollx AFTER INSERT ON poll
-- FOR EACH ROW
-- BEGIN
--     update planned_event set pollx=pollx+1 where event_id=new.event_id and group_id=new.group_id;
-- END$$
-- DELIMITER ;

-- -- trigger to increment the change_location when a user votes
-- DELIMITER $$
-- CREATE TRIGGER increment_change_location AFTER INSERT ON change_location
-- FOR EACH ROW
-- BEGIN
--     update planned_event set change_location=change_location+1 where event_id=new.event_id and group_id=new.group_id;
-- END$$
-- DELIMITER ;


--procedure to fetch the locations based on the interest of the group and return the result
DELIMITER $$
CREATE PROCEDURE fetch_locations(IN group_id varchar(10))
BEGIN
    select * from vis_locations where location_type in (select interest_id from group_interests where group_id=group_id);
    
END$$
DELIMITER ;

-- procedure to fetch the events of the group
DELIMITER $$
CREATE PROCEDURE fetch_events(IN group_id varchar(10))
BEGIN
    select * from planned_event where group_id=group_id;
END$$
DELIMITER ;

--trigger condition if the event is expired then to close the event based on current date and time
DELIMITER $$
CREATE TRIGGER close_event AFTER INSERT ON planned_event
FOR EACH ROW
BEGIN
    if (new.event_date<curdate()) then
        update planned_event set event_status="closed" where event_id=new.event_id and group_id=new.group_id;
    else if (new.event_date=curdate() and new.event_time<curtime()) then
        update planned_event set event_status="closed" where event_id=new.event_id and group_id=new.group_id;
    end if;
END$$
DELIMITER ;

--procedure to fetch the groups of the user
DELIMITER $$
CREATE PROCEDURE fetch_groups(IN member_id varchar(10))
BEGIN
    select * from ho_group where ho_group_id in (select group_id from user_groups where member_id=member_id);
END$$
DELIMITER ;

--procedure to fetch the events in the groups of the user 
DELIMITER $$
CREATE PROCEDURE fetch_events_in_groups(IN member_id varchar(10), IN group_id varchar(10))
BEGIN
    select * from planned_event where group_id=group_id and event_id in (select event_id from planned_event where group_id=group_id);
END$$
DELIMITER ;

    
    
