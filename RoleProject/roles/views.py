# C:\PVSY\RoleProject\roles\views.py

# C:\PVSY\RoleProject\roles\views.py
from django.http import HttpResponseForbidden
from .models import UserProfile
from django.contrib import messages
from .forms import AnnouncementForm
from .models import Announcement
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import LeaveRequest, PENDING, APPROVED, REJECTED
#from .forms import EventForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # <-- IMPORT THIS
from django.contrib import messages # To display success messages
from django.contrib.auth.models import  User
from django.contrib.admin.views.decorators import staff_member_required
from .models import UserProfile, Attendance, ADMIN, MANAGER, EMPLOYEE, Shift
from .forms import AdminEmployeeRegistrationForm # 🚨 New Import
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from .models import Attendance
from roles.models import Attendance
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Event, ADMIN
#from .models import Event # <--- New Model Import
#from .forms import EventForm # <--- New Form Import
from .forms import ShiftForm
from .forms import EventForm
from .forms import LeaveRequestForm
from .models import LeaveRequest
# <--- NEW IMPORTS
# Helper dictionary for sorting days (from previous step)
from collections import OrderedDict
# from .forms import ShiftCreationForm, ShiftAssignmentForm
# DAY_ORDER = OrderedDict([
#     ('MON', 1), ('TUE', 2), ('WED', 3), ('THU', 4), 
#     ('FRI', 5), ('SAT', 6), ('SUN', 7)
# ])
#User = get_user_model()

from django.db import transaction # <-- 🛑 CRITICAL IMPORT


def access_denied_view(request):
    """View to display a 403 Forbidden page for unauthorized users."""
    # You can render a custom template 'access_denied.html' or return a simple 403 status
    
    # Option 1: Render a simple template (Recommended)
    return render(request, 'access_denied.html', status=403)

# ... other imports ...

def register_user_view(request):
    """Handles user registration with a custom form, ensuring atomicity."""
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        # Check if the form data is valid (including unique username/email checks)
        if form.is_valid():
            print("--- FORM PASSED VALIDATION ---")
            try:
                # 🛑 CRITICAL FIX: Atomicity ensures both DB operations succeed or both fail (rollback)
                with transaction.atomic():
                    # 1. Create the built-in Django User
                    print("Creating User...")
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        # Use password1 since it's the one passed validation
                        password=form.cleaned_data['password1'] 
                    )
                   
                    
                    # 2. Create the custom UserProfile
                    print(f"User {user.username} {user.email} {user.password} created successfully.")
                    print(f"User {user.id}  created successfully id.")
                    print("Creating UserProfile...")
                    print(UserProfile.objects,"UserProfileobjects")

        #             UserProfile.objects.get_or_create(
        #             #UserProfile.objects.create(
        #                 user=user,
        #                 #role=form.cleaned_data['role']
        #                 defaults={
        # 'role': form.cleaned_data['role']
    #}
                   # )
                    profile, created = UserProfile.objects.get_or_create(
                    user=user, 
                    defaults={'role': form.cleaned_data['role']}
                )
                    if not created:
                        profile.role = form.cleaned_data['role']
                        profile.save()
                    print(user,"hereentered")
                    # UserProfile.role = form.cleaned_data['role']
                    # UserProfile.save()
                    
                # 3. Success Message and Redirect (Only runs if transaction commits)
                messages.success(request, f"User {user.username} created successfully. You can now log in.")
                return redirect('login') 

            except Exception as e:
                # This block handles any rare DB errors (like the IntegrityError) and rolls back the user.
                print(f"Registration failed and rolled back due to a database error: {e}")
                messages.error(request, "Registration failed due to a server error. Please try again.")
        else:
            # 🛑 DEBUGGING: This runs if the form validation fails (e.g., username/email exists).
            print("--- FORM FAILED VALIDATION ---")
            print("Errors:", form.errors)
            # The code continues to render the form with errors below.
            
    else:
        # GET request: Render a fresh, empty form
        form = UserRegistrationForm()

    context = {'form': form}
    # Render the template (for GET request and invalid POST request)
    return render(request, 'registration/register.html', context)


def home_view(request):
    """Simple view for the home page."""
    return render(request, 'home.html')


# def register_user_view(request):
#     """Handles registration using the custom form (email + role)."""
    
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST) 
#         if form.is_valid():
#             # 1. Create the built-in Django User
#             #    *** FIX: Using 'password1' to resolve the KeyError ***
#             user = User.objects.create_user(
#                 username=form.cleaned_data['username'],
#                 email=form.cleaned_data['email'],
#                 password=form.cleaned_data['password1'] 
#             )
            
#             # 2. Create the custom UserProfile
#             UserProfile.objects.create(
#                 user=user,
#                 #role=form.cleaned_data['role']
#             )
            
#             # 3. Success Message and Redirect
#             messages.success(request, f"User {user.username} created as a {user.userprofile.get_role_display()}. You can now log in.")
#             return redirect('login') # Redirect to the login page
#         # NOTE: If form is invalid, execution falls through to render the form with errors.
#     else:
#         # GET request: Render a fresh, empty form
#         form = UserRegistrationForm()

#     context = {
#         'form': form
#     }
#     # Render the template (for both GET request and invalid POST request)
#     return render(request, 'registration/register.html', context)

# def is_privileged(user):
#     """Checks if the user has a Superuser, ADMIN, or MANAGER role."""
#     # Superuser (Django's built-in top-level admin) can always pass
#     if user.is_superuser: 
#         return True
#     try:
#         # Check the role assigned in the UserProfile
#         return user.userprofile.role in [ADMIN, MANAGER]
#     except UserProfile.DoesNotExist:
#         # If no profile exists, they don't have the required role
#         return False
# # ------------------------------------


def employee_home_view(request):
    """View for the standard employee portal home."""
    return render(request, 'employee_home.html')

def admin_dashboard_view(request):
    """View for the admin/manager dashboard."""
    return render(request, 'admin_dashboard.html') #




@login_required
def role_redirect_view(request):
    """Checks the user's role and redirects to the appropriate dashboard."""
    
    user = request.user
    
    # 1. Handle Superuser separately (optional, but often useful)
    if user.is_superuser:
        return redirect('admin:index') # Redirects to Django's built-in Admin site

    # 2. Check for UserProfile existence
    try:
        role = user.userprofile.role
    except:
        # If no UserProfile exists (e.g., old users or superuser not handled above), 
        # default to Employee/Home. You might need to handle this more strictly.
        return redirect('home')

    # 3. Role-Based Redirection
    if role in ADMIN:
        return redirect('admin_dashboard')
    
    elif role == MANAGER: # <-- New path for Managers
        return redirect('manager_dashboard')
    
    elif role == EMPLOYEE:
        return redirect('employee_dashboard')
        
    # Fallback default
    return redirect('home')





def manager_dashboard_view(request):
    """View for the Manager-specific dashboard."""
    # Ensure you are passing context or logic here if needed
    return render(request, 'manager_dashboard.html')



def employee_list_view(request):
    # Fetch all registered users
    employees = User.objects.all()
    # Pass the 'employees' list to the template
    return render(request, 'placeholder.html', {'employees': employees})





# @login_required
# def employee_list_view(request):
#     return render(request, 'placeholder.html', {'title': 'Employee List'})

@login_required
def admin_shifts_view(request):
    return render(request, 'admin_shifts.html', {'title': 'Admin Shifts'})

# --- Security Check Helper (Must be at the top!) ---
def is_admin(user):
    """Checks if the user has the Admin role."""
    # Adjust this based on whether you use UserProfile or CustomUser
    try:
        return user.is_authenticated and user.userprofile.role == ADMIN
    except AttributeError:
        return False

# --- 1. View to DISPLAY the Shifts List and Form (GET) ---
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='/access-denied/') 
def admin_shifts_view(request):
    """Handles displaying the list of shifts and the form to add a new shift."""
    
    # 1. Fetch all existing shifts
    all_shifts = Shift.objects.select_related('employee').all()
    
    # 2. Instantiate an empty form for the template
    form = ShiftForm() 
    
    context = {
        'title': 'Admin Shift Management',
        'shifts': all_shifts,
        'form': form, # Pass the form to the template
    }
    
    return render(request, 'admin_shifts.html', context)


# --- 2. View to PROCESS the Form Submission (POST) ---
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='/access-denied/')
def add_shift_view(request):
    """Handles POST request to create a new shift."""
    
    # This view should only handle POST requests
    if request.method == 'POST':
        # 1. Populate the form with the data submitted by the user
        form = ShiftForm(request.POST) 
        
        if form.is_valid():
            try:
                # 2. Save the new shift object to the database
                form.save()
                messages.success(request, "Shift has been successfully added.")
                
            except Exception as e:
                messages.error(request, f"Failed to add shift: {e}")
                
        else:
            # If invalid, show general error message
            messages.error(request, "Please correct the errors below.")
            
    # Always redirect back to the shifts list view (admin_shifts)
    # This pattern prevents form resubmission on refresh.
    return redirect('admin_shifts')




# @login_required
# def admin_attendance_page_view(request):
#     return render(request, 'placeholder.html', {'title': 'Admin Attendance Page'})

# @login_required
# def leave_requests_admin_view(request):
#     return render(request, 'placeholder.html', {'title': 'Leave Requests Admin'})
@login_required
def leave_requests_admin_view(request):
    """View for Admin to see ALL employee leave requests."""
    # Fetch all requests from the database (Pending, Approved, and Rejected)
    all_requests = LeaveRequest.objects.all().order_by('-submitted_on')
    
    context = {
        'page_title': 'Admin: All Leave Requests',
        'requests': all_requests
    }
    # 🛑 Change 'placeholder.html' to 'admin_leave_requests.html'
    return render(request, 'admin_leave_requests.html', context)

# @login_required
# def admin_events_page_view(request):
#     return render(request, 'admin_events.html', {'title': 'Admin Events Page'})
# Helper function (make sure this is correct in your file)
def is_admin(user):
    # ... (Your logic for checking the Admin role) ...
    return user.is_authenticated and user.userprofile.role == ADMIN 
    # OR for testing: return user.is_authenticated and user.is_superuser

    
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='/access-denied/') 
def admin_events_page_view(request): # This is the view at line 305
    """
    Admin page to list existing events and handle the creation of a new event.
    """
    
    # Handle Form Submission (POST Request)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Event '{form.cleaned_data['title']}' created successfully!")
            return redirect('admin_events_page') # Redirect back to the same page
        else:
            messages.error(request, "Error creating event. Please check the form inputs.")
            # Pass the invalid form back to the template
    else:
        # Handle Page Load (GET Request)
        form = EventForm()
        
    # Fetch all events for the list, sorted by date
    all_events = Event.objects.all().order_by('date', 'start_time')
    
    context = {
        'page_title': 'Events Management',
        'form': form,
        'events': all_events,
    }
    
    # 🛑 CRITICAL FIX: Ensure the template name matches the file you create 🛑
    return render(request, 'admin_events.html', context)







# 1. Page to see all announcements
@login_required(login_url='login')
def admin_announcements(request):
    """View to list and create announcements without the author field."""
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            # We save directly since we aren't adding an author manually
            form.save()
            return redirect('admin_announcements')
    else:
        form = AnnouncementForm()

    # Fetching only title, content, and date to avoid database errors with author
    announcements = Announcement.objects.all().order_by('-created_at')
    
    context = {
        'page_title': 'Announcements',
        'announcements': announcements,
        'form': form
    }
    return render(request, 'admin_announcements.html', context)

@login_required(login_url='login')
def delete_announcement(request, pk):
    """Deletes a specific announcement."""
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    return redirect('admin_announcements')





@login_required
def admin_reports_page_view(request):
    return render(request, 'placeholder.html', {'title': 'Admin Reports Page'})

# @login_required
# def admin_profile_view(request):
#     return render(request, 'placeholder.html', {'title': 'Admin Profile'})

@login_required
def admin_attendance_list_view(request):
    return render(request, 'placeholder.html', {'title': 'Employee Attendance List'})

@login_required
def admin_add_employee_view(request):
    # This is where your registration logic for admins would go
    return render(request, 'placeholder.html', {'title': 'admin_add_employee.html'})

# @login_required(login_url='login')
# def view_manager_attendance(request):
#     # This filters the records to only include users with the 'Manager' role
#     # Adjust 'userprofile__role' to match your actual model relationship
#     manager_logs = Attendance.objects.filter(
#         user__userprofile__role='Manager'
#     ).select_related('user').order_by('-clock_in_time')

#     context = {
#         'logs': manager_logs,
#         'page_title': 'Manager Attendance Logs'
#     }
#     return render(request, 'admin_view_manager_attendance.html', context)
@login_required(login_url='login')
def view_manager_attendance(request):
    """
    View for Admin to monitor ALL staff attendance logs.
    """
    # .all() fetches everyone from the database
    all_staff_logs = Attendance.objects.all().select_related('user').order_by('-clock_in_time')

    context = {
        'logs': all_staff_logs,
        'page_title': 'Staff Attendance Monitor' # Changed title for clarity
    }
    
    return render(request, 'admin_view_manager_attendance.html', context)




# C:\PVSY\RoleProject\roles\views.py

@login_required
def admin_profile_view(request):
    """View to display the logged-in Admin/Manager's details."""
    # Ensure that only Admins/Managers can access this page (optional, but good practice)
    user_role = request.user.userprofile.role
    if user_role not in [ADMIN, MANAGER]:
        return redirect('home') # Redirect employees away

    # We don't need to pass the user, Django makes 'user' available in the template context
    return render(request, 'admin_profile.html') # 🚨 Changed template name 🚨




@login_required
def admin_attendance_page_view(request):
    """Handles displaying the attendance clock and processing Clock In/Out."""
    user = request.user
    context = {}
    
    # Find the most recent, currently UN-CLOCKED-OUT record for the user
    try:
        current_shift = Attendance.objects.filter(
            user=user, 
            clock_out_time__isnull=True
        ).latest('clock_in_time')
        context['is_clocked_in'] = True
    except Attendance.DoesNotExist:
        current_shift = None
        context['is_clocked_in'] = False

    if request.method == 'POST':
        action = request.POST.get('action')
        now = timezone.now()
        
        if action == 'clock_in' and not context['is_clocked_in']:
            # Create a NEW attendance record
            Attendance.objects.create(
                user=user, 
                clock_in_time=now
            )
            context['is_clocked_in'] = True
            context['message'] = f"Clocked IN successfully at {now.strftime('%H:%M:%S')}."
            
        elif action == 'clock_out' and context['is_clocked_in']:
            # Update the existing shift record
            current_shift.clock_out_time = now
            
            # Calculate the duration of the shift
            if current_shift.clock_in_time:
                current_shift.duration = now - current_shift.clock_in_time
            
            current_shift.save()
            context['is_clocked_in'] = False
            context['message'] = f"Clocked OUT successfully at {now.strftime('%H:%M:%S')}."
        
        elif action == 'clock_in' and context['is_clocked_in']:
            context['message'] = "You are already clocked in! Clock out first."
        
        elif action == 'clock_out' and not context['is_clocked_in']:
            context['message'] = "You must Clock IN before you can Clock OUT."

    # Render the Page with the current status
    return render(request, 'admin_attendance_page.html', context)






@login_required
def admin_add_employee_view(request):
    """Admin view to register a new user (Employee or Manager)."""
    
    # Optional: Basic check to ensure only Admins can access this page
    if request.user.userprofile.role != ADMIN:
        messages.error(request, "Access Denied. Only Administrators can add employees.")
        return redirect('role_redirect')

    if request.method == 'POST':
        form = AdminEmployeeRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user and create the UserProfile with the selected role
            form.save()
            messages.success(request, f"User {form.cleaned_data['username']} added successfully.")
            return redirect('admin_add_employee') # Redirect back to a clean form
        else:
            messages.error(request, "Error adding employee. Please correct the errors below.")
            # Form with errors is passed to the template below
    else:
        form = AdminEmployeeRegistrationForm()

    context = {
        'form': form,
    }
    # CRITICAL FIX: Render the correct template
    return render(request, 'admin_add_employee.html', context)


 












def employee_dashboard_view(request):
    """View for the admin/manager dashboard."""
    return render(request, 'employee_dashboard.html') #


# @login_required  # <--- COMMENT OUT or REMOVE THIS LINE TEMPORARILY
# def profile_view(request):
#     """Placeholder view for the My Profile page."""
#     context = {
#         'user_details': request.user
#     }
#     return render(request, 'profile.html', context)

@login_required(login_url='login')
def profile_view(request):
    # This should RENDER a page, not redirect
    return render(request, 'profile.html', {
        'user': request.user,
        'profile': request.user.userprofile # Assuming you have a UserProfile model
    })






# 🎯 NEW FIX: Add the attendance view
@login_required 
def employee_attendance_view(request):
    """Placeholder view for the Employee Attendance page."""
    context = {
        'page_title': 'My Attendance Records'
    }
    # We will assume a template named 'employee_attendance.html'
    return render(request, 'employee_attendance.html', context)


def is_employee(user):
    """Checks if the user has the Employee role."""
    try:
        return user.is_authenticated and user.userprofile.role == EMPLOYEE
    except AttributeError:
        return False
        
        



@login_required
def employee_shifts_view(request):
    # This filter is the key: it only picks shifts for the LOGGED-IN user
    my_shifts = Shift.objects.filter(employee=request.user).order_by('date')
    
    context = {
        'page_title': 'My Shift Schedule',
        'shifts': my_shifts
    }
    return render(request, 'employee_shifts.html', context)

@login_required 
def leave_request_submit_view(request):
    context = {
        'page_title': 'Submit a Leave Request'
    }
    return render(request, 'leave_request_submit.html', context)







@login_required(login_url='login')
@user_passes_test(is_employee, login_url='/access-denied/')
def employee_events_calendar_view(request):
    """Displays the full list/calendar of published events for employees."""
    
    # 🛑 CRUCIAL: Fetches only future events where is_published=True 🛑
    all_published_events = Event.objects.filter(
        is_published=True,
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')
    
    context = {
        'page_title': 'Company Event Calendar',
        'events': all_published_events, # Send the list to the template
    }
    
    return render(request, 'employee_events_calendar.html', context)

# ----------------- UPDATE EXISTING DASHBOARD VIEW -----------------
# Find your existing employee_dashboard_view and add the fetching logic:
def employee_dashboard_view(request):
    # ... (Existing logic) ...

    # 🛑 ADD THIS EVENTS FETCHING LOGIC 🛑
    published_events = Event.objects.filter(
        is_published=True, 
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')[:5] # Limit to 5 for the dashboard summary

    context = {
        # ... (Your existing context variables) ...
        'published_events': published_events, # Pass the list to the dashboard template
    }
    
    return render(request, 'employee_dashboard.html', context)








# @login_required 
# def employee_reports_view(request):
#     """Placeholder view for employees to access their reports."""
#     context = {
#         'page_title': 'My Reports'
#     }
#     # We will assume a template named 'employee_reports.html'
#     return render(request, 'employee_reports.html', context)




@login_required 
def employee_timesheet_view(request):
    """Placeholder view for employees to manage their timesheets."""
    context = {
        'page_title': 'My Timesheet'
    }
    # We will assume a template named 'employee_timesheet.html'
    return render(request, 'employee_timesheet.html', context)
























@login_required 
def manager_dashboard_view(request):
    """The main manager dashboard."""
    return render(request, 'manager_dashboard.html')

# 🎯 FIX 1: Manager Profile View
@login_required
def manager_profile_view(request):
    """Manager's personal profile page."""
    context = {'page_title': 'My Manager Profile'}
    return render(request, 'manager_profile.html', context) # You will create this template

# 🎯 FIX 2-9: Placeholder Views for all other manager links





@login_required
def manager_shifts_view(request): # Renamed here
    """View for Managers to see the shifts created by Admin."""
    
    # Fetch all shifts from the database
    all_shifts = Shift.objects.select_related('employee').all().order_by('date', 'start_time')
    
    context = {
        'shifts': all_shifts,
        'title': 'Team Shift Schedule'
    }
    
    return render(request, 'manager_shifts.html', context)






# @login_required
# def manager_attendance_page_view(request):
#     context = {'page_title': 'Team Attendance Overview'}
#     return render(request, 'manager_attendance_page.html', context)

@login_required(login_url='login')
def manager_attendance_page_view(request):
    """View for Manager to see all employee attendance."""
    # Logic: Get attendance for all users who are EMPLOYEES
    # records = Attendance.objects.all().order_by('-date')
    
    context = {
        'page_title': 'Employee Attendance Records',
        'attendance_records': [], # Replace [] with records once your model is ready
    }
    return render(request, 'manager_attendance_page.html', context)





@login_required
def leave_requests_manager_view(request):
    # 1. Fetch only PENDING requests from the database
    requests = LeaveRequest.objects.filter(status=PENDING).order_by('-submitted_on')
    
    context = {
        'page_title': 'Leave Requests',
        'requests': requests  # This sends the data to your template
    }
    return render(request, 'manager_leave_requests.html', context)

@login_required
def manager_leave_action_view(request, pk, action):
    """Simple function to Approve or Reject"""
    if request.method == 'POST':
        leave_req = get_object_or_404(LeaveRequest, pk=pk)
        
        if action == 'approve':
            leave_req.status = APPROVED
        elif action == 'reject':
            leave_req.status = REJECTED
            
        leave_req.save()
        
    return redirect('leave_requests_manager')









@login_required
def manager_events_page_view(request):
    """
    View for Managers to see the list of events created by the Admin.
    """
    # Fetch all events from the database, sorted by date
    all_events = Event.objects.all().order_by('date', 'start_time')
    
    context = {
        'page_title': 'Company Events',
        'events': all_events,
    }
    
    return render(request, 'manager_events.html', context)




@login_required
def attendance_page_view(request):
    # Get today's record for this user
    today = timezone.now().date()
    attendance = Attendance.objects.filter(user=request.user, date=today).first()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'clock_in':
            if not attendance:
                Attendance.objects.create(user=request.user, clock_in=timezone.now())
                messages.success(request, "Clocked in successfully!")
            else:
                messages.warning(request, "You are already clocked in.")
                
        elif action == 'clock_out':
            if attendance and not attendance.clock_out:
                attendance.clock_out = timezone.now()
                attendance.save()
                messages.success(request, "Clocked out successfully!")
            else:
                messages.error(request, "You haven't clocked in or already clocked out.")
                
        return redirect('attendance_page')

    return render(request, 'attendance.html', {'attendance': attendance})




@login_required
def manager_reports_page_view(request):
    context = {'page_title': 'Management Reports'}
    return render(request, 'manager_reports_page.html', context)

@login_required
def manager_timesheet_approvals_view(request):
    context = {'page_title': 'Timesheet Approvals'}
    return render(request, 'manager_timesheet_approvals.html', context)


@login_required
def manager_profile_update_view(request):
    """Page to update the manager's profile."""
    context = {'page_title': 'Edit My Profile'}
    return render(request, 'manager_profile_update.html', context)


@login_required
def manager_profile_update_view(request):
    # This view will now raise a TemplateDoesNotExist error when called, 
    # but that's a controlled error, and it solves the NoReverseMatch issue.
    context = {'page_title': 'Edit My Profile'}
    return render(request, 'manager_profile_update.html', context)



@login_required
def employee_list_view(request):
    # Fetch all users to show in the 'Team Employees' list
    employees = User.objects.all()
    return render(request, 'placeholder.html', {'employees': employees})



# ... (Assume is_employee is defined) ...
    
@login_required(login_url='login')
@user_passes_test(is_employee, login_url='/access-denied/') 
def leave_request_submit_view(request):
    """
    Employee page to submit a new leave request and view history.
    """
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            # Save the request but DON'T commit yet
            leave_request = form.save(commit=False)
            # Assign the current logged-in employee to the request
            leave_request.employee = request.user
            leave_request.save()
            
            messages.success(request, "Your leave request has been submitted for approval.")
            # Redirect to the same page to show the updated history
            return redirect('leave_request_submit') 
        else:
            messages.error(request, "Error submitting request. Please correct the fields below.")
    else:
        # GET request: create a fresh, empty form
        form = LeaveRequestForm()
        
    # Fetch employee's history for the bottom section
    history = LeaveRequest.objects.filter(employee=request.user).order_by('-submitted_on')
        
    context = {
        'page_title': 'Submit a Leave Request',
        'form': form,
        'history': history,
    }
    
    # 🛑 CRITICAL FIX: Ensure the template name is correct 🛑
    return render(request, 'employee_leave_submit.html', context)



@login_required(login_url='login')
def announcement_list(request):
    """View for Managers to see the announcements posted by Admin."""
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'announcement_list.html', {
        'announcements': announcements
    })






