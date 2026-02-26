# C:\PVSY\RoleProject\roles\forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, ADMIN, MANAGER, EMPLOYEE # Import all constants
from django.contrib.auth.models import User
from .models import Shift, Announcement
from .models import Shift
from .models import Event
from .models import LeaveRequest
from django.utils import timezone
from .models import Announcement

# --- 1. DEFINE A NEW CHOICE LIST FOR THE FORM ---
ASSIGNABLE_ROLES = (
    (ADMIN, 'Admin'),
    (MANAGER, 'Manager'),
    # Note: EMPLOYEE is intentionally excluded here
)
# ------------------------------------------------

class UserRegistrationForm(UserCreationForm):
    # Add the email field explicitly
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter email'})
    )
    
    # 2. Use the new, limited choice list
    role = forms.ChoiceField(
        choices=ASSIGNABLE_ROLES, # <-- USE THE LIMITED LIST
        label='Assign Role',
        initial=MANAGER, # You can set the initial selection
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'role',)





class AdminEmployeeRegistrationForm(forms.ModelForm):
    # Base User Fields
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    # Role Field (Admin adding a new employee)
    # The Admin can choose to add an Employee or a Manager
    role = forms.ChoiceField(
        choices=[(EMPLOYEE, 'Employee'), (MANAGER, 'Manager')],
        initial=EMPLOYEE,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        # Note: 'role' is added below in the clean method.

    def clean_password_confirm(self):
        # Validation for password matching
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirm

    def save(self, commit=True):
        # 1. Create the base User
        # Use create_user to properly hash the password
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        # 2. Assign the chosen role directly to the UserProfile created by the signal.
        # The signal in models.py has already created the UserProfile by this point.
        user.userprofile.role = self.cleaned_data['role']
        user.userprofile.save()
        
        return user
    



class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        # Use only the fields you want the Admin to fill out
        fields = ['employee', 'date', 'start_time', 'end_time'] 
        widgets = {
            # Optional: Add widgets for better user experience
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }







class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'start_time', 'end_time', 'location', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            # Use appropriate input types for date/time fields
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'required': False}),
        }

    # Optional: Add custom validation if needed (e.g., end time > start time)



class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

    # Custom validation to ensure end date is after start date and dates are in the future
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("The end date must be after the start date.")
        
        # Check that dates are not in the past (optional, but good practice)
        today = timezone.now().date()
        if start_date and start_date < today:
             raise ValidationError("Leave request must start on or after today.")

        return cleaned_data
    



class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content'] # Only title and content
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Announcement Details...', 
                'rows': 3
            }),
        }