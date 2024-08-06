from django.urls import path
from . import views

app_name = 'lmsapp'

urlpatterns = [
    # Home Page
    path('', views.getstarted, name='getstarted'),

    # path('home/', views.home, name='home'),
    path('home/', views.home_new, name='home_new'),
    path('course/', views.course, name='course'),
    path('video/', views.video, name='video'),

    # Registration and Login
    path('register/', views.register_student, name='register'),
    path('login/', views.login, name='login'),

    # Forgot Pass
    path('request_otp/', views.request_otp, name='request_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),

    # #Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    ###########################################################################
    path('dashboard2/', views.dashboard2, name='dashboard2'),
    path('dash_course/', views.dash_course, name='dash_course'),
    path('search/', views.search, name='search'),
    path('resource/', views.resource, name='resource'),
    path('calendar/', views.calendar, name='calendar'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),

    ######################################################################################################

    path('add-course/', views.add_course, name='add_course'),
    path('add-video/', views.add_video, name='add_video'),

]