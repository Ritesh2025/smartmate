from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from smartmate__1 import views

admin.site.site_header = "SmartMate Admin"
admin.site.site_title = "SmartMate Admin Portal"
admin.site.index_title = "Welcome to SmartMate Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(smartmate_1.urls)),
    # path('', views.WelcomePage, name='welcome'),
    path('', views.Login, name='login'),
    path('login/<int:m>/', views.Login, name='login'),
    path('login/<int:m>/create_note/', views.Login, name='login'),
    path('login/<int:m>/download_note/', views.Login, name='login'),
    path('signup/', views.SignUp, name='signup'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.logout, name='logout'),
    path('create_note/', views.create_note, name='create_note'),
    path('download_note/', views.download_notes, name='download_note'),
    path('view_student/', views.view_student, name='view_students'),
    path('flashcard/', views.flashcard, name='flashcard'),
    path('announcement/', views.announcement, name='announcement'),
    path('view_flashcard/', views.view_flashcard, name='view_flashcard'),
    path('view_announcement/', views.view_announcement, name='view_announcement'),
    path('addInForum/', views.create_forum, name='addInForum'),
    # path('addInDiscussion/', views.addInDiscussion, name='addInDiscussion'),
    path('discussionforum/', views.discussionforum, name='discussionforum'),
]

# For using media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG():
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
