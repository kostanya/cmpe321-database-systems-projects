/*CALL add_dbm ("furkan1", "password");
CALL add_dbm ("furkan2", "password");
CALL add_dbm ("furkan3", "password");
CALL add_dbm ("furkan4", "password");

INSERT INTO Departments VALUES("MATH", "Matematik");
INSERT INTO Departments VALUES("CMPE", "Bilgisayar");
  
INSERT INTO Classrooms VALUES("BMA2");
INSERT INTO Physical_Locations VALUES("BMA2", 200, "North");
INSERT INTO Classrooms VALUES("KB500");
INSERT INTO Physical_Locations VALUES("KB500", 2, "South");
INSERT INTO Classrooms VALUES("NH103");
INSERT INTO Physical_Locations VALUES("NH103", 20, "South");

CALL add_ins ("crazy ins", "Berke", "Bok", "email", "pass", "MATH", "Professor");
CALL add_ins ("cmpe ins", "Berke", "Bok", "email", "pas", "CMPE", "Professor");
CALL add_ins ("math ins", "Berke", "Bok", "email", "pas", "MATH", "Professor");

CALL add_student("denemestu", "Adam", "Bokoglu", "email", "pp", "MATH", "2018");
CALL add_student("denemestu2", "Ugurcan", "Kaka", "email", "ot", "MATH", "2019");
CALL add_student("denemestu3", "Badana", "Cesur", "email", "pas", "CMPE", "2003");
CALL add_student("denemestu4", "Burak", "Yılmaz", "email", "pot", "MATH", "2015");


INSERT INTO Courses VALUES("CMPE101", "bilgisayara giris", "CMPE", 101, 150, "BMA2", 3, 1, "cmpe ins");
INSERT INTO Courses VALUES("MATH101", "kurs ismi", "MATH", 101, 150, "BMA2", 4, 7, "crazy ins");
INSERT INTO Courses VALUES("MATH100", "başka kurs", "MATH", 100, 150, "BMA2", 4, 9, "crazy ins");
INSERT INTO Courses VALUES("MATH102", "bambaşka kurs", "MATH", 102, 150, "BMA2", 4, 10, "crazy ins");

INSERT INTO prerequisites VALUES("MATH102", "MATH101");
INSERT INTO prerequisites VALUES("MATH102", "MATH100");

CALL add_course_ins("CMPE250", "Algoritma", "250", "100", "BMA2", 3, 2, "cmpe ins");
CALL add_prerequisite("CMPE250", "CMPE101");

CALL add_course_ins("CMPE350", "kors neym", "300", "250", "BMA2", "4", "5", "cmpe ins");
CALL add_course_ins("MATH200", "mat 200", "200", "200", "BMA2", "4", "6", "crazy ins");
CALL add_course_ins("CMPE350", "kors neym", "350", "2", "KB500", "3", "1", "cmpe ins");

CALL add_course_stu("denemestu3", "MATH100");
CALL add_course_stu("denemestu3", "MATH101");
CALL add_course_stu("denemestu3", "MATH102");
CALL add_course_stu("denemestu2", "MATH100");
CALL add_course_stu("denemestu2", "MATH101");
CALL add_course_stu("denemestu2", "CMPE101");
CALL add_course_stu("denemestu", "MATH100");
CALL add_course_stu("denemestu", "CMPE101");
CALL add_course_stu("denemestu", "CMPE250");
CALL add_course_stu("denemestu4", "CMPE101");
CALL add_course_stu("denemestu4", "CMPE250");
CALL add_course_stu("denemestu3", "CMPE350");
CALL add_course_stu("denemestu2", "CMPE350");
CALL add_course_stu("denemestu", "CMPE350");

CALL give_grade("crazy ins", "MATH100", "2003", "3");
CALL give_grade("crazy ins", "MATH101", "2003", "3.5");
CALL give_grade("crazy ins", "MATH100", "2018", "2.5");
CALL give_grade("cmpe ins", "CMPE101", "2019", "1.5");
CALL give_grade("cmpe ins", "CMPE101", "2015", "4");*/


/* -- DROP PROCEDURE IF EXISTS add_ins;
CALL add_ins("mathins6", "math","ins","mail","pas","MATH", "Professor" );


 -- DROP PROCEDURE IF EXISTS add_student;
CALL add_student("denemestu7", "deneme","stu","mail","pp","CMPE", "2007" );


-- DROP PROCEDURE IF EXISTS login_ins;
CALL login_ins("cmpe ins", "pas");


-- DROP PROCEDURE IF EXISTS login_student;
CALL login_student("denemestu", "pp");


-- DROP PROCEDURE IF EXISTS filter_course;
call filter_course("math", "north", 3,4);


-- DROP PROCEDURE IF EXISTS search_keyword;
CALL search_keyword("ku");


-- DROP PROCEDURE IF EXISTS view_my_courses_stu;
CALL view_my_courses_stu("denemestu3");


-- DROP PROCEDURE IF EXISTS view_my_courses_stu;
CALL view_my_courses_stu("denemestu2");


-- DROP PROCEDURE IF EXISTS add_course_stu;
CALL add_course_stu("denemestu3","CMPE101");


-- DROP PROCEDURE IF EXISTS view_all_courses;
CALL view_all_courses();


-- DROP PROCEDURE IF EXISTS give_grade;
CALL give_grade("crazy ins", "MATH100", "2018", "2.5");


-- DROP PROCEDURE IF EXISTS update_course_name;
CALL update_course_name("crazy ins", "MATH100", "introduction to math");


-- DROP PROCEDURE IF EXISTS view_my_students;
CALL view_my_students("cmpe ins", "CMPE101");


-- DROP PROCEDURE IF EXISTS view_my_courses_ins;
CALL view_my_courses_ins("crazy ins");


-- DROP PROCEDURE IF EXISTS add_prerequisite;
CALL add_prerequisite("CMPE250", "CMPE101");


-- DROP PROCEDURE IF EXISTS add_course;
DELETE FROM Courses WHERE course_id = "CMPE250";
CALL add_course("CMPE250", "Algoritma", "250", "100", "BMA2", 3, 2, "cmpe ins");


-- DROP PROCEDURE IF EXISTS view_classrooms;
CALL view_classrooms("9");


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































