-- 2018400090 - 2018400150
CREATE database trial;
USE trial;

-- Create table for database managers.
CREATE TABLE IF NOT EXISTS Database_Manager
(username VARCHAR(50) NOT NULL, 
password VARCHAR(50) NOT NULL,
PRIMARY KEY (username));

-- Create table for departments.
CREATE TABLE IF NOT EXISTS Departments
(department_id VARCHAR(50) NOT NULL,
department_name VARCHAR(50) NOT NULL,
PRIMARY KEY (department_id),
UNIQUE (department_name));

-- Create trigger for fix database managers size.

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
password VARCHAR(50) NOT NULL,
department_id VARCHAR(50) NOT NULL,
PRIMARY KEY (username),
FOREIGN KEY (department_id) REFERENCES Departments(department_id) ON UPDATE CASCADE ON DELETE CASCADE);

-- Create table for students.

CREATE TABLE IF NOT EXISTS Students
(username VARCHAR(50) NOT NULL, 
student_id INTEGER NOT NULL, 
added_courses JSON,
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
course_code INTEGER NOT NULL,
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
(grade FLOAT(10) NOT NULL,
student_id INTEGER NOT NULL,
course_id VARCHAR(50) NOT NULL,
PRIMARY KEY (student_id, course_id),
FOREIGN KEY (student_id) REFERENCES Students(student_id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON UPDATE CASCADE ON DELETE CASCADE);
