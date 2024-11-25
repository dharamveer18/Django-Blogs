from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf.urls.static import static
#from authentication.views import *  
from django.conf import settings
from django.contrib.auth.views import LogoutView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns 

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post_detail/<str:slug>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path('login/', views.login_page, name='login_page'),
    path('sign/', views.signup_page, name="signup_page"),
    path('profile/', views.profile_view, name="profile_view"),
    path('logout/',views.logout_view, name="logout"),  
    path('edit/', views.edit_profile, name="edit_profile"),
    path('category/<str:slug>/',views.category,name="category"),
    path('tag/<str:slug>/' ,views.tag,name="tag")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
