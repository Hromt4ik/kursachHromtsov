from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm


from django.contrib import admin
from .models import Role
from .models import CargoCategory
from .models import CustomUser
from .models import Warehouse
from .models import Car
from .models import PointIssue
from .models import Package

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(CargoCategory)
admin.site.register(Warehouse)
admin.site.register(Car)
admin.site.register(PointIssue)
admin.site.register(Package)

# Register your models here.
