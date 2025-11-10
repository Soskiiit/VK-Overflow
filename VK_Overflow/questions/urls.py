from django.urls import path

from questions import views


urlpatterns = [
    path('', views.index, name='homepage'),
    path('my-questions/', views.my_questions, name='my_questions'),
    path('new-question/', views.new_question, name='new_question'),
]
