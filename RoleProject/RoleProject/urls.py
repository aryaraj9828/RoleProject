# C:\PVSY\RoleProject\RoleProject\urls.py

from django.contrib import admin
from django.urls import path, include



#from roles.views import role_redirect_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('roles.urls')), # Includes all your custom role URLs
    
    # --- Recommended way to handle Django Auth URLs ---
    path('accounts/', include('django.contrib.auth.urls')),
    # Simple include without defining a namespace


    
    
]