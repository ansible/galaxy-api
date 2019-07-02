from django.urls import path

from .views import TestView


app_name = 'api'
urlpatterns = [
    path('test', TestView.as_view(), name='test')
]
