from django import views
from django.urls import path
from .views import add_user_view, dashboard_view, login_view, query_builder_view, record_count_view, users_view
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='index'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('query_builder/', query_builder_view, name='query_builder'), 
    path('users/', users_view, name='users'),
    path('add_user/', add_user_view, name='add_user'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/record_count/', record_count_view, name='record_count_view'),
  

]
