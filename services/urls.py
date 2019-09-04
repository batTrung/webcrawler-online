from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
    path('website-downloader/', views.item_register, name='item_register'),
    path('website-downloader/<slug:slug>', views.site_download, name='site_download'),
]
