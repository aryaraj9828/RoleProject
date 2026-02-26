# C:\PVSY\RoleProject\roles\models.py
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

# --- Role Constants ---
ADMIN = 'AD'
MANAGER = 'MG'
EMPLOYEE = 'EM'

ROLE_CHOICES = [
    (ADMIN, 'Admin'),
    (MANAGER, 'Manager'),
    (EMPLOYEE, 'Employee'),
]

# --- User Profile Model ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=EMPLOYEE,
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    




class Attendance(models.Model):
    """Stores clock-in and clock-out times for a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Store the actual clock-in time
    clock_in_time = models.DateTimeField(null=True, blank=True)
    
    # Store the actual clock-out time (null if user is currently clocked in)
    clock_out_time = models.DateTimeField(null=True, blank=True)
    
    # Optional: Calculate total duration of the shift
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.clock_in_time.date() if self.clock_in_time else 'N/A'}"

    class Meta:
        # Orders attendance records by the most recent clock-in time
        ordering = ['-clock_in_time']






# --- 4. Signals for automatic UserProfile creation ---
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creates or updates the UserProfile whenever a User object is saved.
    This ensures every User has a corresponding UserProfile.
    """
    if created:
        # Only create a profile if the user object is brand new
        # We default the role to EMPLOYEE (or whatever your default is)
        UserProfile.objects.create(user=instance, role=EMPLOYEE)
    else:
        # Save the profile if it exists (for existing users)
        # Handle cases where profile might not exist for old users
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            # This handles users created before the signal was active
            UserProfile.objects.create(user=instance, role=EMPLOYEE)



User = get_user_model() # This is the base User model (or your CustomUser/UserProfile relation)

class Shift(models.Model):
    # Relate the shift to an Employee (assuming ForeignKey is appropriate)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shifts')
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.employee.username} on {self.date}"
    


# class Announcement(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     created_at = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True) 
    
#     def __str__(self):
#         return self.title[:50]






# ... (Existing models: UserProfile, Shift, Announcement) ...

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True) # Optional end time
    location = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.title} on {self.date}"
    
    class Meta:
        ordering = ['date', 'start_time']




# Assuming you have an EMPLOYEE role constant defined, if not, use a simple default
PENDING = 1
APPROVED = 2
REJECTED = 3

LEAVE_STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected'),
]

class LeaveRequest(models.Model):
    # Link the request to the submitting employee
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(max_length=500)
    
    # Type of leave (you can expand these)
    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation/Annual Leave'),
        ('personal', 'Personal Day'),
        ('other', 'Other'),
    ]
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES, default='vacation')

    # Status fields
    status = models.IntegerField(choices=LEAVE_STATUS_CHOICES, default=PENDING)
    submitted_on = models.DateTimeField(default=timezone.now)
    manager_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} ({self.status_display})"
        
    @property
    def status_display(self):
        return dict(LEAVE_STATUS_CHOICES).get(self.status)

    class Meta:
        ordering = ['-submitted_on']



# 
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE) <-- COMMENT THIS OUT
    created_at = models.DateTimeField(auto_now_add=True)