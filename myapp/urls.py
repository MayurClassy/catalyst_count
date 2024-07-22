from django import views
from django.urls import path
from .views import  dashboard_view, login_view, query_builder_view, record_count_view, upload_chunk, users_list
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='index'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('query_builder/', query_builder_view, name='query_builder'), 
    path('users/', users_list, name='users'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('record_count/', record_count_view, name='record_count_view'),
    path('users/', users_list, name='users_list'),
    path('upload_chunk/', upload_chunk, name='upload_chunk'),

]
