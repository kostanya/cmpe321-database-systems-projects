
/*  INSERT INTO Database_Manager VALUES("furkan1", "password");
  INSERT INTO Database_Manager VALUES("furkan2", "password");
  INSERT INTO Database_Manager VALUES("furkan3", "password");
  INSERT INTO Database_Manager VALUES("furkan4", "password");

 INSERT INTO Departments VALUES("MATH", "Matematik");
 INSERT INTO Users VALUES("crazy ins", "Berke", "Bok", "email", "passsss", "MATH");
 INSERT INTO Instructors VALUES("crazy ins", "Professor");
INSERT INTO Classrooms VALUES("BMA2");

INSERT INTO Physical_Locations VALUES("BMA2", 200, "North");

 INSERT INTO Departments VALUES("CMPE", "Bilgisayar");
 INSERT INTO Users VALUES("cmpe ins", "Berke", "Bok", "email", "pas", "CMPE");
 INSERT INTO Instructors VALUES("cmpe ins", "Professor");
INSERT INTO Courses VALUES("CMPE101", "bilgisayara giris", "CMPE", 101, 150, "BMA2", 3, 1, "cmpe ins");

 INSERT INTO Courses VALUES("MATH101", "kurs ismi", "MATH", 101, 150, "BMA2", 4, 7, "crazy ins");
 INSERT INTO Courses VALUES("MATH100", "başka kurs", "MATH", 100, 150, "BMA2", 4, 9, "crazy ins");
 INSERT INTO Courses VALUES("MATH102", "bambaşka kurs", "MATH", 102, 150, "BMA2", 4, 10, "crazy ins");

 INSERT INTO prerequisites VALUES("MATH102", "MATH101");
 INSERT INTO prerequisites VALUES("MATH102", "MATH100");
-- INSERT INTO prerequisites VALUES("MATH102", "AA100");

INSERT INTO Users VALUES("denemestu", "Adam", "Bokoglu", "email", "pp", "MATH");
INSERT INTO Students (username, student_id, added_courses) VALUES("denemestu", "2018", '["a","b","c"]');

INSERT INTO Grades VALUES(3.5, "2018", "MATH102");

INSERT INTO Users VALUES("denemestu2", "Ugurcan", "Kaka", "email", "ot", "MATH");
INSERT INTO Students (username, student_id, added_courses) VALUES("denemestu2", "2019", '["a","b","c"]');

INSERT INTO Users VALUES("denemestu4", "Burak", "Yılmaz", "email", "pot", "MATH");
INSERT INTO Students (username, student_id, added_courses) VALUES("denemestu4", "2015", '["a","b","c"]');

INSERT INTO Users VALUES("denemestu3", "Badana", "Cesur", "email", "pas", "CMPE");
INSERT INTO Students (username, student_id, added_courses) VALUES("denemestu3", "2003", '["a","b","c"]');

INSERT INTO Grades VALUES(4.0, "2018", "MATH101");
INSERT INTO Grades VALUES(2.5, "2019", "MATH101");
INSERT INTO Grades VALUES(3.0, "2015", "MATH102");*/



-- limitation for credit ? 






/*-- DROP PROCEDURE IF EXISTS add_course;
DELETE FROM Courses WHERE course_id = "CMPE250";
CALL add_course("CMPE250", "Algoritma", "250", "100", "BMA2", 3, 2, "cmpe ins");


-- DROP PROCEDURE IF EXISTS view_classrooms;
CALL view_classrooms (9);


-- DROP PROCEDURE IF EXISTS delete_student;
 CALL delete_student(2018);


-- DROP PROCEDURE IF EXISTS update_ins_title;
CALL update_ins_titles("crazy ins", "Associate Professor");


-- DROP PROCEDURE IF EXISTS view_students;
CALL view_students();


-- DROP PROCEDURE IF EXISTS view_instructors;
CALL view_instructors();


-- DROP PROCEDURE IF EXISTS view_student_grades;
CALL view_student_grades(2015);


-- DROP PROCEDURE IF EXISTS view_ins_courses;
CALL view_ins_courses("crazy ins");


-- DROP PROCEDURE IF EXISTS view_avg_grade;
CALL view_avg_grade("MATH101")*/































