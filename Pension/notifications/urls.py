from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<str:room_name>/', views.room, name='room'),
    path('notification/', views.NotificationSentView.as_view(), name='notification_sent'),
    path('notification_recieve/', views.NotificationRecieveView.as_view(), name='notification_recieve'),
    path('test/<pk>', views.testapi.as_view(), name='test'),
]