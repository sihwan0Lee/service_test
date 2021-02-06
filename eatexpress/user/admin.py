from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number',
                    'address', 'gender', 'password', 'register_date',)


# Register the admin class with the associated model
admin.site.register(User, UserAdmin)
