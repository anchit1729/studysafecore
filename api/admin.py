from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name',]

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Venue)
admin.site.register(HKUMember)
admin.site.register(VisitRecord)
