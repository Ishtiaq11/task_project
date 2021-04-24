from . import views
from django.urls import include, path, re_path

urlpatterns = [
    path('quizzes/', views.quizzes_view, name='quizzes_view'),
    re_path(r'^quizzes/(?P<alias>[\w-]+)/$', views.quiz_detail_view, name='quiz_detail_view'),
    re_path(r'^quizzes/(?P<alias>[\w-]+)/options/$', views.options_view, name='options_view'),
    re_path(r'^quizzes/(?P<alias>[\w-]+)/vote/$', views.vote_view, name='vote_view'),
    re_path(r'^quizzes/(?P<alias>[\w-]+)/result/$', views.quiz_result_view, name='quiz_result_view'),
    re_path(r'^quizzes/(?P<alias>[\w-]+)/comment/$', views.CommentList.as_view(), name='quiz_comments')




]