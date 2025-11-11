from django.contrib import admin
from .models import Teacher, Discipline, RequestedDiscipline


admin.site.register(Teacher)
admin.site.register(Discipline)
admin.site.register(RequestedDiscipline)
