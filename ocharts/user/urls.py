from django.urls import path

from .views import LoginView


app_name = 'user'
urlpatterns = [
    path('osu-auth/', LoginView.as_view(), name='osu-auth'),
]
