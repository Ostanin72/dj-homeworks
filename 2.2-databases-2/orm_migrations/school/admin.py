from django.contrib import admin

from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']
    list_filter = ['name']
    # inlines = [StudentTeacherInline, ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject']
    list_filter = ['name']
