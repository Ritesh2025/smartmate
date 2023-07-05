from django.contrib import admin
# from .models import FacultyDetail, StudentDetail, DepartmentDetail, CourseDetail, Subject, Note, Flashcard, Announcement, Discussion, Forum
from .models import *

class Facdetails(admin.ModelAdmin):
    list_display=('fid','name','email','password', 'did_fk')

class Studetails(admin.ModelAdmin):
    list_display=('sid', 'name', 'email', 'password', 'cid_fk', 'access_stu')

class DeptDetails(admin.ModelAdmin):
    list_display=('did', 'dname')

class CourseDetails(admin.ModelAdmin):
    list_display=('cid', 'cname', 'did_fk')

class Subjects(admin.ModelAdmin):
    list_display=('sub_id', 'sub_name', 'did_fk', 'cid_fk', 'fid_fk')

class Notes(admin.ModelAdmin):
    list_display=('note_id', 'note_text', 'file', 'fid_fk', 'sub_id_fk', 'cid_fk')

class Flashcards(admin.ModelAdmin):
    list_display=('card_id', 'set_title', 'sub_id_fk', 'sid_fk', 'cid_fk', 'term','desc')

class Announcements(admin.ModelAdmin):
    list_display=('ann_id', 'title', 'desc', 'fid_fk', 'sub_id_fk', 'cid_fk','date')

class Forums(admin.ModelAdmin):
    list_display=('forum_id','name', 'topic', 'description', 'date_created', 'created_by')

class Discussions(admin.ModelAdmin):
    list_display=('dis_id', 'forum', 'discuss', 'date_created', 'created_by')


# Register your models here.
admin.site.register(FacultyDetail, Facdetails)
admin.site.register(StudentDetail, Studetails)
admin.site.register(DepartmentDetail, DeptDetails)
admin.site.register(CourseDetail, CourseDetails)
admin.site.register(Subject, Subjects)
admin.site.register(Note, Notes)
admin.site.register(Flashcard, Flashcards)
admin.site.register(Announcement, Announcements)
admin.site.register(Forum, Forums)
admin.site.register(Discussion, Discussions)