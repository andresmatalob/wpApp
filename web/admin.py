from django.contrib import admin
from .models import Company
from .models import Project
from .models import Task
from .models import Department
#from .models import User
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Department)
#admin.site.register(User)