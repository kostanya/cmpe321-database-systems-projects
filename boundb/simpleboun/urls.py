from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('student', views.student, name='student'),
    path('instructor', views.instructor, name='instructor'),
    path('manager', views.manager, name='manager'),
    path('loginStudent',views.loginStudent,name="loginStudent"),
    path('loginInstructor',views.loginInstructor,name="loginInstructor"),
    path('loginManager',views.loginManager,name="loginManager"),
    path('student/home', views.studentHome, name='studentHome'),
    path('instructor/home', views.instructorHome, name='instructorHome'),
    path('manager/home', views.managerHome, name='managerHome')
]