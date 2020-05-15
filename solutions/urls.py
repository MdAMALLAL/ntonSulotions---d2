from django.urls import path, include, re_path
from . import views

app_name='solutions'


urlpatterns = [


    path('<int:pk>/', views.QuestionSingle.as_view(), name='questiondetail'),
    path('<int:pk>/edit',views.QuestionEdit.as_view(),name='questionedit'),
    path('nouvou/',views.QuestionCreate.as_view(),name='questioncreate'),
    path('<int:pk>/addanswere/',views.add_reponce_to_question,name='questionereponder'),
    path('<int:pk>/resolved/',views.questioneResolved,name='questioneResolved'),
    #path('page/<int:page>/',views.QuestionList.as_view(),name='questionlistpages'),
    path('',views.QuestionList.as_view(),name='questionlist'),





]
