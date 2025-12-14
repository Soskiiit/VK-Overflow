from django.urls import path

from questions import views


urlpatterns = [
    path('', views.index, name='homepage'),
    path('my-questions/', views.my_questions, name='my_questions'),
    path('new-question/', views.new_question, name='new_question'),
    path('question/<int:question_id>', views.view_question, name='view_question'),
    path('tag/<str:tag_name>', views.view_tag, name='view_tag'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('vote/', views.vote, name='vote_question'),
]
