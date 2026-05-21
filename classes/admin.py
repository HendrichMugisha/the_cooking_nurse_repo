from django.contrib import admin
from .models import Course, ClassSession

class ClassSessionInline(admin.TabularInline):
    model = ClassSession
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'course_type', 'price', 'is_active']
    list_filter = ['course_type', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ClassSessionInline]

@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ['course', 'date', 'start_time', 'end_time', 'attendees_count', 'capacity']
    list_filter = ['course', 'date']
