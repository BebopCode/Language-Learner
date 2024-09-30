from django.urls import path
from .views import WordCreateView
from .views import GoogleLoginView
from .views import WordUpdateView
from .views import RemoveUserData
from .views import ReturnMeaning
from .views import WordsLearnedCountView
urlpatterns = [
    path('word_data/', WordCreateView.as_view(), name='word-data'),
    path('word_update/',WordUpdateView.as_view(), name='word-update'),
    path('email/', GoogleLoginView.as_view(),name='email'),
    path('clear_user_data/', RemoveUserData.as_view(), name='delete-user-words'),
    path('word_meaning/', ReturnMeaning.as_view(), name = 'return-meaning'),
    path('words_learned/',WordsLearnedCountView.as_view(),name='words-count')
]