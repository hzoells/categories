from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('questions/',views.QuestionList.as_view()),
    path('questions/<int:pk>/',views.QuestionDetail.as_view()),
    path('games/',views.GameList.as_view()),
    path('games/<str:game_name>',views.GameDetail.as_view()),
    path('games/<str:game_name>/questions',views.GameQuestionsList.as_view()),
    path('players/',views.PlayerList.as_view()),
    path('answers/<int:pk>',views.PlayerAnswers.as_view()),
    path('games/<str:game_name>/answers',views.GameAnswersList.as_view()),
    path('games/<str:game_name>/score',views.Score.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
