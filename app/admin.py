from django.contrib import admin

# Register your models here.
from .models import Subject_data, MidSemPaperSet, SemesterPaperSet

admin.site.register(Subject_data)
admin.site.register(MidSemPaperSet)
admin.site.register(SemesterPaperSet)