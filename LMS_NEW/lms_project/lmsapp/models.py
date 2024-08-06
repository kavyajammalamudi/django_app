from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import string

# ID generation functions
def generate_student_id():
    last_student = Student.objects.all().order_by('Student_ID').last()
    if not last_student:
        return 'SID00001'
    student_id = last_student.Student_ID
    new_id = int(student_id[3:]) + 1
    return 'SID' + str(new_id).zfill(5)

def generate_admin_id():
    last_admin = Admin.objects.all().order_by('Admin_ID').last()
    if not last_admin:
        return 'AID00001'
    admin_id = last_admin.Admin_ID
    new_id = int(admin_id[3:]) + 1
    return 'AID' + str(new_id).zfill(5)

def generate_teacher_id():
    last_teacher = Teacher.objects.all().order_by('Teacher_ID').last()
    if not last_teacher:
        return 'TCR00001'
    teacher_id = last_teacher.Teacher_ID
    new_id = int(teacher_id[3:]) + 1
    return 'TCR' + str(new_id).zfill(5)

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self.create_user(email, password, **extra_fields)

# Base User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    mobile_no = models.CharField(max_length=10, blank=True, unique=True)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    # groups = models.ForeignKey(Group, related_name='custom_user_set')
    # user_permissions = models.ForeignKey(Permission, related_name='custom_user_set')

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permission_set', blank=True)

    def __str__(self):
        return self.email
    
# Student User Model
class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    Student_ID = models.CharField(max_length=8, unique=True)
    enrolled_courses = models.ManyToManyField('Course', blank=True, related_name='enrolled_students')

    def save(self, *args, **kwargs):
        if not self.Student_ID:
            self.Student_ID = generate_student_id()
        super().save(*args, **kwargs)

class Admin(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_admin': True})
    Admin_ID = models.CharField(max_length=8, unique=True)

    def save(self, *args, **kwargs):
        if not self.Admin_ID:
            self.Admin_ID = generate_admin_id(Student)
        super().save(*args, **kwargs)

class Teacher(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_teacher': True})
    Teacher_ID = models.CharField(max_length=8, unique=True)

    def save(self, *args, **kwargs):
        if not self.Teacher_ID:
            self.Teacher_ID = generate_admin_id(Student)
        super().save(*args, **kwargs)

###################################################################################################################

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP is valid for 10 minutes
        return timezone.now() - self.created_at <= timezone.timedelta(minutes=3)

    def __str__(self):
        return f'{self.user.email} - {self.otp}'

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

#############################################################################################################################

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='course_images/', default='course_images/default_placeholder.jpg')
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video_url = models.URLField()
    video_name = models.CharField(max_length=255)  # Field to store the name of the video
    video_des = models.TextField(blank=True, null=True)  # Field to store the description of the video
    video_number = models.PositiveIntegerField()  # Add this field to order videos

    def __str__(self):
        return self.video_name

#############################################################################################################################