# C:\PVSY\RoleProject\roles\urls.py

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views 



urlpatterns = [
    # Basic Home View
     path('profile/', views.profile_view, name='profile'),
    path('', views.home_view, name='home'),
    
    # Register View (must have name='register')
    path('register/', views.register_user_view, name='register'),
    
    
    # Authentication URLs (includes /accounts/login/, /accounts/logout/, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.employee_home_view, name='home'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),


    
    
    path('', views.employee_home_view, name='home'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),

    path('dashboard/', views.role_redirect_view, name='role_redirect'),

    path('manager_dashboard/', views.manager_dashboard_view, name='manager_dashboard'),




    # --- Dashboard Functionality URLs (Placeholders) ---
    path('employees/', views.employee_list_view, name='employee_list'),
    path('shifts/', views.admin_shifts_view, name='admin_shifts'),
    path('shifts/add/', views.add_shift_view, name='add_shift_url'),
    path('attendance/', views.admin_attendance_page_view, name='admin_attendance_page'),
    path('leave_requests/', views.leave_requests_admin_view, name='leave_requests_admin'),
    path('events/', views.admin_events_page_view, name='admin_events_page'),
    # path('announcements/', views.announcement_list_view, name='announcement_list'),
    path('reports/', views.admin_reports_page_view, name='admin_reports_page'),
    path('profile/', views.admin_profile_view, name='admin_profile'),
    path('attendance_list/', views.admin_attendance_list_view, name='admin_attendance_list'),
    path('add_employee/', views.admin_add_employee_view, name='admin_add_employee'),
    #   path('announcements/add/', views.add_announcement_view, name='add_announcement_url'),
    # path('announcements/', views.announcement_list, name='announcements_url'),
    
    # The page where the admin fills out the form
    #  path('announcements/add/', views.add_announcement_view, name='add_announcement_url'),

   
    # 1. URL for Adding a New Employee (Uses the AdminEmployeeRegistrationForm)
    path('add_employee/', views.admin_add_employee_view, name='admin_add_employee'),
    
    # 2. URL for Viewing the List of Employees (Renders admin_employee_list.html)
    path('employee/dashboard/', views.employee_dashboard_view, name='employee_dashboard'),
    # ... (Your other URLs like attendance, dashboard, etc.) ...
 #
    # path('profile/', views.profile_view, name='profile'), # <-- ADD THIS LINE
    # path('profile/', views.profile_view, name='profile'),
    path('employee/dashboard/', views.employee_dashboard_view, name='employee_dashboard'),




    path('attendance/', views.employee_attendance_view, name='employee_attendance'),
    # path('shifts/', views.employee_shifts_view, name='employee_shifts'),
    path('leave/submit/', views.leave_request_submit_view, name='leave_request_submit'), # <-- ADD THIS LINE
    # path('announcements/', views.announcement_list_view, name='announcement_list'), # <-- ADD THIS LINE
    path('my-shifts/', views.employee_shifts_view, name='employee_shifts'),
    # ✅ FIX B: Add the URL pattern for Events Calendar
    path('events/calendar/', views.employee_events_calendar_view, name='employee_events_calendar'), # <-- ADD THIS LINE
    # path('reports/', views.employee_reports_view, name='employee_reports'),
    path('timesheet/', views.employee_timesheet_view, name='employee_timesheet'),
    # path('leave/submit/', views.leave_request_submit_view, name='leave_request_submit'),
    path('my-work-shifts/', views.employee_shifts_view, name='employee_shifts'),




    # --- Manager Paths (NEW FIX) ---
    path('manager/dashboard/', views.manager_dashboard_view, name='manager_dashboard'),
    path('manager/profile/', views.manager_profile_view, name='manager_profile'), # <-- FIX for the error!
    #path('manager/employees/', views.manager_employee_list_view, name='manager_employee_list'),
    path('manager/shifts/', views.manager_shifts_view, name='manager_shifts'),
    path('manager/attendance/', views.manager_attendance_page_view, name='manager_attendance_page'),
    path('manager/leave/', views.leave_requests_manager_view, name='leave_requests_manager'),
    path('manager/events/', views.manager_events_page_view, name='manager_events_page'),
    path('manager/reports/', views.manager_reports_page_view, name='manager_reports_page'),
    path('manager/timesheet/approvals/', views.manager_timesheet_approvals_view, name='manager_timesheet_approvals'),
    #path('manager/add-employee/', views.manager_add_employee_view, name='manager_add_employee'),
    
    # --- Shared Paths (if applicable) ---
    # path('announcements/', views.announcement_list_view, name='announcement_list'),

    path('manager/profile/edit/', views.manager_profile_update_view, name='manager_profile_update'),

    # path('employee/dashboard/', views.employee_dashboard_view, name='employee_dashboard'),
    # path('employee/shifts/', views.employee_shift_list_view, name='employee_shift_list'),
    path('employee/shifts/', views.employee_shifts_view, name='employee_shift_list'),
    # path('shifts/', views.employee_shifts_view, name='employee_shifts'),
    # path('announcements/add/', views.add_announcement_view, name='add_announcement_url'),


    path('employee/events/calendar/', views.employee_events_calendar_view, name='employee_events_calendar'),


    # Page to view all pending requests

#     path('manager/leave/requests/', views.manager_leave_requests_view, name='manager_leave_requests'),

# # This path handles the Approve/Reject action (must be defined AFTER the list view)
# path('manager/leave/action/<int:pk>/<str:action>/', views.manager_leave_action_view, name='manager_leave_action'),

# path('manager/leave/', views.leave_requests_admin_view, name='leave_requests_manager'),
# path('manager/leave/requests/', views.manager_leave_requests_view, name='manager_leave_requests'),

# 2. Endpoint to handle the approve/reject action
# path('manager/leave/action/<int:pk>/<str:action>/', views.manager_leave_action_view, name='manager_leave_action'),

# 3. (Your existing Admin history view should also be here, pointing to its function):
# path('admin/leave/history/', views.admin_leave_history_view, name='admin_leave_history'),
path('manager/leave/', views.leave_requests_manager_view, name='leave_requests_manager'),
    
    # The background action for buttons
    path('manager/leave/action/<int:pk>/<str:action>/', views.manager_leave_action_view, name='manager_leave_action'),
    path('employees/', views.employee_list_view, name='employee_list_url'),
    # roles/urls.py
# path('manager/shifts/', views.manager_shifts, name='manager_shifts'),
# path('manager/shifts/', views.manager_shifts, name='manager_shifts'),
path('manager/shifts/', views.manager_shifts_view, name='manager_shifts'),
path('manager/events/', views.manager_events_page_view, name='manager_events_page'),

path('attendance/', views.attendance_page_view, name='attendance_page'),
path('attendance/', views.attendance_page_view, name='attendance_page'),
# path('admin/manager-attendance/', views.view_manager_attendance, name='view_manager_attendance'),
# path('manager-attendance-log/', views.view_manager_attendance, name='view_manager_attendance'),
# path('view-manager-attendance/', views.view_manager_attendance, name='view_manager_attendance'),
# path('view-manager-attendance/', views.view_manager_attendance, name='view_manager_attendance'),
# path('view-manager-attendance/', views.view_manager_attendance, name='view_manager_attendance'),
path('view-manager-attendance/', views.view_manager_attendance, name='view_manager_attendance'),


# path('announcements/', views.admin_announcements, name='admin_announcements'),
path('announcements/', views.admin_announcements, name='admin_announcements'), #
# path('announcements/delete/<int:pk>/', views.delete_announcement, name='delete_announcement'),
path('announcements/delete/<int:pk>/', views.delete_announcement, name='delete_announcement'),
path('announcements/view/', views.announcement_list, name='announcement_list'),
path('manager/announcements/', views.announcement_list, name='announcement_list'),
]

