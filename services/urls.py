from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	path('contact/', views.contact, name='contact'),
    path('website-downloader/', views.item_register, name='item_register'),
    path('website-downloader/refresh/<slug:slug>/', views.site_refresh, name='site_refresh'),
    path('demo/<path:file_path>', views.site_preview, name='site_preview'),
    path('website-downloader/<slug:slug>/', views.site_download, name='site_download'),
    path('website-downloader/download/<slug:slug>/', views.download_file, name='download_file'),
    path('website-downloader/stop/<str:task_id>/', views.stop_download, name='stop_download'),
]
