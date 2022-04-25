-- 2018400090 - 2018400150
 CREATE database SimpleBounDB;
 USE SimpleBounDB;


-- github push trial from vscode


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
added_courses JSON,
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





DELIMITER $$  
CREATE PROCEDURE update_ins_title (IN input_username VARCHAR(50), IN input_title VARCHAR(50))  
BEGIN 
	IF input_username NOT IN (SELECT username FROM Instructors) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Instructor username is not valid.';
	ELSE
		UPDATE Instructors 
		SET title = input_title
		WHERE username = input_username;
	END IF;
END $$  
DELIMITER ; 




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




DELIMITER $$  
CREATE PROCEDURE view_instructors ()  
BEGIN  
	SELECT Users.username, name, surname, email, department_name, title
	FROM ((Instructors
	INNER JOIN Users ON Instructors.username = Users.username)
	INNER JOIN Departments ON Departments.department_id = Users.department_id);
END $$  
DELIMITER ; 




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





DELIMITER $$  
CREATE PROCEDURE view_ins_courses (IN input_ins_username VARCHAR(50))  
BEGIN  
	IF input_ins_username NOT IN (SELECT instructor_username FROM Courses) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Instructor username is not valid.';
	ELSE
		SELECT Courses.course_id, Courses.name AS course_name, Classrooms.classroom_id, campus, time_slot
		FROM ((Classrooms
		INNER JOIN Courses ON Classrooms.classroom_id = Courses.classroom_id)
		INNER JOIN Physical_Locations ON Classrooms.classroom_id = Physical_Locations.classroom_id)
		WHERE instructor_username = input_ins_username;    
	END IF;
END $$  
DELIMITER ;  





DELIMITER $$  
CREATE PROCEDURE view_avg_grade (IN input_course_id VARCHAR(50))  
BEGIN  
	IF input_course_id NOT IN (SELECT course_id FROM Courses) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course ID is not valid.';
	ELSE
		SELECT Courses.course_id, Courses.name AS course_name, sum(grade)/count(grade) AS average_grade
		FROM Courses
		INNER JOIN Grades ON Grades.course_id = Courses.course_id 
		WHERE Courses.course_id = input_course_id;
	END IF;
END $$ 
DELIMITER ;




DELIMITER $$  
CREATE PROCEDURE view_classrooms (IN input_time_slot INT)  
BEGIN  
	IF (input_time_slot>=11 OR input_time_slot<=0) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Time slot is not valid.';
	ELSE
		SELECT Physical_Locations.classroom_id, campus, classroom_capacity
		FROM Physical_Locations
		INNER JOIN Courses
		WHERE time_slot = input_time_slot;
	END IF;
END $$  
DELIMITER ; 





DELIMITER $$  
CREATE PROCEDURE add_course (IN input_course_id VARCHAR(50),
IN input_course_name VARCHAR(50), IN input_course_code VARCHAR(50),
IN input_quota INT, IN input_classroom_id VARCHAR(50), IN input_credits INT,
IN input_time_slot INT, IN ins_username VARCHAR(50))  
BEGIN  
	DECLARE dep_id VARCHAR(50);
	DECLARE capacity INT;
	SELECT classroom_capacity 
    FROM Physical_Locations
    WHERE classroom_id = input_classroom_id
    INTO capacity;
    IF capacity < input_quota THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course quota can not be greater than the capacity of the classroom.';
	ELSE
		SELECT department_id
		FROM Users
		INNER JOIN Instructors
		ON Users.username = Instructors.username
		WHERE Instructors.username = ins_username
		INTO dep_id;
		INSERT INTO Courses VALUES(input_course_id, input_course_name, dep_id,
								input_course_code, input_quota, input_classroom_id,
								input_credits, input_time_slot, ins_username);
	END IF;
END $$ 
DELIMITER ;












