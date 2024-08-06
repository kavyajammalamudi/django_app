from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'mobile_no', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'Student_ID']
    list_filter = ['user__is_active']  # Filtering based on related user

class AdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'Admin_ID']
    list_filter = ['user__is_active']  # Filtering based on related user

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'Teacher_ID']
    list_filter = ['user__is_active']  # Filtering based on related user

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Teacher, TeacherAdmin)

###################################################################################
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')
    search_fields = ('name',)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('video_name', 'course',  'video_des', 'video_number',)
    search_fields = ('course', 'video_name',)
admin.site.register(Course, CourseAdmin)
admin.site.register(Video, VideoAdmin)