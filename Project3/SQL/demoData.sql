CALL add_dbm ("manager1", "managerpass1");
CALL add_dbm ("manager2", "managerpass2");
CALL add_dbm ("manager35", "managerpass35");
CALL add_dbm ("manager4", "password4");

INSERT INTO Departments VALUES("CMPE", "Computer Engineering");
INSERT INTO Departments VALUES("IE", "Industrial Engineering");
INSERT INTO Departments VALUES("MATH", "Mathematics");
INSERT INTO Departments VALUES("PHIL", "Philosophy");
INSERT INTO Departments VALUES("POLS", "Political Science and International Relations");
  
INSERT INTO Classrooms VALUES("HD201");
INSERT INTO Physical_Locations VALUES("HD201", 100, "Hisar Campus");
INSERT INTO Classrooms VALUES("HD202");
INSERT INTO Physical_Locations VALUES("HD202", 140, "Hisar Campus");
INSERT INTO Classrooms VALUES("BMA2");
INSERT INTO Physical_Locations VALUES("BMA2", 200, "North Campus");
INSERT INTO Classrooms VALUES("BMA3");
INSERT INTO Physical_Locations VALUES("BMA3", 150, "North Campus");
INSERT INTO Classrooms VALUES("TB310");
INSERT INTO Physical_Locations VALUES("TB310", 5, "South Campus");
INSERT INTO Classrooms VALUES("M1171");
INSERT INTO Physical_Locations VALUES("M1171", 100, "South Campus");

CALL add_ins ("arzucan.ozgur", "Arzucan", "Ozgur", "arzucan.ozgur@simpleboun.edu.tr", "mypass4321", "CMPE", "Associate Professor");
CALL add_ins ("charles.sutherland", "Charles", "Sutherland", "sutherland@simpleboun.edu.tr", "princecharles", "CMPE", "Professor");
CALL add_ins ("faith.hancock", "Faith", "Hancock", "hancock@simpleboun.edu.tr", "faithfaith11", "MATH", "Associate Professor");
CALL add_ins ("lyuba.boer", "Lyuba", "Boerio", "lyub.boerio15@simpleboun.edu.tr", "easypass12", "PHIL", "Assistant Professor");
CALL add_ins ("naz.ozcan", "Naz", "Ozcan", "ozcan@simpleboun.edu.tr", "1nazozcan1", "CMPE", "Assistant Professor");
CALL add_ins ("park.ho", "Park", "Ho", "park.ho@simpleboun.edu.tr", "linkinpark", "CMPE", "Professor");
CALL add_ins ("philip.sonn", "Philip", "Sonn", "sonn.philip@simpleboun.edu.tr",	"philip-philip", "POLS", "Associate Professor");
CALL add_ins ("rosabel.eerk", "Rosabel", "Eerkens", "eerk@simpleboun.edu.tr", "eerkens1984", "IE", "Assistant Professor");
CALL add_ins ("sevgi.demir", "Sevgi", "Demirbilek", "sevgi.demir1@simpleboun.edu.tr", "dmrblk1234", "MATH", "Professor");
CALL add_ins ("simon.hunt",	"Simon",	"Hunt",	"hunt.simon@simpleboun.edu.tr",	"123abc", "PHIL", "Professor");


CALL add_student("berke.argin", "Berke", "Argin", "berke.argin@simpleboun.edu.tr", "newyork123","MATH","16080");
CALL add_student("niyazi.ulke","Niyazi","Ulke", "ulke@simpleboun.edu.tr", "mypass","CMPE","17402");
CALL add_student("ryan.andrews","Ryan","Andrews","andrews@simpleboun.edu.tr","pass4321","PHIL","18321");
CALL add_student("he.gongmin","He","Gongmin","he.gongmin@simpleboun.edu.tr","passwordpass","IE","19333");
CALL add_student("carm.galian","Carmelita","Galiano","carm.galian@simpleboun.edu.tr","madrid9897","PHIL","19356");
CALL add_student("kron.helene","Helene","Kron","kron.helene@boun.edu.tr","helenepass","CMPE","20341");
CALL add_student("aylin.karakaya","Aylin","Karakaya","aylin.karakaya@simpleboun.edu.tr","aylin12","IE","20345");
CALL add_student("demir.sari","Demir","Sari","demir@simpleboun.edu.tr","12345pass","CMPE","21246");
CALL add_student("yeager.eren","Eren","Yeager","yeager.eren@simpleboun.edu.tr","aot123","CMPE","22344");
CALL add_student("mikasa.ack","Mikasa","Ackerman","mikasa.ack@simpleboun.edu.tr","aot345","PHIL","23344");
CALL add_student("mike.knuew","Mike","Knuew","mike@simpleboun.edu.tr","passpass","POLS","23567");

INSERT INTO Courses VALUES("CMPE150", "Introduction to Computing", "CMPE", 150, 100, "HD201", 3, 1, "arzucan.ozgur");
INSERT INTO Courses VALUES("CMPE250", "Data Structures and Algorithms", "CMPE", 250, 5, "BMA2", 4, 2, "park.ho");
INSERT INTO prerequisites VALUES("CMPE250", "CMPE150");
INSERT INTO Courses VALUES("CMPE321", "Introduction to Database Systems", "CMPE", 321, 12, "BMA2", 4, 3, "arzucan.ozgur");
INSERT INTO prerequisites VALUES("CMPE321", "CMPE250");
INSERT INTO Courses VALUES("CMPE352", "Fundamentals of Software Engineering", "CMPE", 352, 120, "BMA3", 2, 3, "naz.ozcan");
INSERT INTO Courses VALUES("CMPE451", "Project Development in Software Engineering", "CMPE", 451, 120, "BMA3", 2, 10, "charles.sutherland");
INSERT INTO prerequisites VALUES("CMPE451", "CMPE321");
INSERT INTO prerequisites VALUES("CMPE451", "CMPE352");
INSERT INTO Courses VALUES("ENG493", "Sp. Tp. in Software Engineering", "CMPE", 493, 5, "BMA2", 3, 4, "park.ho");
INSERT INTO Courses VALUES("MATH101", "Calculus I", "MATH", 101, 5, "TB310", 4, 1, "faith.hancock");
INSERT INTO Courses VALUES("MATH102", "Calculus II", "MATH", 102, 5, "TB310", 4, 2, "sevgi.demir");
INSERT INTO prerequisites VALUES("MATH102", "MATH101");
INSERT INTO Courses VALUES("IE306", "Systems Simulation", "IE", 306, 100, "M1171", 3, 3, "rosabel.eerk");
INSERT INTO Courses VALUES("IE310", "Operations Research", "IE", 310, 80, "M1171", 4, 7, "rosabel.eerk");
INSERT INTO Courses VALUES("PHIL101", "Introduction to Philosophy", "PHIL", 101, 3, "M1171", 3, 10, "simon.hunt");
INSERT INTO Courses VALUES("PHIL106", "Philosophical Texts", "PHIL", 106, 100, "HD201", 3, 8, "lyuba.boer");
INSERT INTO prerequisites VALUES("PHIL106", "PHIL101");
INSERT INTO Courses VALUES("POLS101", "Introduction to Politics", "POLS", 101, 3, "HD202", 3, 6, "philip.sonn");

INSERT INTO Grades VALUES(3, "16080", "IE310");
INSERT INTO Grades VALUES(3, "16080", "CMPE150");
INSERT INTO Grades VALUES(4, "16080", "CMPE250");
INSERT INTO Grades VALUES(4, "16080", "ENG493");
INSERT INTO Grades VALUES(4, "17402", "CMPE150");
INSERT INTO Grades VALUES(3.5, "17402", "CMPE250");
INSERT INTO Grades VALUES(4, "17402", "PHIL101");
INSERT INTO Grades VALUES(3.5, "19333", "MATH101");
INSERT INTO Grades VALUES(2.5, "19333", "MATH102");
INSERT INTO Grades VALUES(3, "19356", "MATH101");
INSERT INTO Grades VALUES(4, "19356", "PHIL101");
INSERT INTO Grades VALUES(2, "19356", "POLS101");
INSERT INTO Grades VALUES(3.5, "20341", "CMPE150");
INSERT INTO Grades VALUES(3, "20341", "ENG493");
INSERT INTO Grades VALUES(3.5, "21246", "CMPE150");
INSERT INTO Grades VALUES(3.5, "21246", "CMPE250");
INSERT INTO Grades VALUES(2.5, "22344", "CMPE150");
INSERT INTO Grades VALUES(4, "22344", "CMPE250");
INSERT INTO Grades VALUES(3, "22344", "CMPE321");
INSERT INTO Grades VALUES(1, "22344", "CMPE352");
INSERT INTO Grades VALUES(3.5, "22344", "MATH101");
INSERT INTO Grades VALUES(1.5, "22344", "POLS101");
INSERT INTO Grades VALUES(3, "23344", "ENG493");
INSERT INTO Grades VALUES(3, "23344", "IE306");
INSERT INTO Grades VALUES(2.5, "23567", "POLS101");


CALL add_course_stu("berke.argin", "CMPE321");
CALL add_course_stu("berke.argin", "IE306");
CALL add_course_stu("niyazi.ülke", "CMPE321");
CALL add_course_stu("ryan.andrews", "PHIL101");
CALL add_course_stu("he.gongmin", "IE306");
CALL add_course_stu("he.gongmin", "IE310");
CALL add_course_stu("carm.galian", "MATH102");
CALL add_course_stu("carm.galian", "PHIL106");
CALL add_course_stu("kron.helene", "CMPE250");
CALL add_course_stu("demir.sari", "CMPE321");
CALL add_course_stu("demir.sari", "IE306");
CALL add_course_stu("demir.sari", "PHIL101");
CALL add_course_stu("yeager.eren", "CMPE451");
CALL add_course_stu("yeager.eren", "MATH102");
CALL add_course_stu("mikasa.ack", "CMPE150");
CALL add_course_stu("mikasa.ack", "PHIL101");
CALL add_course_stu("mikasa.ack", "POLS101");