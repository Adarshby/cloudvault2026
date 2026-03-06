from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('register/', views.register, name='register'),
    path('share/<uuid:token>/', views.share_download, name='share_download'),
    path('admin/', admin.site.urls),
    path('', include('storage.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]


