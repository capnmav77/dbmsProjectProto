CREATE DATABASE IF NOT EXISTS hang_out;
USE hang_out;

create table users(
    username varchar(20) not null unique, 
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
select * from users;
select * from users where username = 'Ramesh';
insert into users values('Ramesh','rameshwar77411@gmail.com','cambridge road','bangalore','karnataka','Male','bananas123','nothing much to say', null,true);
insert into users values('Bharath','bharath@gmail.com','cambridge road','bangalore','karnataka','Male','bananas123','nothing much to say', null,true);
insert into users values('Zero','Zero@gmail.com','cambridge road','bangalore','karnataka','Male','bananas123','nothing much to say', null,true);

create table interests(
    interest_id varchar(10) not null unique,
    interest_name varchar(20) not null,
    interest_desc varchar(50),
    primary key (interest_id)
);
-- drop table interests;
insert into interests values('I004','Food','Yum');
insert into interests values('I003','Sports','Stress your bod to the limit');
insert into interests values('I001','general','a general place to visit');
insert into interests values('I002','concerts','concerts to party into ');

create table ho_group(
	ho_group_id varchar(10) not null unique, 
    ho_group_name varchar(20) not null, 
    ho_group_desc varchar(50) , 
    admin_name varchar(20) not null , 
    date_created date, 
    member_count int default 0 not null,
    previously_visited_loc varchar(10) ,
    pending_requests int default 0 not null ,
    primary key (ho_group_id),
    foreign key (admin_name) references users(username) 
);
select * from ho_group;
insert into ho_group values('G00001','Test-group','just a test group','Ramesh', '2023-10-23', 1,null,0);
insert into ho_group values('G00002','TG-2','just another test group','Ramesh', '2023-10-23', 1,null,0);
insert into ho_group values('G00003','TG-3','just another test group','Ramesh', '2023-10-23', 1,null,0);
insert into ho_group values('G00004','TG-4','just another test group','Bharath', '2023-10-23', 1,null,0);
delete from ho_group where ho_group_id = 'G00005';


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
select * from vis_locations;
insert into vis_locations values('Rameshs_house','I001', 'your','fav','home', 'rameshwar77411@gmail.com','its a friendly neighbourhood home' , 5,null);
insert into vis_locations values('Spain','I002', 'your','fav','country', 'spain@gmail.com','its spain !' , 5, null);

create table planned_event(
	event_id varchar(10) not null, 
	event_name varchar(30) not null, 
	group_id varchar(10) not NULL,
    location_name varchar(20) not NULL, 
	event_date date,
    event_time time,
    event_desc varchar(50),
    pollx int default 0 not null,  
    primary key (event_id,group_id), 
    foreign key (location_name) references vis_locations(location_name) on delete cascade,
    foreign key (group_id) references ho_group(ho_group_id) on delete CASCADE
);
select * from planned_event;
delete from planned_event where event_id = 'E00004';
insert into planned_event values('E00001','COACHELLA','G00001','Spain','2023-10-23','00:00:00','a huge concert to party',0);
insert into planned_event values('E00001','COACHELLA','G00004','Spain','2023-10-23','00:00:00','a huge concert to party',0);


create table user_groups(
	username varchar(20) not null, 
    group_id varchar(10) not null,
    date_joined date,
    primary key (username,group_id),
    foreign key (username) references users(username) on delete cascade,
    foreign key (group_id) references ho_group(ho_group_id) on delete cascade 
);



select * from user_groups;
insert into user_groups values('Ramesh','G00001','2023-10-23');
insert into user_groups values('Ramesh','G00002','2023-10-23');
insert into user_groups values('Ramesh','G00003','2023-10-23');
insert into user_groups values('Bharath','G00004','2023-10-23');
DELETE FROM user_groups WHERE group_id = 'G00002' AND username = 'Ramesh';
-- DELETE FROM user_groups WHERE group_id = 'G00002' AND member_name = 'Zero';

create table group_interests(
	group_id varchar(10) not NULL, 
    interest_id varchar(10) not NULL default 'I001', 
    primary key (group_id,interest_id),
    foreign key (group_id) references ho_group(ho_group_id) on delete cascade,
    foreign key (interest_id) references interests(interest_id) on delete cascade
);
insert into group_interests values('G00001','I001');


create table group_requests(
	group_id varchar(10) not null,
    username varchar(20) not null,
    primary key (group_id,username),
    foreign key (group_id) references ho_group(ho_group_id) on delete cascade,
    foreign key (username) references users(username) on delete cascade
);
insert into group_requests values('G00002','Bharath');
insert into group_requests values('G00002','Zero');
insert into group_requests values('G00004','Zero');
insert into group_requests values('G00004','Ramesh');
select * from group_requests;
DELETE FROM group_requests WHERE group_id = 'G00002' AND username = 'Ramesh';


-- Functions 

-- a function to check if the corresponding username's password matches the given password and return a authorise or unauthorise response :
DELIMITER $$
CREATE FUNCTION check_password(in_username VARCHAR(20), in_password VARCHAR(20))
RETURNS BOOLEAN DETERMINISTIC
BEGIN
    DECLARE user_password VARCHAR(20);
    SELECT password INTO user_password FROM users WHERE username = in_username;
    IF user_password = in_password THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END
$$
DELIMITER ;
#SELECT check_password('Ramesh', 'bananas123');

-- a function to check for pro users : 
DELIMITER $$
CREATE FUNCTION check_isprouser(in_username varchar(20))
RETURNS BOOLEAN DETERMINISTIC
BEGIN 
	declare result bool;
    SELECT is_pro_member INTO result FROM users WHERE username = in_username; 
    IF result = true THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END
$$
DELIMITER ;
#select check_isprouser('Ramesh');

DELIMITER $$
CREATE FUNCTION check_group_exists(in_group_id varchar(10))
RETURNS BOOLEAN DETERMINISTIC
BEGIN
    DECLARE groupcount int ;
    SELECT count(*) INTO groupcount 
    FROM ho_group
    WHERE ho_group_id = in_group_id;
    IF groupcount = 1 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END
$$
DELIMITER ;
#select check_group_exists('G00001');

DELIMITER $$

CREATE FUNCTION check_username(uname VARCHAR(255)) RETURNS INT DETERMINISTIC
BEGIN
    DECLARE user_exists INT;
    SET user_exists = (
        SELECT COUNT(*) FROM users WHERE username = uname
    );

    IF user_exists > 0 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END $$;

DELIMITER ;

DELIMITER $$

CREATE FUNCTION add_user(uname VARCHAR(255), uemail VARCHAR(255), upassword VARCHAR(255)) RETURNS INT DETERMINISTIC
BEGIN
    INSERT INTO users (username, email_id, password)
    VALUES (uname, uemail, upassword);
    
    RETURN 1;
END $$;

DELIMITER ;



-- Procedures

-- a procedure to add the user to the group on approval of the group admin 
DELIMITER $$
CREATE PROCEDURE accept_group_request(IN in_group_id VARCHAR(10), IN in_username VARCHAR(20))
BEGIN
    DECLARE request_exists INT;

    -- Check if the request exists
    SELECT COUNT(*) INTO request_exists FROM group_requests
    WHERE group_id = in_group_id AND username = in_username;

    -- If the request exists, add the user to the group and remove the request
    IF request_exists = 1 THEN
        INSERT INTO user_groups (username, group_id, date_joined)
        VALUES (in_username, in_group_id, CURDATE());
        
        DELETE FROM group_requests
        WHERE group_id = in_group_id AND username = in_username;
        
        update ho_group 
        set pending_requests = pending_requests - 1
        where ho_group_id = in_group_id;
        
         COMMIT;

        SELECT 'Request Processed Successfully' AS Result;
    ELSE
        SELECT 'Request Not Found' AS Result;
    END IF;
END
$$
DELIMITER ;
-- drop procedure accept_group_request ;
#call accept_group_request('G00002','Bharath');


DELIMITER $$
CREATE PROCEDURE get_user_groups(IN user_name VARCHAR(20))
BEGIN
	select ho_group_id as Groupid , ho_group_name as Groupname
    from ho_group join user_groups on ho_group.ho_group_id = user_groups.group_id
    where user_groups.username = user_name ;
END
$$
DELIMITER ;
#drop procedure get_user_groups;
#call get_user_groups('Bharath');


#getting groups with user as the admin : 
DELIMITER $$
CREATE PROCEDURE get_admin_groups(IN user_name VARCHAR(20))
BEGIN
	select ho_group_id as Groupid , ho_group_name as Groupname
    from ho_group as ho join user_groups as ug on ho.ho_group_id = ug.group_id
    where ug.username = user_name and ho.admin_name = user_name;
END
$$
DELIMITER ;
#call get_admin_groups('Bharath');

DELIMITER $$
CREATE PROCEDURE get_group_events(IN curr_group_id varchar(10))
BEGIN
	select event_id , event_name , location_name , event_date , event_time , event_desc , pollx
    from planned_event 
    where planned_event.group_id = curr_group_id ;
END
$$ 
DELIMITER ;
#CALL get_group_events('G00001');


#Procedure to get group_details 
DELIMITER $$
CREATE PROCEDURE get_group_details(IN curr_group_id varchar(10))
BEGIN
	select * 
    FROM ho_group
    where ho_group.ho_group_id = curr_group_id ;
END
$$
DELIMITER ; 
#CALL get_group_details('G00001');


#getting group_requests for admin approval 
DELIMITER $$ 
CREATE PROCEDURE get_group_requests(IN in_group_id VARCHAR(10))
BEGIN 
	select * 
    FROM group_requests
    WHERE group_id = in_group_id ;
END 
$$ 
DELIMITER ; 
#call get_group_requests('G00004');


DELIMITER $$ 
CREATE PROCEDURE add_group_requests(IN in_group_id VARCHAR(10),IN in_username varchar(20))
BEGIN 
	declare user_exists int;
    declare request_exists int;
    
    select count(*) into user_exists
    from user_groups
    where username = in_username and group_id = in_group_id;
    
    SELECT COUNT(*) INTO request_exists 
    FROM group_requests
    WHERE group_id = in_group_id AND username = in_username;
    
    IF user_exists = 1 or request_exists = 1 THEN
		SELECT 'user already in group or request is pending ' AS Result;
	ELSE
		insert into group_requests values(in_group_id,in_username);
        
		update ho_group 
		set pending_requests = pending_requests + 1
		WHERE ho_group_id = in_group_id;
        
        COMMIT;
        
        SELECT 'user request added ';
	end if;	
END 
$$ 
DELIMITER ;

-- drop procedure add_group_requests;
-- call add_group_requests('G00001','Zero');
-- select * from group_requests;
select * from group_requests;
select * from user_groups;
-- call add_group_requests('G00003','Bharath');

DELIMITER $$

CREATE PROCEDURE UpdateGroupAdminAndDeleteGroup(IN deleted_user VARCHAR(20))
BEGIN
    DECLARE admin_group_id VARCHAR(10);
    DECLARE longest_member VARCHAR(20);
    DECLARE member_count INT;

    SELECT ho_group_id INTO admin_group_id
    FROM ho_group
    WHERE admin_name = deleted_user;

    -- If the deleted user was an admin
    IF admin_group_id IS NOT NULL THEN
        -- Find the person who has been in the group for the longest time
        SELECT username INTO longest_member
        FROM user_groups
        WHERE group_id = admin_group_id
        ORDER BY date_joined
        LIMIT 1;

        -- Update the group admin name
        UPDATE ho_group
        SET admin_name = longest_member
        WHERE ho_group_id = admin_group_id;

        -- Check the member count in the group
        SELECT COUNT(*) INTO member_count
        FROM user_groups
        WHERE group_id = admin_group_id;

        -- If there are no members left in the group, delete the group
        IF member_count = 0 THEN
            DELETE FROM ho_group WHERE ho_group_id = admin_group_id;
        END IF;
    END IF;
END;
$$

DELIMITER ;



-- Triggers 

DELIMITER $$
CREATE TRIGGER update_member_count
AFTER INSERT ON user_groups
FOR EACH ROW
BEGIN
    -- Increment the member_count for the corresponding group
    UPDATE ho_group
    SET member_count = member_count + 1
    WHERE ho_group_id = NEW.group_id;
END
$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER delete_member_count
AFTER DELETE ON user_groups
FOR EACH ROW
BEGIN
    -- Decrement the member_count for the corresponding group
    UPDATE ho_group
    SET member_count = member_count - 1
    WHERE ho_group_id = OLD.group_id;
END
$$
DELIMITER ;


DELIMITER $$

CREATE TRIGGER after_delete_user
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    CALL UpdateGroupAdminAndDeleteGroup(OLD.username);
END;
$$
DELIMITER ;



