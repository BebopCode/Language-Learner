from django.urls import path
from .views import WordCreateView

urlpatterns = [
    path('word_data/', WordCreateView.as_view(), name='word-data')
]