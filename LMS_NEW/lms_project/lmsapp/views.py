from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import HttpResponse


#Getstarted
def getstarted(request):
    return render(request,'getstarted.html')

# Home Page
def home(request):
    return render(request,'home.html')

def home_new(request):
    return render(request,'home_new.html')

def course(request):
    return render(request,'course-1.html')

def video(request):
    return render(request, 'video2.html')

# def video(request, video_id):
#     main_video = get_object_or_404(Video, id=video_id)
#     context = {
#         'main_video': main_video,
#     }
#     return render(request, 'video2.html', context)

#############################################################################################################################################

# Registration
@csrf_exempt
def register_student(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_student = True
                user.save()
                id = generate_student_id()
                Student.objects.create(user=user, Student_ID = id)
                messages.success(request, 'Registration successful. Welcome!')
                return redirect('lmsapp:login')  

            except Exception as e:
                messages.error(request, f'An error occurred during registration: {e}')

        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = CustomUserCreationForm(request.POST)


    return render(request, 'TEST.html', {'form': form})

# def register_admin(request):
#     if request.method == 'POST':
#         form = AdminForm(request.POST)
#         if form.is_valid():
#             admin = form.save()
#             return redirect('login')  # Redirect to login or other appropriate page
#     else:
#         form = AdminForm()
#     return render(request, 'register_admin.html', {'form': form})

# def register_teacher(request):
#     if request.method == 'POST':
#         form = TeacherForm(request.POST)
#         if form.is_valid():
#             teacher = form.save()
#             return redirect('login')  # Redirect to login or other appropriate page
#     else:
#         form = TeacherForm()
#     return render(request, 'register_teacher.html', {'form': form})

######################################################################################################################################################

# Login
@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            print(f"Email: {email}, Password: {password}, User: {user}")
            if user is not None:
                try:
                    student_detail = Student.objects.get(user=user)
                    auth_login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('lmsapp:dashboard')
                except Student.DoesNotExist:
                    messages.error(request, 'You must be a student to log in.')
            else:
                messages.error(request, 'Please enter a correct email and password. Note that both fields may be case-sensitive.')
        else:
            print("Form errors:", form.errors)
        
    else:
        form = UserLoginForm()
    
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")

    return render(request, 'login.html', {'form': form})

####################################################################################################################################################

@login_required
def dashboard(request):
    try:
        student_detail = Student.objects.get(user=request.user)
        student_data = {
            'first_name': student_detail.user.first_name,
            'last_name': student_detail.user.last_name,
            'email': student_detail.user.email,
            'student_id': student_detail.Student_ID,
            'phone_number': student_detail.user.mobile_no,
        }
    except Student.DoesNotExist:
        student_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'student_id': '',
            'phone_number': '',
        }
        student_detail = None

    if student_detail:
        enrolled_courses = student_detail.enrolled_courses.all()
    else:
        enrolled_courses = []

    courses_with_videos = []

    for course in enrolled_courses:
        videos = course.video_set.order_by('video_number')
        courses_with_videos.append({
            'course': course,
            'videos': videos,
            'video_count': videos.count()
        })

    context = {
        'student': student_data,
        'student_courses': courses_with_videos,
    }
    return render(request, 'test-dashboard.html', context)

###################################################################################################################################################################

@login_required
def dashboard2(request):
    try:
        student_detail = Student.objects.get(user=request.user)
        student_data = {
            'first_name': student_detail.user.first_name,
            'last_name': student_detail.user.last_name,
            'email': student_detail.user.email,
            'student_id': student_detail.Student_ID,
            'phone_number': student_detail.user.mobile_no,
        }

    except Student.DoesNotExist:
        student_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'student_id': '',
            'phone_number': '',
        }

    courses = [
        {'title': 'DevOps', 'description': 'Master the principles of DevOps...', 'image': 'images/devops.png', 'link': 'video'},  # Adjust URL or use reverse
        {'title': 'JavaScript', 'description': 'Learn JavaScript...', 'image': 'images/js-1.png', 'link': '#'},
        {'title': 'HTML', 'description': 'Learn the basics of HTML...', 'image': 'images/html-1.jpg', 'link': '#'},
        {'title': 'Linux', 'description': 'Get hands-on experience with Linux...', 'image': 'images/linux.jpeg', 'link': '#'},
        {'title': 'AWS', 'description': 'Learn about Amazon Web Services...', 'image': 'images/aws.jpg', 'link': '#'},
        {'title': 'Java', 'description': 'Learn Java programming...', 'image': 'images/java.jpg', 'link': '#'},
    ]
    
    context = {'courses': courses}
    return render(request, 'dashboard.html', context)


def dash_course(request):
    return render(request,'dash_course.html')

def resource(request):
    return render(request,'resource.html')

def profile(request):
    return render(request,'my_profile.html')

def calendar(request):
    return render(request,'calendar_page.html')

def contact(request):
    return render(request,'contact_us.html')

def search(request):
    query = request.GET.get('q')
    
    if query:
        if 'contact' in query.lower():
            return redirect('lmsapp:contact')
        elif 'resource' in query.lower() or 'resources' in query.lower():
            return redirect('lmsapp:resource')
        elif 'course' in query.lower() or 'courses' in query.lower():
            return redirect('lmsapp:dash_course')
        elif 'profile' in query.lower() or 'profile' in query.lower():
            return redirect('lmsapp:profile')
        elif 'calendar' in query.lower() or 'calendar' in query.lower():
            return redirect('lmsapp:calendar')
        
        
        
        # add other conditions as necessary
    return HttpResponse('No matching page found.')

# def courses(request):
#     courses_cards = [
#         {'title': 'HTML', 'description': 'Learn HTML basics...', 'button': 'Enroll now', 'image': 'path/to/html-image.jpg'},
#         {'title': 'CSS', 'description': 'Master CSS...', 'button': 'Enroll now', 'image': 'path/to/css-image.jpg'},
#         {'title': 'JavaScript', 'description': 'Learn JavaScript...', 'button': 'Enroll now', 'image': 'path/to/javascript-image.jpg'}
#     ]
#     return render(request, 'courses.html', {'courses_cards': courses_cards})



########################################################################################################################################################
# Forget Password 1
def request_otp(request):
    if request.method == 'POST':
        form = RequestOTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email, is_student=True)
            otp = OTP.objects.create(user=user)

            # first_name = user.first_name
            # last_name = user.last_name

            from_email = settings.EMAIL_HOST_USER

            # Send OTP to user's email
            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp.otp}. It is valid for 3 minutes.',
                    from_email,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "OTP sent to your email.")
            except Exception as e:
                messages.error(request, "Failed to send OTP. Please try again.")
            
            # Store the user's email in session to use it in the next step
            request.session['email'] = email
            request.session.set_expiry(240)
            return redirect('lmsapp:verify_otp')
        else:
            messages.error(request, "Invalid email address.")
    else:
        form = RequestOTPForm()
    return render(request, 'otp_reset_password.html', {'form': form, 'step': 'email'})


# Forget Password 2
def verify_otp(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Session expired. Please request OTP again.")
        return redirect('request_otp')
    
    user = CustomUser.objects.get(email=email, is_student=True)
    
    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data['otp']
            otp_object = OTP.objects.filter(user=user, otp=otp_input).first()
            
            if otp_object and otp_object.is_valid():
                messages.success(request, "OTP verified")
                return redirect('lmsapp:reset_password')
            else:
                messages.error(request, "Invalid or expired OTP.")
        else:
            messages.error(request, "Invalid OTP format.")
    else:
        form = VerifyOTPForm()

    return render(request, 'otp_reset_password.html', {'form': form, 'step': 'otp'})


# Forget Password 3
def reset_password(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Session expired. Please request OTP again.")
        return redirect('request_otp')

    user = CustomUser.objects.get(email=email, is_student=True)

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password successfully reset.")
            return redirect('lmsapp:login')
        else:
            messages.error(request, "The two password fields must match.")
    else:
        form = ResetPasswordForm()

    return render(request, 'otp_reset_password.html', {'form': form, 'step': 'password'})

#####################################################################################################################################

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lmsapp:add_video')
    else:
        form = CourseForm()
    return render(request, 'admin_add_course.html', {'form': form})

def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video added successfully!')
            return redirect('lmsapp:add_video')
    else:
        form = VideoForm()

    return render(request, 'admin_add_video.html', {'form': form})

################################################################################################################