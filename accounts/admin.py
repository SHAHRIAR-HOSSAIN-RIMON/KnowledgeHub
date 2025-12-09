from django.contrib import admin
#You import Django’s admin system so you can register models and customize how they appear.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#BaseUserAdmin = the original admin class

#UserAdmin = your new customized admin class
#Inside your models.py, you probably defined a custom UserAdmin class (or imported one).
from  .models import User

# Register your models he

@admin.register(User)
#“Register this model (User) in the admin using the class below.”

class UserAdmin(BaseUserAdmin):
    #You create a new admin class that inherits from your base admin class.

#This lets you override or extend the default behavior.
    list_display =   ("email",'username','is_staff','is_active')
    search_fields =  ('email','username')