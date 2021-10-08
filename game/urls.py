from django.urls import path

from . import views

app_name = "game"

urlpatterns = [
    path('', views.index, name="index"),
    path('place/<slug:name>/', views.place, name="place"),
    path('decision/', views.decision, name="decision"),
    path('result/', views.result, name="result"),

    path('items/<slug:name>/', views.items),
    path('items/send/<slug:name>/', views.items_send),
    path('questions/person/<int:personid>/', views.get_questions),
    path('questions/<int:questionid>/', views.ask_question),
    path('questions/confirm/<int:personid>/', views.confirm_beginning),
    path('events/<slug:page>', views.check_events),
    path('submit/<slug:submit_id>/<slug:value>', views.inspector_submit),
    path('chat/<slug:name>', views.approve_chat)
]
