-- 2018400090 - 2018400150
 CREATE database SimpleBounDB;
 USE SimpleBounDB;
 

-- Create table for database managers.
CREATE TABLE IF NOT EXISTS Database_Manager
(username VARCHAR(50) NOT NULL, 
password VARCHAR(256) NOT NULL,
PRIMARY KEY (username));

-- Create table for departments.
CREATE TABLE IF NOT EXISTS Departments
(department_id VARCHAR(50) NOT NULL,
department_name VARCHAR(50) NOT NULL,
PRIMARY KEY (department_id),
UNIQUE (department_name));

-- Create table for classrooms.

CREATE TABLE IF NOT EXISTS Classrooms 
(classroom_id VARCHAR(50) NOT NULL,
PRIMARY KEY (classroom_id));

-- Create table for physical locations of classrooms.

CREATE TABLE IF NOT EXISTS Physical_Locations
(classroom_id VARCHAR(50) NOT NULL,
classroom_capacity INTEGER NOT NULL,
campus VARCHAR(50) NOT NULL,
PRIMARY KEY (classroom_id),
FOREIGN KEY (classroom_id) REFERENCES Classrooms(classroom_id) ON UPDATE CASCADE ON DELETE CASCADE);

-- Create table for users.

CREATE TABLE IF NOT EXISTS Users 
(username VARCHAR(50) NOT NULL, 
name VARCHAR(50) NOT NULL,
surname VARCHAR(50) NOT NULL,
email VARCHAR(255) NOT NULL,
password VARCHAR(256) NOT NULL,
department_id VARCHAR(50) NOT NULL,
PRIMARY KEY (username),
FOREIGN KEY (department_id) REFERENCES Departments(department_id) ON UPDATE CASCADE ON DELETE CASCADE);

-- Create table for students.

CREATE TABLE IF NOT EXISTS Students
(username VARCHAR(50) NOT NULL, 
student_id VARCHAR(50) NOT NULL, 
completed_credits INTEGER DEFAULT 0,
GPA FLOAT(3,2) DEFAULT NULL,
weightedGrade FLOAT(5,1) DEFAULT 0,
PRIMARY KEY (username),
FOREIGN KEY (username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE,
UNIQUE (student_id));

-- Create table for instructors.

CREATE TABLE IF NOT EXISTS Instructors
(username VARCHAR(50) NOT NULL,
title VARCHAR(50) NOT NULL CHECK (title in ('Assistant Professor', 'Associate Professor', 'Professor')),
PRIMARY KEY (username),
FOREIGN KEY (username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE);

-- Create table for courses.

CREATE TABLE IF NOT EXISTS Courses 
(course_id VARCHAR(50) NOT NULL,
name VARCHAR(50) NOT NULL,
department_id VARCHAR(50) NOT NULL,
course_code VARCHAR(50) NOT NULL,
quota INTEGER NOT NULL,
classroom_id VARCHAR(50) NOT NULL,
credits INTEGER NOT NULL,
time_slot INTEGER NOT NULL CHECK (time_slot<11 AND time_slot>0),
instructor_username VARCHAR(50) NOT NULL,
PRIMARY KEY (course_id),
UNIQUE(classroom_id, time_slot),
FOREIGN KEY (classroom_id) REFERENCES Classrooms(classroom_id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (instructor_username) REFERENCES Instructors(username) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (department_id) REFERENCES Departments(department_id) ON UPDATE CASCADE ON DELETE CASCADE);

-- Create table for prerequisites.

CREATE TABLE IF NOT EXISTS Prerequisites
(course_id VARCHAR(50) NOT NULL,
prerequisite_id VARCHAR(50) NOT NULL,
PRIMARY KEY (course_id, prerequisite_id),
FOREIGN KEY (course_id) REFERENCES Courses(course_id),
FOREIGN KEY (prerequisite_id) REFERENCES Courses(course_id),
 -- Foreign key referential actions (ON UPDATE, ON DELETE)
 -- are prohibited on columns used in CHECK constraints.
 -- Likewise, CHECK constraints are prohibited on columns used in foreign key referential actions.
CHECK (course_id > prerequisite_id));


-- Create table for added courses.


CREATE TABLE IF NOT EXISTS Added_Courses
(student_id VARCHAR(50) NOT NULL,
course_id VARCHAR(50) NOT NULL,
PRIMARY KEY (student_id, course_id),
FOREIGN KEY (student_id) REFERENCES Students(student_id),
FOREIGN KEY (course_id) REFERENCES Courses(course_id));



-- Create table for grades.
 
CREATE TABLE IF NOT EXISTS Grades
(grade FLOAT(2,1) NOT NULL,
student_id VARCHAR(50) NOT NULL,
course_id VARCHAR(50) NOT NULL,
PRIMARY KEY (student_id, course_id),
FOREIGN KEY (student_id) REFERENCES Students(student_id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON UPDATE CASCADE ON DELETE CASCADE);


-- Create trigger to fix database managers' size.

DELIMITER $$

CREATE TRIGGER limitSize 
BEFORE INSERT
ON Database_Manager
FOR EACH ROW
BEGIN
   DECLARE db_cnt BIGINT;
   SELECT COUNT(*) AS cnt
     FROM Database_Manager 
     INTO db_cnt ;
   IF db_cnt >= 4 THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'There are already 4 database managers. You can not add more.';
   END IF;
END$$

DELIMITER ;


-- Create trigger to update credits and GPA.

DELIMITER $$

CREATE TRIGGER addGrade
AFTER INSERT
ON Grades
FOR EACH ROW
BEGIN
	UPDATE ((Grades
    INNER JOIN Courses ON Grades.course_id = Courses.course_id)
    INNER JOIN Students ON Grades.student_id = Students.student_id)
    SET GPA = (weightedGrade + credits*new.grade) / (completed_credits + credits),
		completed_credits = completed_credits + credits,
		weightedGrade = weightedGrade + credits*new.grade
		WHERE Courses.course_id = new.course_id and Students.student_id = new.student_id;
END$$
DELIMITER ;


-- Create trigger to prevent an instructor from adding a course whose quota is larger than the classrom capacity.



DELIMITER $$
CREATE TRIGGER limitQuota
BEFORE INSERT
ON Courses
FOR EACH ROW
BEGIN
	DECLARE capacity INT;
   
    SELECT classroom_capacity FROM Physical_Locations
    WHERE classroom_id = new.classroom_id
    INTO capacity;
    
    IF capacity < new.quota THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course quota can not be greater than the capacity of the classroom.';
	END IF;	
END$$
DELIMITER ;

-- 2

DELIMITER $$  
CREATE PROCEDURE login_dbm (IN dbm_username VARCHAR(50), IN input_password VARCHAR(256))  
BEGIN  
	IF dbm_username NOT IN (SELECT username FROM Database_Manager WHERE username = dbm_username) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username is not valid.';
	ELSE
		SELECT * FROM Database_Manager WHERE username = dbm_username and password = SHA2(input_password, 256) ;
	END IF;
END $$ 
DELIMITER ;



DELIMITER $$  
CREATE PROCEDURE login_student (IN stu_username VARCHAR(50), IN input_password VARCHAR(256))  
BEGIN  
	IF stu_username NOT IN (SELECT username FROM Students WHERE username = stu_username) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username is not valid.';
	ELSE
		SELECT * FROM Users WHERE username = stu_username and password = SHA2(input_password, 256) ;
	END IF;
END $$ 
DELIMITER ;

DELIMITER $$  
CREATE PROCEDURE login_ins (IN ins_username VARCHAR(50), IN input_password VARCHAR(256))  
BEGIN  
	IF ins_username NOT IN (SELECT username FROM Instructors WHERE username = ins_username) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username is not valid.';
	ELSE
		SELECT * FROM Users WHERE username = ins_username and password = SHA2(input_password, 256) ;
	END IF;
END $$ 
DELIMITER ;

-- 3

DELIMITER $$  
CREATE PROCEDURE delete_student (IN input_student_id VARCHAR(50))  
BEGIN 
	IF input_student_id NOT IN (SELECT student_id FROM Students) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student ID is not valid.';
	ELSE
		DELETE Users
		FROM Users
		INNER JOIN Students 
		ON Users.username = Students.username 
		WHERE student_id = input_student_id;
	END IF;
END $$  
DELIMITER ;



-- 4

DELIMITER $$  
CREATE PROCEDURE update_ins_title (IN input_username VARCHAR(50), IN input_title VARCHAR(50))  
BEGIN 
	DECLARE message VARCHAR(100);
	IF input_username NOT IN (SELECT username FROM Instructors) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Instructor username is not valid.';
	ELSEIF STRCMP(input_title, 'Assistant Professor') AND STRCMP(input_title, 'Associate Professor') AND STRCMP(input_title, 'Professor') THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Title is not valid.';
    ELSEIF NOT STRCMP(input_title, (SELECT title FROM Instructors WHERE username = input_username)) THEN
		SET message =  CONCAT ('Title of the instructor is already ', input_title, '.');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = message;
	ELSE
		UPDATE Instructors 
		SET title = input_title
		WHERE username = input_username;
	END IF;
END $$  
DELIMITER ; 


-- 5

DELIMITER $$  
CREATE PROCEDURE view_students ()  
BEGIN  
	SELECT Users.username, name, surname, email, department_name, completed_credits, GPA
	FROM ((Students
	INNER JOIN Users ON Students.username = Users.username)
	INNER JOIN Departments ON Departments.department_id = Users.department_id)
	ORDER BY completed_credits ASC;
END $$  
DELIMITER ; 


-- 6

DELIMITER $$  
CREATE PROCEDURE view_instructors ()  
BEGIN  
	SELECT Users.username, name, surname, email, department_name, title
	FROM ((Instructors
	INNER JOIN Users ON Instructors.username = Users.username)
	INNER JOIN Departments ON Departments.department_id = Users.department_id);
END $$  
DELIMITER ; 


-- 7

DELIMITER $$  
CREATE PROCEDURE view_student_grades (IN input_student_id VARCHAR(50))  
BEGIN  
	IF input_student_id NOT IN (SELECT student_id FROM Students) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student ID is not valid.';
	ELSE
		SELECT Courses.course_id, Courses.name AS course_name , grade
		FROM ((Grades
		INNER JOIN Courses ON Grades.course_id = Courses.course_id)
		INNER JOIN Students ON Grades.student_id = Students.student_id)
		WHERE Students.student_id = input_student_id;    
	END IF;
END $$  
DELIMITER ;  



-- 8

DELIMITER $$  
CREATE PROCEDURE view_ins_courses (IN input_ins_username VARCHAR(50))  
BEGIN  
	IF input_ins_username NOT IN (SELECT instructor_username FROM Courses) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Instructor username is not valid.';
	ELSE
		SELECT Courses.course_id, Courses.name AS course_name, Physical_Locations.classroom_id, campus, time_slot
		FROM (Physical_Locations
		INNER JOIN Courses ON Physical_Locations.classroom_id = Courses.classroom_id)
		WHERE instructor_username = input_ins_username;    
	END IF;
END $$  
DELIMITER ;  



-- 9


DELIMITER $$  
CREATE PROCEDURE view_avg_grade (IN input_course_id VARCHAR(50))  
BEGIN  
	IF input_course_id NOT IN (SELECT course_id FROM Courses) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course ID is not valid.';
	ELSE
		SELECT Courses.course_id, Courses.name AS course_name, sum(grade)/count(grade) AS average_grade
		FROM Courses
		LEFT JOIN Grades ON Grades.course_id = Courses.course_id 
		WHERE Courses.course_id = input_course_id;
	END IF;
END $$ 
DELIMITER ;

-- 10

DELIMITER $$  
CREATE PROCEDURE add_dbm (IN input_dbm_username VARCHAR(50), IN input_password VARCHAR(256))  
BEGIN     
    IF input_dbm_username IN (SELECT username FROM Database_Manager WHERE username = input_dbm_username) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username is already taken.';
	ELSE
		INSERT INTO Database_Manager VALUES(input_dbm_username, SHA2(input_password, 256));
	END IF;
END $$  
DELIMITER ;




DELIMITER $$  
CREATE PROCEDURE add_student (IN input_stu_username VARCHAR(50),IN input_stu_name VARCHAR(50),
IN input_stu_surname VARCHAR(50),IN input_mail VARCHAR(50), IN input_password VARCHAR(256),
IN input_dep_id VARCHAR(50), IN input_stu_id VARCHAR(50))  
BEGIN     
    IF input_stu_username IN (SELECT username FROM Users WHERE username = input_stu_username) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username is already taken.';
	ELSEIF input_dep_id NOT IN (SELECT department_id
							FROM Departments
                            WHERE department_id = input_dep_id) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Department ID is not valid.';
	ELSEIF input_stu_id IN (SELECT student_id FROM Students WHERE student_id = input_stu_id)THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student ID is already taken.';
	ELSE
		INSERT INTO Users VALUES(input_stu_username, input_stu_name, input_stu_surname, input_mail, SHA2(input_password, 256), input_dep_id);
        INSERT INTO Students(username, student_id) VALUES(input_stu_username, input_stu_id);
	END IF;
END $$  
DELIMITER ;



DELIMITER $$  
CREATE PROCEDURE add_ins (IN input_ins_username VARCHAR(50),IN input_ins_name VARCHAR(50),
IN input_ins_surname VARCHAR(50),IN input_mail VARCHAR(50), IN input_password VARCHAR(256),
IN input_dep_id VARCHAR(50), IN input_title VARCHAR(50))  
BEGIN     
    IF input_ins_username IN (SELECT username FROM Users WHERE username = input_ins_username) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username is already taken.';
	ELSEIF input_dep_id NOT IN (SELECT department_id
							FROM Departments
                            WHERE department_id = input_dep_id) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Department ID is not valid.';
    ELSEIF STRCMP(input_title, 'Assistant Professor') AND STRCMP(input_title, 'Associate Professor') AND STRCMP(input_title, 'Professor') THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Title is not valid.';
	ELSE
		INSERT INTO Users VALUES(input_ins_username, input_ins_name, input_ins_surname, input_mail, SHA2(input_password, 256), input_dep_id);
        INSERT INTO Instructors VALUES(input_ins_username, input_title);
	END IF;
END $$  
DELIMITER ;


-- 11

DELIMITER $$  
CREATE PROCEDURE view_classrooms (IN input_time_slot INT)  
BEGIN  
	IF (input_time_slot>=11 OR input_time_slot<=0) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Time slot is not valid.';
	ELSE
		SELECT classroom_id, campus, classroom_capacity
        FROM Physical_Locations
        WHERE classroom_id NOT IN 
		(SELECT classroom_id
		FROM Courses
		WHERE time_slot = input_time_slot);
	END IF;
END $$  
DELIMITER ; 


-- 12

DELIMITER $$  
CREATE PROCEDURE add_course_ins (IN input_course_id VARCHAR(50),
IN input_course_name VARCHAR(50), IN input_course_code VARCHAR(50),
IN input_quota INT, IN input_classroom_id VARCHAR(50), IN input_credits INT,
IN input_time_slot INT, IN ins_username VARCHAR(50))  
BEGIN  
	DECLARE dep_id VARCHAR(50);
    SELECT department_id
		FROM Users
		INNER JOIN Instructors
		ON Users.username = Instructors.username
		WHERE Instructors.username = ins_username
		INTO dep_id;
		INSERT INTO Courses VALUES(input_course_id, input_course_name, dep_id,
								input_course_code, input_quota, input_classroom_id,
								input_credits, input_time_slot, ins_username);
	
END $$ 
DELIMITER ;


-- 13

DELIMITER $$  
CREATE PROCEDURE add_prerequisite (IN input_course_id VARCHAR(50), IN input_prerequisite_id VARCHAR(50))  
BEGIN  
	IF input_course_id NOT IN (SELECT course_id FROM Courses) OR input_prerequisite_id NOT IN (SELECT course_id FROM Courses)  THEN 
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course ID or Prerequisite ID is not valid.';
    ELSE    
		INSERT INTO prerequisites VALUES(input_course_id, input_prerequisite_id);
    END IF;    
END $$  
DELIMITER ;

-- 14


DELIMITER $$  
CREATE PROCEDURE view_my_courses_ins (IN ins_username VARCHAR(50))  
BEGIN  
	SELECT Courses.course_id, Courses.name AS course_name, Courses.classroom_id, time_slot, quota,
    GROUP_CONCAT(prerequisite_id ORDER BY prerequisite_id SEPARATOR ', ') AS prerequisites
	FROM ((Physical_Locations
	INNER JOIN Courses ON Physical_Locations.classroom_id = Courses.classroom_id)
    LEFT JOIN Prerequisites ON Courses.course_id = Prerequisites.course_id)
	WHERE instructor_username = ins_username
    GROUP BY Courses.course_id
    ORDER BY Courses.course_id ASC;
END $$  
DELIMITER ; 



-- 15

DELIMITER $$  
CREATE PROCEDURE view_my_students (IN ins_username VARCHAR(50), IN input_course_id VARCHAR(50))  
BEGIN  
	IF input_course_id NOT IN (SELECT course_id FROM Courses WHERE instructor_username = ins_username) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course ID is not valid.';	-- This course does not belong to you or does not exist.
	ELSE
		SELECT Users.username, Students.student_id, email, Users.name, surname
        FROM (((Users
        INNER JOIN Students ON Users.username = Students.username)
        INNER JOIN Added_Courses ON Students.student_id = Added_courses.student_id)
        INNER JOIN Courses ON Courses.course_id = Added_courses.course_id)
        WHERE instructor_username = ins_username and Courses.course_id = input_course_id;
	END IF;
END $$ 
DELIMITER ;


-- 16


DELIMITER $$  
CREATE PROCEDURE update_course_name (IN ins_username VARCHAR(50), IN input_course_id VARCHAR(50), IN input_course_name VARCHAR(50))  
BEGIN  
	IF input_course_id NOT IN (SELECT course_id FROM Courses WHERE instructor_username = ins_username) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course ID is not valid.';	-- This course does not belong to you or does not exist.
	ELSE
		UPDATE Courses
        SET Courses.name = input_course_name
        WHERE course_id = input_course_id;
	END IF;
END $$ 
DELIMITER ;


-- 17


DELIMITER $$  
CREATE PROCEDURE give_grade (IN ins_username VARCHAR(50), IN input_course_id VARCHAR(50),
IN input_student_id VARCHAR(50), IN input_grade FLOAT(2,1))  
BEGIN  
	IF input_student_id NOT IN (SELECT student_id 
								FROM Added_Courses 
                                INNER JOIN Courses 
                                ON Added_Courses.course_id = Courses.course_id
                                WHERE instructor_username = ins_username
                                AND Courses.course_id = input_course_id) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student ID or Course ID is not valid.';
	ELSE 
		INSERT INTO Grades VALUES(input_grade, input_student_id, input_course_id);
        DELETE FROM Added_Courses
        WHERE student_id = input_student_id 
        AND course_id = input_course_id;
	END IF;
END $$ 
DELIMITER ;


-- 18


DELIMITER $$  
CREATE PROCEDURE view_all_courses ()  
BEGIN  
	SELECT Courses.course_id, Courses.name AS course_name, Users.surname as instructor_surname,
	Departments.department_name, credits, classroom_id, time_slot, quota,
    GROUP_CONCAT(prerequisite_id ORDER BY prerequisite_id SEPARATOR ', ') AS prerequisites
	FROM ((((Users
	INNER JOIN Instructors ON Users.username = Instructors.username)
	INNER JOIN Departments ON Users.department_id = Departments.department_id)
    INNER JOIN Courses ON Courses.department_id = Departments.department_id)
    LEFT JOIN Prerequisites ON Courses.course_id = Prerequisites.course_id)
    GROUP BY Courses.course_id
    ORDER BY Courses.course_id ASC;
END $$  
DELIMITER ; 


-- 19


DELIMITER $$  
CREATE PROCEDURE add_course_stu (IN stu_username VARCHAR(50), IN input_course_id VARCHAR(50))  
BEGIN 
	DECLARE stu_id VARCHAR(50);
    DECLARE cnt_pre INT;
    DECLARE cnt_join INT;
    DECLARE cnt_enrolled INT;
    DECLARE course_quota INT;
    
	SELECT student_id FROM Students WHERE username = stu_username INTO stu_id;
    
    SELECT count(*)
    FROM (SELECT prerequisite_id FROM prerequisites WHERE course_id = input_course_id) AS x
    INTO cnt_pre;
    
    SELECT count(*)
    FROM (SELECT prerequisite_id FROM prerequisites WHERE course_id = input_course_id) AS x 
		INNER JOIN (SELECT course_id
					FROM Grades
                    WHERE student_id = stu_id ) AS y
		ON x.prerequisite_id = y.course_id
    INTO cnt_join;
    
    SELECT count(*) FROM Added_Courses WHERE course_id = input_course_id INTO cnt_enrolled;
    SELECT quota FROM Courses WHERE course_id = input_course_id INTO course_quota;
    
    IF input_course_id NOT IN (SELECT course_id FROM Courses) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course ID is not valid.';
	ELSEIF input_course_id IN (SELECT course_id
							FROM Grades
                            WHERE student_id = stu_id) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You cannot take this course again.';
	ELSEIF cnt_pre != cnt_join THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You do not meet the prerequisites.';
	ELSEIF cnt_enrolled = course_quota THEN  -- just to be sure
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You cannot add the course due to quota restrictions.';
	ELSE
		INSERT INTO Added_Courses VALUES(stu_id, input_course_id);
	END IF;
END $$  
DELIMITER ;




-- 20


DELIMITER $$  
CREATE PROCEDURE view_my_courses_stu (IN stu_username VARCHAR(50))  
BEGIN  
	DECLARE stu_id VARCHAR(50);
	SELECT student_id FROM Students WHERE username = stu_username INTO stu_id;
    
    SELECT Added_courses.course_id, Courses.name AS course_name, NULL AS grade 
    FROM Added_courses 
    INNER JOIN Courses ON Courses.course_id = Added_courses.course_id
    WHERE Added_courses.student_id = stu_id
    UNION
    SELECT Grades.course_id, Courses.name AS course_name, grade 
    FROM Grades 
    INNER JOIN Courses ON Courses.course_id = Grades.course_id
    WHERE Grades.student_id = stu_id;
    
END $$  
DELIMITER ;



-- 21



DELIMITER $$  
CREATE PROCEDURE search_keyword (input_course_name VARCHAR(50))  
BEGIN  
	SELECT Courses.course_id, Courses.name AS course_name, Users.surname as instructor_surname,
	Departments.department_name, credits, classroom_id, time_slot, quota,
    GROUP_CONCAT(prerequisite_id ORDER BY prerequisite_id SEPARATOR ', ') AS prerequisites
	FROM ((((Users
	INNER JOIN Instructors ON Users.username = Instructors.username)
	INNER JOIN Departments ON Users.department_id = Departments.department_id)
    INNER JOIN Courses ON Courses.department_id = Departments.department_id)
    LEFT JOIN Prerequisites ON Courses.course_id = Prerequisites.course_id)
    WHERE Courses.name LIKE CONCAT('%', input_course_name , '%')
    GROUP BY Courses.course_id
    ORDER BY Courses.course_id ASC;
END $$  
DELIMITER ; 



-- 22




DELIMITER $$  
CREATE PROCEDURE filter_course (IN input_dep_id VARCHAR(50), IN input_campus VARCHAR(50),
IN min_credits INT, IN max_credits INT )  
BEGIN  
	IF input_dep_id NOT IN (SELECT department_id FROM Departments) THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Department ID is not valid.';
	ELSE
		SELECT Courses.course_id, Courses.name AS course_name, Users.surname as instructor_surname,
		Departments.department_name, credits, Courses.classroom_id, time_slot, quota,
		GROUP_CONCAT(prerequisite_id ORDER BY prerequisite_id SEPARATOR ', ') AS prerequisites
		FROM (((((Users
		INNER JOIN Instructors ON Users.username = Instructors.username)
		INNER JOIN Departments ON Users.department_id = Departments.department_id)
		INNER JOIN Courses ON Courses.department_id = Departments.department_id)
		INNER JOIN Physical_Locations ON Physical_Locations.classroom_id = Courses.classroom_id)
		LEFT JOIN Prerequisites ON Courses.course_id = Prerequisites.course_id)
		WHERE campus = input_campus 
        AND credits>=min_credits 
        AND credits<=max_credits 
        AND Departments.department_id = input_dep_id
		GROUP BY Courses.course_id
		ORDER BY Courses.course_id ASC;
	END IF;
END $$  
DELIMITER ;