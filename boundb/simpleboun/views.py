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
    print("student")

def instructorHome(req):
    print("instructor")

def managerHome(req):
    print("manager")