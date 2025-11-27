from django.urls import path

from users import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
