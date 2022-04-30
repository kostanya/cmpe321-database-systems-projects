from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .db_utils import run_statement
import re

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

    try:
        result=run_statement(f"CALL login_student('{username}','{password}')")

        if result: 
            req.session["username"]=username 
            return HttpResponseRedirect('../simpleboun/student/home') 
        else:
            return HttpResponseRedirect('../simpleboun/student?fail=true')
    except Exception as e:
        return HttpResponseRedirect('../simpleboun/student?fail=true')

def loginInstructor(req):
    username=req.POST["username"]
    password=req.POST["password"]
    try: 
        result=run_statement(f"CALL login_ins('{username}','{password}')")

        if result: 
            req.session["username"]=username 
            return HttpResponseRedirect('../simpleboun/instructor/home') 
        else:
            return HttpResponseRedirect('../simpleboun/instructor?fail=true')
    except Exception as e:
        return HttpResponseRedirect('../simpleboun/instructor?fail=true')
        
def loginManager(req):
    username=req.POST["username"]
    password=req.POST["password"]

    try: 
        result=run_statement(f"CALL login_dbm('{username}','{password}')")
        
        if result: 
            req.session["username"]=username 
            return HttpResponseRedirect('../simpleboun/manager/home') 
        else:
            return HttpResponseRedirect('../simpleboun/manager?fail=true')
    except Exception as e:
        return HttpResponseRedirect('../simpleboun/manager?fail=true')

def studentHome(req):
    username=req.session["username"]
    return render(req,'studentHome.html',{"username":username})

def listAllCourses(req):
    results = run_statement(f"CALL view_all_courses()")
    username=req.session["username"]

    return render(req,'listAllCourses.html',{"username":username, "results": results})

def enrollCourse(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    
    return render(req,'enrollCourse.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def enrollCourseWorker(req):
    courseid=req.POST["courseid"]
    username=req.session["username"]

    try:
        run_statement(f"CALL add_course_stu('{username}','{courseid}');")
        
        return HttpResponseRedirect('../student/enrollCourse?success=true')
    
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)
        username=req.session["username"]
        
        return render(req,'enrollCourse.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)[8:-2]})

def listMyCourses(req):
    username=req.session["username"]
    results = run_statement(f"CALL view_my_courses_stu('{username}');")

    return render(req,'listMyCourses.html',{"username":username, "results": results}) 

def searchKeyword(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]

    return render(req,'searchKeyword.html',{"username":username, "action_fail":isFailed})

def searchKeywordWorker(req):
    keyword=req.POST["keyword"]
    username=req.session["username"]
    isFailed=req.GET.get("fail",False)

    try:
        results = run_statement(f"CALL search_keyword('{keyword}');")
        if results: 
            return render(req,'searchKeyword.html',{"username":username, "action_fail":isFailed, "results":results}) 
        else:
            isFailed=req.GET.get("fail",True)
            return render(req,'searchKeyword.html',{"username":username, "action_fail":isFailed, "results":results})         
    except Exception as e:
        print(str(e)[8:-2])
        
        return HttpResponseRedirect('../student/searchKeyword?fail=true')

def filterCourses(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]
   
    return render(req,'filterCourses.html',{"username":username, "action_fail":isFailed})

def filterCoursesWorker(req):
    department=req.POST["department"]
    campus=req.POST["campus"]
    minCredits=req.POST["minCredits"]
    maxCredits=req.POST["maxCredits"]
    username=req.session["username"]
    isFailed=req.GET.get("fail",False)
   
    try:
        results=run_statement(f"CALL filter_course('{department}','{campus}','{minCredits}','{maxCredits}');")
        
        if results:
            return render(req,'filterCourses.html',{"username":username, "action_fail":isFailed,"results":results})
        else: 
            isFailed=req.GET.get("fail",True)
            return render(req,'filterCourses.html',{"username":username, "action_fail":isFailed,"results":results})
    except Exception as e:
        print(str(e)[8:-2])
   
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
    username=req.session["username"]
    isFailed=req.GET.get("fail",False)

    try:
        results = run_statement(f"CALL view_classrooms('{timeslot}');")
        
        return render(req,'listClassrooms.html',{"username":username, "action_fail":isFailed, "results": results})
    except Exception as e:
        isFailed=req.GET.get("fail",True)

        return render(req,'listClassrooms.html',{"username":username, "action_fail":isFailed, "errormessage": str(e)[8:-2]})

def addCourse(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]

    return render(req,'addCourse.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def addCourseWorker(req):
    courseid=req.POST["courseid"]
    name=req.POST["name"]
    list1 = re.findall(r'\d+', courseid)
    coursecode = list1[0]
    credits=req.POST["credits"]
    classroomid=req.POST["classroomid"]
    timeslot=req.POST["timeslot"]
    quota=req.POST["quota"]
    username=req.session["username"]

    try:
        run_statement(f"CALL add_course_ins('{courseid}','{name}','{coursecode}','{quota}','{classroomid}', '{credits}', '{timeslot}','{username}');")

        return HttpResponseRedirect('../instructor/addCourse?success=true')
    except IndexError:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)

        return render(req,'addCourse.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": "Please enter a valid course ID."})
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)

        return render(req,'addCourse.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)[8:-2]})

def addPrerequisite(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]

    return render(req,'addPrerequisite.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def addPrerequisiteWorker(req):
    courseid=req.POST["courseid"]
    prerequisiteid=req.POST["prerequisiteid"]
    username=req.session["username"]

    try:
        run_statement(f"CALL add_prerequisite('{courseid}','{prerequisiteid}');")

        return HttpResponseRedirect('../instructor/addPrerequisite?success=true')
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)
        username=req.session["username"]

        return render(req,'addPrerequisite.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)[8:-2]})

def viewMyCourses(req):
    username=req.session["username"]
    results = run_statement(f"CALL view_my_courses_ins('{username}');")

    return render(req,'viewMyCourses.html',{"username":username, "results": results})

def listStudents(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]

    return render(req,'listStudents.html',{"username":username, "action_fail":isFailed})

def listStudentsWorker(req):
    courseid=req.POST["courseid"]
    username=req.session["username"]
    isFailed=req.GET.get("fail",False)

    try:
        results = run_statement(f"CALL view_my_students('{username}','{courseid}');")

        return render(req,'listStudents.html',{"username":username, "action_fail":isFailed, "results":results})
    except Exception as e:
        isFailed=req.GET.get("fail",True)

        return render(req,'listStudents.html',{"username":username, "action_fail":isFailed, "errormessage": str(e)[8:-2]})

def changeName(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]

    return render(req,'changeName.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def changeNameWorker(req):
    courseid=req.POST["courseid"]
    name=req.POST["name"]
    username=req.session["username"]

    try:
        run_statement(f"CALL update_course_name('{username}','{courseid}','{name}')")
        
        return HttpResponseRedirect('../instructor/changeName?success=true')
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)
        
        return render(req,'changeName.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)[8:-2]})

def uploadGrade(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]

    return render(req,'uploadGrade.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def uploadGradeWorker(req):
    courseid=req.POST["courseid"]
    studentid=req.POST["studentid"]
    grade=req.POST["grade"]
    username=req.session["username"]

    try:
        run_statement(f"CALL give_grade('{username}','{courseid}','{studentid}', '{grade}');")

        return HttpResponseRedirect("../instructor/uploadGrade?success=true")
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)

        return render(req,'uploadGrade.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)[8:-2]})

def managerHome(req):
    username=req.session["username"]
    return render(req,'managerHome.html',{"username":username})

def addStudent(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]

    return render(req,'addStudent.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def addStudentWorker(req):
    session_username = req.session["username"]
    username=req.POST["username"]
    name=req.POST["name"]
    surname=req.POST["surname"]
    mail=req.POST["mail"]
    password=req.POST["password"]
    departmentid=req.POST["departmentid"]
    studentid=req.POST["studentid"]


    try:
        run_statement(f"CALL add_student('{username}','{name}','{surname}','{mail}','{password}','{departmentid}', '{studentid}')")
        return HttpResponseRedirect("../manager/addStudent?success=true")
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)
        
        return render(req,'addStudent.html',{"username":session_username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)[8:-2]})

def addInstructor(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]
    return render(req,'addInstructor.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def addInstructorWorker(req):
    session_username = req.session["username"]
    username=req.POST["username"]
    name=req.POST["name"]
    surname=req.POST["surname"]
    mail=req.POST["mail"]
    password=req.POST["password"]
    departmentid=req.POST["departmentid"]
    title=req.POST["title"]

    try:
        run_statement(f"CALL add_ins('{username}','{name}','{surname}','{mail}','{password}','{departmentid}', '{title}')")
        return HttpResponseRedirect("../manager/addInstructor?success=true")
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)
        
        return render(req,'addInstructor.html',{"username":session_username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)[8:-2]})

def deleteStudent(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]

    return render(req,'deleteStudent.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def deleteStudentWorker(req):
    studentid=req.POST["studentid"]

    try:
        run_statement(f"CALL delete_student ('{studentid}');")
        return HttpResponseRedirect("../manager/deleteStudent?success=true")
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)
        username=req.session["username"]
        
        return render(req,'deleteStudent.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)[8:-2]})

def updateTitle(req):
    isFailed=req.GET.get("fail",False)
    isSuccessful=req.GET.get("success",False)
    username=req.session["username"]

    return render(req,'updateTitle.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful})

def updateTitleWorker(req):
    instructor_username=req.POST["instructor_username"]
    title=req.POST["title"]

    try:
        run_statement(f"CALL update_ins_title('{instructor_username}','{title}');")

        return HttpResponseRedirect("../manager/updateTitle?success=true")
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        isSuccessful=req.GET.get("success",False)
        username=req.session["username"]
        
        return render(req,'updateTitle.html',{"username":username, "action_fail":isFailed, "action_success": isSuccessful, "errormessage": str(e)[8:-2]})

def viewStudents(req):
    results = run_statement(f"CALL view_students();")

    username=req.session["username"]
    return render(req,'viewStudents.html',{"username":username, "results":results})

def viewInstructors(req):
    results = run_statement(f"CALL view_instructors();")

    username=req.session["username"]
    return render(req,'viewInstructors.html',{"username":username, "results":results}) 

def viewGrades(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]

    return render(req,'viewGrades.html',{"username":username, "action_fail":isFailed})

def viewGradesWorker(req):
    studentid=req.POST["studentid"]
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]

    try:
        results = run_statement(f"CALL view_student_grades('{studentid}')")
        return render(req,'viewGrades.html',{"username":username, "action_fail":isFailed, "results": results}) 
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        return render(req,'viewGrades.html',{"username":username, "action_fail":isFailed, "errormessage": str(e)[8:-2]})

def viewCourses(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]

    return render(req,'viewCourses.html',{"username":username, "action_fail":isFailed})

def viewCoursesWorker(req):
    instructor_username=req.POST["instructor_username"]
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]

    try:
        results = run_statement(f"CALL view_ins_courses('{instructor_username}');")
        return render(req,'viewCourses.html',{"username":username, "action_fail":isFailed, "results": results}) 
    except Exception as e:
        isFailed=req.GET.get("fail",True)

        return render(req,'viewCourses.html',{"username":username, "action_fail":isFailed, "errormessage": str(e)[8:-2]})

def viewAverage(req):
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]

    return render(req,'viewAverage.html',{"username":username, "action_fail":isFailed})

def viewAverageWorker(req):
    courseid=req.POST["courseid"]
    isFailed=req.GET.get("fail",False)
    username=req.session["username"]

    try:
        results = run_statement(f"CALL view_avg_grade('{courseid}');")
        return render(req,'viewAverage.html',{"username":username, "action_fail":isFailed, "results": results}) 
    except Exception as e:
        isFailed=req.GET.get("fail",True)
        return render(req,'viewAverage.html',{"username":username, "action_fail":isFailed, "errormessage": str(e)[8:-2]})