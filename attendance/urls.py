from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search_attendance/', views.search_attendance, name='search_attendance'),
    path('update_student_redirect/', views.update_student_redirect, name='update_student_redirect'),
    path('update_student/', views.update_student, name='update_student'),
    path('attendance/', views.take_attendance, name='attendance'),
]
