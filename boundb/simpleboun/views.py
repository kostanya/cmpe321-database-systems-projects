from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .db_utils import run_statement

def index(req):
    if req.session:
        req.session.flush()
    return render(req,'entry.html')

def student(req):
    isFailed=req.GET.get("fail",False) 
    loginForm=UserLoginForm() 
    return render(req,'loginIndexStudent.html',{"login_form":loginForm,"action_fail":isFailed})

def instructor(req):
    isFailed=req.GET.get("fail",False) 
    loginForm=UserLoginForm() 
    return render(req,'loginIndexInstructor.html',{"login_form":loginForm,"action_fail":isFailed})

def manager(req):
    isFailed=req.GET.get("fail",False) 
    loginForm=UserLoginForm() 
    return render(req,'loginIndexManager.html',{"login_form":loginForm,"action_fail":isFailed})

def loginStudent(req):
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM Users WHERE username='{username}' and password='{password}';") 

    if result: 
        req.session["username"]=username 
        return HttpResponseRedirect('../simpleboun/student/home') 
    else:
        return HttpResponseRedirect('../simpleboun/student?fail=true')

def loginInstructor(req):
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM Users WHERE username='{username}' and password='{password}';") 

    if result: 
        req.session["username"]=username 
        return HttpResponseRedirect('../simpleboun/instructor/home') 
    else:
        return HttpResponseRedirect('../simpleboun/instructor?fail=true')

def loginManager(req):
    username=req.POST["username"]
    password=req.POST["password"]

    result=run_statement(f"SELECT * FROM Database_Manager WHERE username='{username}' and password='{password}';") 

    if result: 
        req.session["username"]=username 
        return HttpResponseRedirect('../simpleboun/manager/home') 
    else:
        return HttpResponseRedirect('../simpleboun/manager?fail=true')

def studentHome(req):
    username=req.session["username"]
    return render(req,'studentHome.html',{"username":username})

def listAllCourses(req):
    ##result = SQL

    username=req.session["username"]
    return render(req,'listAllCourses.html',{"username":username}) ##add result here

def enrollCourse(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'enrollCourse.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def enrollCourseWorker(req):
    courseid=req.POST["courseid"]

    try:
        ##SQL
        return HttpResponseRedirect('../student/enrollCourse?success=true')
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../student/enrollCourse?fail=true')

def listMyCourses(req):
    ##result = SQL

    username=req.session["username"]
    return render(req,'listMyCourses.html',{"username":username}) ##add result here

def searchKeyword(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]
    return render(req,'searchKeyword.html',{"username":username, "action_fail":isFailed})

def searchKeywordWorker(req):
    keyword=req.POST["keyword"]

    try:
        ###SQL
        return render(req,'searchKeyword.html',{"username":username, "action_fail":isFailed}) ##add result here
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../student/searchKeyword?fail=true')

def filterCourses(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]
    return render(req,'filterCourses.html',{"username":username, "action_fail":isFailed})

def filterCoursesWorker(req):
    department=req.POST["deparment"]
    campus=req.POST["campus"]
    minCredits=req.POST["minCredits"]
    maxCredits=req.POST["maxCredits"]

    try:
        ###SQL
        return render(req,'filterCourses.html',{"username":username, "action_fail":isFailed}) ##add result here
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../student/filterCourses?fail=true')

def instructorHome(req):
    username=req.session["username"]
    return render(req,'instructorHome.html',{"username":username})

def listClassrooms(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]
    return render(req,'listClassrooms.html',{"username":username, "action_fail":isFailed})

def listClassroomsWorker(req):
    timeslot=req.POST["timeslot"]

    try:
        ###SQL
        return render(req,'listClassrooms.html',{"username":username, "action_fail":isFailed}) ##add result here
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../instructor/listClassrooms?fail=true')

def addCourse(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'addCourse.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def addCourseWorker(req):
    courseid=req.POST["courseid"]
    name=req.POST["name"]
    credits=req.POST["credits"]
    classroomid=req.POST["classroomid"]
    timeslot=req.POST["timeslot"]
    quota=req.POST["quota"]
    username=req.session["username"]

    try:
        run_statement(f"INSERT INTO Courses VALUES('{courseid}','{name}','CMPE', 322, NULL,'{quota}','{classroomid}', '{credits}', '{timeslot}','{username}')")
        return HttpResponseRedirect('../instructor/addCourse?success=true')
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)

        return render(req,'addCourse.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)})

def addPrerequisite(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'addPrerequisite.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def addPrerequisiteWorker(req):
    courseid=req.POST["courseid"]
    prerequisiteid=req.POST["prerequisiteid"]

    try:
        ##SQL
        return HttpResponseRedirect('../instructor/addPrerequisite?success=true')
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../instructor/addPrerequisite?fail=true')

def viewMyCourses(req):
    ##result = SQL

    username=req.session["username"]
    return render(req,'viewMyCourses.html',{"username":username}) ##add result here

def listStudents(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]
    return render(req,'listStudents.html',{"username":username, "action_fail":isFailed})

def listStudentsWorker(req):
    courseid=req.POST["courseid"]

    try:
        ##SQL
        return render(req,'listStudents.html',{"username":username, "action_fail":isFailed})
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../instructor/listStudents?fail=true')

def changeName(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'changeName.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def changeNameWorker(req):
    courseid=req.POST["courseid"]
    name=req.POST["name"]

    try:
        ##SQL
        return HttpResponseRedirect('../instructor/changeName?success=true')
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../instructor/changeName?fail=true')

def uploadGrade(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'uploadGrade.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def uploadGradeWorker(req):
    courseid=req.POST["courseid"]
    studentid=req.POST["studentid"]
    grade=req.POST["grade"]

    try:
        ##SQL
        return HttpResponseRedirect("../instructor/uploadGrade?success=true")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../instructor/uploadGrade?fail=true')

def managerHome(req):
    username=req.session["username"]
    return render(req,'managerHome.html',{"username":username})

def addStudent(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'addStudent.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def addStudentWorker(req):
    username=req.POST["username"]
    name=req.POST["name"]
    surname=req.POST["surname"]
    mail=req.POST["mail"]
    password=req.POST["password"]
    departmentid=req.POST["departmentid"]
    studentid=req.POST["studentid"]

    try:
        run_statement(f"INSERT INTO Users VALUES('{username}','{name}','{surname}','{mail}','{password}','{departmentid}')")
        run_statement(f"INSERT INTO Students VALUES('{username}', '{studentid}', NULL)")
        return HttpResponseRedirect("../manager/addStudent?success=true")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/addStudent?fail=true')

def addInstructor(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'addInstructor.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def addInstructorWorker(req):
    username=req.POST["username"]
    name=req.POST["name"]
    surname=req.POST["surname"]
    mail=req.POST["mail"]
    password=req.POST["password"]
    departmentid=req.POST["departmentid"]
    title=req.POST["title"]

    try:
        run_statement(f"INSERT INTO Users VALUES('{username}','{name}','{surname}','{mail}','{password}','{departmentid}')")
        run_statement(f"INSERT INTO Instructors VALUES('{username}', '{title}')")
        return HttpResponseRedirect("../manager/addInstructor?success=true")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/addInstructor?fail=true')

def deleteStudent(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'deleteStudent.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def deleteStudentWorker(req):
    studentid=req.POST["studentid"]

    try:
        ###SQL
        return HttpResponseRedirect("../manager/deleteStudent?success=true")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/deleteStudent?fail=true')

def updateTitle(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'updateTitle.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def updateTitleWorker(req):
    instructor_username=req.POST["instructor_username"]
    title=req.POST["title"]

    try:
        ###SQL
        return HttpResponseRedirect("../manager/updateTitle?success=true")
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/updateTitle?fail=true')

def viewStudents(req):
    ##result = SQL

    username=req.session["username"]
    return render(req,'viewStudents.html',{"username":username}) ##add result here

def viewInstructors(req):
    ##result = SQL

    username=req.session["username"]
    return render(req,'viewInstructors.html',{"username":username}) ##add result here

def viewGrades(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]
    return render(req,'viewGrades.html',{"username":username, "action_fail":isFailed})

def viewGradesWorker(req):
    studentid=req.POST["studentid"]

    try:
        ###SQL
        return render(req,'viewGrades.html',{"username":username, "action_fail":isFailed}) ##add result here
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/viewGrades?fail=true')

def viewCourses(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]
    return render(req,'viewCourses.html',{"username":username, "action_fail":isFailed})

def viewCoursesWorker(req):
    instructor_username=req.POST["instructor_username"]

    try:
        ###SQL
        return render(req,'viewCourses.html',{"username":username, "action_fail":isFailed}) ##add result here
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/viewCourses?fail=true')

def viewAverage(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]
    return render(req,'viewAverage.html',{"username":username, "action_fail":isFailed})

def viewAverageWorker(req):
    courseid=req.POST["courseid"]

    try:
        ###SQL
        return render(req,'viewAverage.html',{"username":username, "action_fail":isFailed}) ##add result here
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('../manager/viewAverage?fail=true')