from django.urls import path

from questions import views


urlpatterns = [
    path('', views.index, name='homepage'),
    path('my-questions/', views.my_questions, name='my_questions'),
    path('new-question/', views.new_question, name='new_question'),
    path('question/<int:question_id>', views.view_question, name='view_question'),
    path('tag/<int:tag_id>', views.view_tag, name='view_tag'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('answer/', views.new_answer, name='new_answer'),
    path('vote/', views.vote, name='vote_question'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('set-best-answer/', views.set_best_answer, name='set_best_answer'),
]
