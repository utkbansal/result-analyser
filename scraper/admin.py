from django.contrib import admin
from .models import Branch, College, Subject, Student

admin.site.register(Branch)
admin.site.register(College)
admin.site.register(Subject)
admin.site.register(Student)